import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from random import choice

from .config import load_config, terminal_settings_path
from .paths import APP_DIR, ASSETS_DIR
from .utils import atomic_write_text, file_lock, print_error


CMD_PROFILE_GUID = "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}"
IMAGE_EXTENSIONS = {".gif", ".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def rotate_backups(backups_dir, retention):
    backups = sorted(
        backups_dir.glob("settings_*.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    for old_backup in backups[retention:]:
        try:
            old_backup.unlink()
        except OSError:
            pass


def backup_terminal_settings(settings_file, retention):
    backups_dir = APP_DIR / "backups"
    backups_dir.mkdir(exist_ok=True)
    backup_path = backups_dir / "settings_backup.json"
    shutil.copy2(settings_file, backup_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_backup = backups_dir / f"settings_{timestamp}.json"
    shutil.copy2(settings_file, timestamped_backup)
    rotate_backups(backups_dir, retention)


def collect_images(backgrounds_path):
    images = {"random": []}
    for root, _, files in os.walk(backgrounds_path):
        root_path = Path(root)
        folder_key = root_path.name if root_path != backgrounds_path else "root"
        for file_name in files:
            image_path = root_path / file_name
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            images.setdefault(folder_key, []).append(str(image_path))
            images["random"].append(str(image_path))
    return images


def force_cmd_default(settings):
    settings["defaultProfile"] = CMD_PROFILE_GUID


def change_background(background_type=None, quiet=False):
    config = load_config()
    settings_file = terminal_settings_path(config)
    terminal_config = config.get("terminal", {})
    selected_type = background_type or terminal_config.get("backgroundType", "random")
    retention = int(terminal_config.get("backupRetention", 20))
    backgrounds_path = ASSETS_DIR / "backgrounds"

    try:
        with file_lock(APP_DIR / ".terminal_settings.lock"):
            with open(settings_file, "r", encoding="utf-8") as file:
                settings = json.load(file)

            images = collect_images(backgrounds_path)
            if selected_type not in images or not images[selected_type]:
                if not quiet:
                    print(f"[DOSKEY Manager] No background group named '{selected_type}'. Using random.")
                selected_type = "random"

            available_images = images.get(selected_type, [])
            if not available_images:
                raise RuntimeError(f"No images found in {backgrounds_path}")

            current_background = settings.get("profiles", {}).get("defaults", {}).get("backgroundImage")
            if len(available_images) == 1:
                new_background = available_images[0]
            else:
                new_background = choice(available_images)
                while new_background == current_background:
                    new_background = choice(available_images)

            backup_terminal_settings(settings_file, retention)
            settings.setdefault("profiles", {}).setdefault("defaults", {})
            settings["profiles"]["defaults"]["backgroundImage"] = new_background
            settings["profiles"]["defaults"]["backgroundImageOpacity"] = terminal_config.get(
                "backgroundOpacity",
                0.26,
            )

            if terminal_config.get("forceCmdDefault", True):
                force_cmd_default(settings)

            serialized = json.dumps(settings, indent=4)
            json.loads(serialized)
            atomic_write_text(settings_file, serialized)
        return True
    except Exception as error:
        if not quiet:
            print_error("Background update failed", error)
        return False
