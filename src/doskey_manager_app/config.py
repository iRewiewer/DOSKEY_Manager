import json
import os
from pathlib import Path
from re import IGNORECASE, sub

from .paths import APP_DIR
from .utils import atomic_write_text, deep_merge, load_json


DEFAULT_CONFIG = {
    "version": 3,
    "commandPrefix": "d",
    "winStoreLocation": "%LOCALAPPDATA%\\Packages",
    "startup": {
        "showTitle": True,
        "changeBackground": True,
        "backgroundMode": "async"
    },
    "terminal": {
        "packagesPath": "%LOCALAPPDATA%\\Packages",
        "packageName": "Microsoft.WindowsTerminal_8wekyb3d8bbwe",
        "backgroundType": "random",
        "backgroundOpacity": 0.26,
        "forceCmdDefault": True,
        "backupRetention": 20
    }
}


def load_config():
    config_path = APP_DIR / "config.json"
    if not config_path.exists():
        atomic_write_text(config_path, json.dumps(DEFAULT_CONFIG, indent=4))
        return DEFAULT_CONFIG

    loaded = load_json(config_path, {})
    return deep_merge(DEFAULT_CONFIG, loaded)


def command_prefix(config=None):
    value = (config or load_config()).get("commandPrefix", DEFAULT_CONFIG["commandPrefix"])
    if not isinstance(value, str):
        return DEFAULT_CONFIG["commandPrefix"]

    prefix = value.strip()
    if not prefix or "=" in prefix or any(character.isspace() for character in prefix):
        return DEFAULT_CONFIG["commandPrefix"]
    return prefix


def expand_legacy_packages_path(raw_path):
    value = raw_path or DEFAULT_CONFIG["terminal"]["packagesPath"]
    if "%appdata%" in value.lower():
        appdata = os.environ.get("APPDATA")
        if appdata:
            value = sub("%appdata%", str(Path(appdata).parent), value, flags=IGNORECASE)
    return Path(os.path.expandvars(value))


def terminal_settings_path(config):
    terminal_config = config.get("terminal", {})
    packages_path = terminal_config.get("packagesPath") or config.get("winStoreLocation")
    package_name = terminal_config.get("packageName", DEFAULT_CONFIG["terminal"]["packageName"])
    return expand_legacy_packages_path(packages_path) / package_name / "LocalState" / "settings.json"
