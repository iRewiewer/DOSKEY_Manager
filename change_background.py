from json import loads, dumps
from os import walk, getenv, path
from shutil import copyfile
from random import choice
from argparse import ArgumentParser
from winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx, CloseKey
import os


def print_error(message, e):
    """Simple error handling function"""
    print(
        f"[DOSKEY Manager] {message}.\nCreate issue on GitHub and copy paste this message there.\nError: {e}")


def get_app_folder_path():
    """Retrieve the path of the DOSKEY Manager application from registry, excluding the filename."""
    key_path = r"SOFTWARE\Microsoft\Command Processor"
    try:
        hkey = OpenKey(HKEY_LOCAL_MACHINE, key_path)
        path_value, _ = QueryValueEx(hkey, "DoskeyManagerPath")
        CloseKey(hkey)
        path_value = path_value.strip('"')
        return os.path.dirname(path_value)
    except Exception as e:
        print_error("An error occurred getting app path from registry", e)
        return None


def load_config():
    """Load configuration from a JSON file, or create default config if missing."""
    config = {}
    app_folder = get_app_folder_path()
    if not app_folder:
        return
    config_path = os.path.join(app_folder, "config.json")
    if path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = loads(f.read())
        except Exception as e:
            print_error("An error occurred reading config", e)
    else:
        config = {
            "winStoreLocation": "%appdata%\\Local\\Packages"
        }
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(dumps(config, indent=4))
        except Exception as e:
            print_error("An error occurred creating config", e)
            exit(1)

    return config


def win_terminal_directory(config):
    """Construct the path to the Windows Terminal directory."""
    location = config.get("winStoreLocation", "")
    if "%appdata%" in location:
        appdata = getenv('APPDATA')
        base_appdata = path.dirname(appdata)
        return location.replace("%appdata%", base_appdata)
    return location


def collect_images(backgrounds_path):
    """Collect images from the backgrounds folder, organizing them by folder."""
    images = {"random": []}
    for root, dirs, files in walk(backgrounds_path):
        folder_key = path.basename(
            root) if root != backgrounds_path else "root"
        # Build full paths for each file
        full_paths = [os.path.join(root, f) for f in files]
        images.setdefault(folder_key, []).extend(full_paths)
        images["random"].extend(full_paths)
    return images


def change_background(backgrounds_path, json_path, settings, background_type):
    """Change the Windows Terminal background."""
    try:
        images = collect_images(backgrounds_path)
    except Exception as e:
        print_error(
            "An error occurred loading images from backgrounds folder", e)
        return False

    if background_type not in images or not images[background_type]:
        print(
            f"[DOSKEY Manager] Couldn't find a background folder called '{background_type}'. Changing to random.")
        background_type = "random"

    current_background = settings.get("profiles", {}).get(
        "defaults", {}).get("backgroundImage")
    available_images = images[background_type]

    # If only one image is available, use it directly
    if len(available_images) == 1:
        new_background = available_images[0]
    else:
        new_background = choice(available_images)
        # Avoid repeating the current background if possible
        if current_background in available_images and len(available_images) > 1:
            while new_background == current_background:
                new_background = choice(available_images)

    try:
        settings["profiles"]["defaults"]["backgroundImage"] = new_background
        settings["profiles"]["defaults"]["backgroundImageOpacity"] = 0.26
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(dumps(settings, indent=4))
    except Exception as e:
        print_error("An error occurred applying a new background", e)
        return False

    return True


def main():
    """Main application function."""
    config = load_config()
    app_folder = get_app_folder_path()
    if not app_folder:
        return

    terminal_dir = win_terminal_directory(config)
    json_path = os.path.join(
        terminal_dir, r"Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json")
    backgrounds_path = os.path.join(app_folder, "backgrounds")

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            settings = loads(f.read())
        # Create backup in case of failure
        backup_path = os.path.join(app_folder, "settings_backup.json")
        copyfile(json_path, backup_path)
    except Exception as e:
        print(
            f"[DOSKEY Manager] Error reading JSON via background changer script. Create issue on GitHub and copy paste this message there.\nError: {e}")
        return False

    parser = ArgumentParser(prog="bg")
    parser.add_argument('-type', default="random")
    args = parser.parse_args()

    if not change_background(backgrounds_path, json_path, settings, args.type):
        backup_path = os.path.join(app_folder, "settings_backup.json")
        copyfile(backup_path, json_path)


if __name__ == "__main__":
    main()
