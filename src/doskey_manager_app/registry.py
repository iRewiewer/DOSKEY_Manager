from datetime import datetime

from .paths import DISABLED_MARKER, LOADER_PATH
from .utils import atomic_write_text, print_error


try:
    import winreg
except ImportError:
    winreg = None


COMMAND_PROCESSOR_KEY = r"Software\Microsoft\Command Processor"


def root_for_scope(scope):
    if winreg is None:
        raise RuntimeError("Windows registry is unavailable")
    if scope == "machine":
        return winreg.HKEY_LOCAL_MACHINE
    return winreg.HKEY_CURRENT_USER


def read_reg_value(scope, name):
    if winreg is None:
        return None
    try:
        with winreg.OpenKey(root_for_scope(scope), COMMAND_PROCESSOR_KEY) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except OSError:
        return None


def write_reg_value(scope, name, value):
    with winreg.CreateKeyEx(root_for_scope(scope), COMMAND_PROCESSOR_KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)


def delete_reg_value(scope, name):
    try:
        with winreg.OpenKey(root_for_scope(scope), COMMAND_PROCESSOR_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, name)
        return True
    except FileNotFoundError:
        return True
    except PermissionError:
        raise
    except OSError:
        return False


def loader_reg_value():
    return f'"{LOADER_PATH}"'


def autorun_contains_loader(value):
    if not value:
        return False
    return str(LOADER_PATH).lower() in value.lower() or LOADER_PATH.name.lower() in value.lower()


def is_single_loader_autorun(value):
    if not value or "&" in value:
        return False
    cleaned = value.strip().strip('"').lower()
    return cleaned.endswith(f"\\{LOADER_PATH.name.lower()}") or cleaned == LOADER_PATH.name.lower()


def install(scope, migrate_from_machine=False):
    current = read_reg_value(scope, "AutoRun")
    loader_value = loader_reg_value()

    if current and autorun_contains_loader(current):
        new_value = current
    elif current:
        write_reg_value(scope, "DoskeyManagerPreviousAutoRun", current)
        new_value = f"{loader_value} & {current}"
    else:
        new_value = loader_value

    write_reg_value(scope, "AutoRun", new_value)
    write_reg_value(scope, "DoskeyManagerPath", loader_value)
    if DISABLED_MARKER.exists():
        DISABLED_MARKER.unlink()

    print(f"Installed DOSKEY Manager AutoRun in {scope}.")

    if migrate_from_machine and scope == "user":
        machine_autorun = read_reg_value("machine", "AutoRun")
        if machine_autorun and autorun_contains_loader(machine_autorun):
            try:
                uninstall("machine", quiet=True)
                print("Removed the old machine-wide AutoRun entry.")
            except PermissionError:
                print_error("Machine-wide AutoRun still exists; run uninstall as administrator for --scope machine")


def uninstall(scope, quiet=False):
    current = read_reg_value(scope, "AutoRun")
    previous = read_reg_value(scope, "DoskeyManagerPreviousAutoRun")
    loader_value = loader_reg_value()

    if current and (current.strip() == loader_value or is_single_loader_autorun(current)):
        if previous:
            write_reg_value(scope, "AutoRun", previous)
        else:
            delete_reg_value(scope, "AutoRun")
    elif current and current.startswith(f"{loader_value} & "):
        restored = current[len(f"{loader_value} & "):]
        write_reg_value(scope, "AutoRun", restored)
    elif current and autorun_contains_loader(current):
        print_error(f"AutoRun in {scope} contains DOSKEY Manager but is not in a known format; leaving it unchanged")
    elif not quiet:
        print(f"No DOSKEY Manager AutoRun found in {scope}.")

    delete_reg_value(scope, "DoskeyManagerPath")
    delete_reg_value(scope, "DoskeyManagerPreviousAutoRun")
    if DISABLED_MARKER.exists() and scope == "user":
        DISABLED_MARKER.unlink()

    if not quiet:
        print(f"Uninstalled DOSKEY Manager AutoRun from {scope}.")


def disable(scope, hard=False):
    if hard:
        uninstall(scope)
        return

    atomic_write_text(DISABLED_MARKER, f"Disabled at {datetime.now().isoformat(timespec='seconds')}\n")
    print("DOSKEY Manager is soft-disabled. Run DOSKEY_Loader.bat enable to re-enable it.")


def enable(scope):
    if DISABLED_MARKER.exists():
        DISABLED_MARKER.unlink()

    current = read_reg_value(scope, "AutoRun")
    if not autorun_contains_loader(current):
        install(scope)
    else:
        print("DOSKEY Manager is enabled.")
