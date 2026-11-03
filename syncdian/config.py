import json
import logging
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional

from syncdian.constants import (
    APPDATA_DIR, CONFIG_FILE, DEFAULT_EXCLUSIONS,
    MODE_SNAPSHOT_ZIP, SCHEDULE_DAILY
)

logger = logging.getLogger(__name__)


@dataclass
class VaultConfig:
    id: str
    name: str
    path: str
    enabled: bool = True
    backup_mode: str = MODE_SNAPSHOT_ZIP  # 'snapshot_zip' o 'mirror_sync'
    retention_count: int = 10  # Mantener últimos N zips
    last_sync: Optional[str] = None
    last_status: str = "never"  # 'success', 'failed', 'running', 'never'
    last_error: Optional[str] = None


@dataclass
class ScheduleConfig:
    enabled: bool = True
    mode: str = SCHEDULE_DAILY  # 'daily', 'interval'
    daily_time: str = "21:00"   # Formato HH:MM
    interval_hours: int = 6
    run_on_startup: bool = False


@dataclass
class GoogleDriveConfig:
    client_id: str = ""
    client_secret: str = ""
    credentials_path: str = ""
    root_folder_name: str = "Syncdian Obsidian Backups"
    root_folder_id: str = ""
    user_email: str = ""
    authenticated: bool = False


@dataclass
class AppSettings:
    language: str = "es"
    start_with_windows: bool = False
    minimize_to_tray: bool = True
    start_minimized: bool = False
    notify_on_sync: bool = True
    exclude_patterns: List[str] = field(default_factory=lambda: list(DEFAULT_EXCLUSIONS))


@dataclass
class SyncHistoryRecord:
    id: str
    timestamp: str
    vault_name: str
    status: str  # 'success', 'failed'
    mode: str
    files_count: int
    size_bytes: int
    duration_seconds: float
    message: str


class ConfigManager:
    _instance: Optional['ConfigManager'] = None

    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.vaults: List[VaultConfig] = []
        self.schedule: ScheduleConfig = ScheduleConfig()
        self.google_drive: GoogleDriveConfig = GoogleDriveConfig()
        self.settings: AppSettings = AppSettings()
        self.history: List[SyncHistoryRecord] = []
        self.load()

    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = ConfigManager()
        return cls._instance

    def ensure_directories(self):
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            (APPDATA_DIR / "logs").mkdir(parents=True, exist_ok=True)
            (APPDATA_DIR / "temp").mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"No se pudieron crear directorios de datos: {e}")

    def load(self):
        self.ensure_directories()
        if not self.config_path.exists():
            logger.info("Archivo de configuración no encontrado. Usando valores por defecto.")
            return

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Vaults
            self.vaults = [
                VaultConfig(**v) for v in data.get("vaults", [])
            ]

            # Schedule
            sched_data = data.get("schedule", {})
            self.schedule = ScheduleConfig(**sched_data)

            # Google Drive
            gdrive_data = data.get("google_drive", {})
            self.google_drive = GoogleDriveConfig(**gdrive_data)

            # Settings
            settings_data = data.get("settings", {})
            self.settings = AppSettings(**settings_data)

            # Sincronizar idioma activo
            from syncdian.i18n import set_current_language
            set_current_language(self.settings.language)

            # History (máximo los últimos 50 registros)
            hist_data = data.get("history", [])
            self.history = [SyncHistoryRecord(**h) for h in hist_data][-50:]

            logger.info("Configuración cargada correctamente.")
        except Exception as e:
            logger.error(f"Error al cargar configuración: {e}. Manteniendo valores por defecto.")

    def save(self):
        self.ensure_directories()
        try:
            data = {
                "vaults": [asdict(v) for v in self.vaults],
                "schedule": asdict(self.schedule),
                "google_drive": asdict(self.google_drive),
                "settings": asdict(self.settings),
                "history": [asdict(h) for h in self.history[-50:]],
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info("Configuración guardada en disco.")
        except Exception as e:
            logger.error(f"Error al guardar configuración: {e}")

    def add_vault(self, name: str, path: str, backup_mode: str = MODE_SNAPSHOT_ZIP) -> VaultConfig:
        vault = VaultConfig(
            id=str(uuid.uuid4())[:8],
            name=name,
            path=str(Path(path).resolve()),
            backup_mode=backup_mode
        )
        self.vaults.append(vault)
        self.save()
        return vault

    def update_vault(self, vault: VaultConfig):
        for i, v in enumerate(self.vaults):
            if v.id == vault.id:
                self.vaults[i] = vault
                break
        self.save()

    def remove_vault(self, vault_id: str):
        self.vaults = [v for v in self.vaults if v.id != vault_id]
        self.save()

    def add_history_record(self, record: SyncHistoryRecord):
        self.history.append(record)
        if len(self.history) > 100:
            self.history = self.history[-100:]
        self.save()


def get_config() -> ConfigManager:
    return ConfigManager.get_instance()

