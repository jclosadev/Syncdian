import fnmatch
import json
import logging
import os
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable

from syncdian.constants import OBSIDIAN_APPDATA_CONFIG, TEMP_DIR

logger = logging.getLogger(__name__)


class VaultManager:
    @staticmethod
    def detect_obsidian_vaults() -> List[Dict[str, str]]:
        """
        Lee el archivo de configuración oficial de Obsidian en AppData
        para detectar automáticamente los vaults existentes en la máquina.
        """
        detected = []
        try:
            if OBSIDIAN_APPDATA_CONFIG.exists():
                with open(OBSIDIAN_APPDATA_CONFIG, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    vaults_dict = data.get("vaults", {})
                    for vault_id, v_info in vaults_dict.items():
                        v_path = v_info.get("path")
                        if v_path:
                            path_obj = Path(v_path)
                            name = path_obj.name or "Obsidian Vault"
                            detected.append({
                                "id": vault_id,
                                "name": name,
                                "path": str(path_obj.resolve()),
                                "exists": path_obj.exists()
                            })
        except Exception as e:
            logger.warning(f"No se pudieron auto-detectar los vaults de Obsidian: {e}")

        return detected

    @staticmethod
    def is_excluded(relative_path: str, exclusions: List[str]) -> bool:
        """
        Comprueba si una ruta relativa coincide con los patrones de exclusión.
        Soporta comodines y separadores de carpeta tanto Windows como Unix.
        """
        norm_path = relative_path.replace("\\", "/")
        parts = norm_path.split("/")

        for pattern in exclusions:
            norm_pattern = pattern.replace("\\", "/").rstrip("/")
            # Si el patrón coincide directamente con el archivo/ruta
            if fnmatch.fnmatch(norm_path, norm_pattern) or fnmatch.fnmatch(norm_path, f"*{norm_pattern}*"):
                return True
            # Si alguna de las carpetas padre coincide con el patrón
            for part in parts:
                if fnmatch.fnmatch(part, norm_pattern):
                    return True
        return False

    @classmethod
    def scan_vault(
        cls,
        vault_path: Path,
        exclusions: List[str]
    ) -> Tuple[List[Path], int]:
        """
        Escanea todos los archivos dentro del vault que no coinciden con las exclusiones.
        Retorna la lista de rutas de archivo absolutas y el tamaño total en bytes.
        """
        vault_path = Path(vault_path).resolve()
        if not vault_path.exists() or not vault_path.is_dir():
            raise FileNotFoundError(f"La ruta del vault no existe o no es un directorio: {vault_path}")

        files_to_sync: List[Path] = []
        total_size = 0

        for root, dirs, files in os.walk(vault_path):
            # Filtrar carpetas excluidas antes de descender
            dirs_to_remove = []
            for d in dirs:
                dir_full = Path(root) / d
                rel_dir = dir_full.relative_to(vault_path)
                if cls.is_excluded(str(rel_dir), exclusions):
                    dirs_to_remove.append(d)
            for d in dirs_to_remove:
                dirs.remove(d)

            # Evaluar archivos
            for f in files:
                file_path = Path(root) / f
                try:
                    rel_file = file_path.relative_to(vault_path)
                    if not cls.is_excluded(str(rel_file), exclusions):
                        files_to_sync.append(file_path)
                        total_size += file_path.stat().st_size
                except Exception as e:
                    logger.debug(f"Error al evaluar archivo {file_path}: {e}")

        return files_to_sync, total_size

    @classmethod
    def create_vault_zip_snapshot(
        cls,
        vault_name: str,
        vault_path: Path,
        exclusions: List[str],
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Tuple[Path, int, int]:
        """
        Crea un archivo ZIP comprimido con timestamp del vault.
        Retorna (zip_path, total_files, zip_size_bytes).
        """
        vault_path = Path(vault_path).resolve()
        files, _ = cls.scan_vault(vault_path, exclusions)
        total_files = len(files)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = "".join(c for c in vault_name if c.isalnum() or c in ("-", "_", " ")).strip()
        zip_filename = f"{safe_name}_{timestamp}.zip"
        
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        zip_output_path = TEMP_DIR / zip_filename

        logger.info(f"Comenzando compresión de {vault_name} ({total_files} archivos) en {zip_output_path}")

        with zipfile.ZipFile(zip_output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for i, file_path in enumerate(files, 1):
                try:
                    rel_path = file_path.relative_to(vault_path)
                    zf.write(file_path, arcname=str(rel_path))
                except Exception as e:
                    logger.warning(f"No se pudo empaquetar {file_path}: {e}")

                if progress_callback and (i % 25 == 0 or i == total_files):
                    progress_callback(i, total_files, str(rel_path))

        zip_size = zip_output_path.stat().st_size
        logger.info(f"Snapshot ZIP creado con éxito: {zip_output_path.name} ({zip_size / 1024 / 1024:.2f} MB)")
        return zip_output_path, total_files, zip_size

