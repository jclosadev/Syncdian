import os
import sys
from pathlib import Path

APP_NAME = "Syncdian"
APP_DISPLAY_NAME = "Syncdian - Obsidian to Google Drive"
APP_VERSION = "1.0.0"

# Rutas de datos de usuario en AppData
APPDATA_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / APP_NAME
CONFIG_FILE = APPDATA_DIR / "config.json"
TOKEN_FILE = APPDATA_DIR / "token.json"
CREDENTIALS_FILE = APPDATA_DIR / "credentials.json"
LOG_DIR = APPDATA_DIR / "logs"
TEMP_DIR = APPDATA_DIR / "temp"

# Obsidian paths
OBSIDIAN_APPDATA_CONFIG = Path(os.getenv("APPDATA", "")) / "obsidian" / "obsidian.json"

# Google Drive Scopes
# Con 'drive.file', la app solo tiene acceso a los archivos y carpetas que ella misma crea.
DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]

# Modos de respaldo
MODE_SNAPSHOT_ZIP = "snapshot_zip"
MODE_MIRROR_SYNC = "mirror_sync"

# Modos de programación
SCHEDULE_DAILY = "daily"
SCHEDULE_INTERVAL = "interval"
SCHEDULE_MANUAL = "manual"

# Exclusiones estándar en Obsidian (archivos temporales/caché)
DEFAULT_EXCLUSIONS = [
    ".git",
    ".trash",
    ".obsidian/workspace*",
    ".obsidian/cache",
    ".DS_Store",
    "desktop.ini",
    "thumbs.db"
]

