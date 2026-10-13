import argparse

from .config import command_prefix, load_config, terminal_settings_path
from .paths import APP_DIR, DISABLED_MARKER, PROFILE_ORDER_PATH, PROFILES_DIR
from .profiles import emit_aliases, load_profile_order, print_aliases
from .registry import disable, enable, install, read_reg_value, uninstall
from .terminal import change_background
from .welcome import display_title


VERSION = "3.0"


def background_mode(config):
    mode = str(config.get("startup", {}).get("backgroundMode", "async")).strip().lower()
    if mode in {"async", "sync", "off"}:
        return mode
    return "async"


def should_change_background(config, mode=None):
    startup_config = config.get("startup", {})
    selected_mode = mode or background_mode(config)
    return startup_config.get("changeBackground", True) and selected_mode != "off"


def print_help():
    prefix = command_prefix()

    print("DOSKEY Manager")
    print()
    print("Commands:")
    print(f"  {prefix} help                 Show this help")
    print(f"  {prefix} aliases              List loaded aliases")
    print(f"  {prefix} status               Show registry/config status")
    print(f"  {prefix} bg [color]           Change Windows Terminal background")
    print(f"  {prefix} config               Print important config file paths")
    print(f"  {prefix} enable               Re-enable soft-disabled startup")
    print(f"  {prefix} disable              Soft-disable startup without removing AutoRun")
    print(f"  {prefix} disable --hard       Remove AutoRun for this user")
    print(f"  {prefix} install              Install AutoRun for this user")
    print(f"  {prefix} uninstall            Remove AutoRun for this user")
    print()
    print("Alias Profiles:")
    print_aliases()


def print_config_paths():
    config = load_config()
    print(f"App:       {APP_DIR}")
    print(f"Config:    {APP_DIR / 'config.json'}")
    print(f"Profiles:  {PROFILES_DIR}")
    print(f"Order:     {PROFILE_ORDER_PATH}")
    print(f"Terminal:  {terminal_settings_path(config)}")


def status():
    print_config_paths()
    print()
    print(f"Soft disabled: {'yes' if DISABLED_MARKER.exists() else 'no'}")
    print(f"HKCU AutoRun:  {read_reg_value('user', 'AutoRun') or '<not set>'}")
    print(f"HKLM AutoRun:  {read_reg_value('machine', 'AutoRun') or '<not set>'}")
    print()
    profiles_dir, load_order = load_profile_order()
    print("Profile load order:")
    for profile_file in load_order:
        marker = "" if (profiles_dir / profile_file).exists() else " (missing)"
        print(f"  {profile_file}{marker}")


def startup(alias_output):
    config = load_config()
    if DISABLED_MARKER.exists():
        emit_aliases(alias_output)
        return

    startup_config = config.get("startup", {})
    if startup_config.get("showTitle", True):
        display_title()

    mode = background_mode(config)
    if mode == "sync" and should_change_background(config, mode):
        change_background(quiet=True)

    emit_aliases(alias_output)


def startup_background():
    config = load_config()
    if DISABLED_MARKER.exists():
        return

    mode = background_mode(config)
    if mode == "async" and should_change_background(config, mode):
        change_background(quiet=True)


def build_parser():
    parser = argparse.ArgumentParser(prog=command_prefix(), description="DOSKEY Manager command suite")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("help")
    subparsers.add_parser("aliases")
    subparsers.add_parser("status")
    subparsers.add_parser("config")
    subparsers.add_parser("version")

    startup_parser = subparsers.add_parser("startup")
    startup_parser.add_argument("--alias-output", required=True)

    subparsers.add_parser("startup-background")

    emit_parser = subparsers.add_parser("emit-aliases")
    emit_parser.add_argument("--output")

    bg_parser = subparsers.add_parser("bg")
    bg_parser.add_argument("type", nargs="?")
    bg_parser.add_argument("-type", dest="type_flag", default=None)

    for name in ("install", "enable", "uninstall"):
        command_parser = subparsers.add_parser(name)
        command_parser.add_argument("--scope", choices=["user", "machine"], default="user")

    install_parser = subparsers.choices["install"]
    install_parser.add_argument("--migrate-from-machine", action="store_true")

    disable_parser = subparsers.add_parser("disable")
    disable_parser.add_argument("--scope", choices=["user", "machine"], default="user")
    disable_parser.add_argument("--hard", action="store_true")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command in (None, "help"):
        print_help()
    elif args.command == "aliases":
        print_aliases()
    elif args.command == "status":
        status()
    elif args.command == "config":
        print_config_paths()
    elif args.command == "version":
        print(f"DOSKEY Manager Version {VERSION}")
    elif args.command == "startup":
        startup(args.alias_output)
    elif args.command == "startup-background":
        startup_background()
    elif args.command == "emit-aliases":
        emit_aliases(args.output)
    elif args.command == "bg":
        if not change_background(args.type_flag or args.type):
            return 1
    elif args.command == "install":
        install(args.scope, args.migrate_from_machine)
    elif args.command == "enable":
        enable(args.scope)
    elif args.command == "disable":
        disable(args.scope, args.hard)
    elif args.command == "uninstall":
        uninstall(args.scope)
    return 0
