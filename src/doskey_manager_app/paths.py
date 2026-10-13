from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
SOURCE_DIR = PACKAGE_DIR.parent
APP_DIR = SOURCE_DIR.parent if SOURCE_DIR.name == "src" else SOURCE_DIR
ASSETS_DIR = APP_DIR / "assets"
PROFILES_DIR = APP_DIR / "profiles"
PROFILE_ORDER_PATH = APP_DIR / "profiles.json"
LOADER_PATH = APP_DIR / "DOSKEY_Loader.bat"
DISABLED_MARKER = APP_DIR / ".doskey_manager.disabled"
