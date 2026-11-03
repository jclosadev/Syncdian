import logging
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Dict, Any, List

from syncdian.config import get_config, VaultConfig, SyncHistoryRecord
from syncdian.constants import MODE_SNAPSHOT_ZIP, MODE_MIRROR_SYNC
from syncdian.core.gdrive import GoogleDriveService
from syncdian.core.vault_manager import VaultManager
from syncdian.i18n import tr

logger = logging.getLogger(__name__)


class SyncEngine:
    def __init__(
        self,
        gdrive_service: Optional[GoogleDriveService] = None,
        progress_callback: Optional[Callable[[float, str], None]] = None,
        log_callback: Optional[Callable[[str], None]] = None
    ):
        self.config_manager = get_config()
        self.gdrive = gdrive_service or GoogleDriveService()
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def _log(self, message: str):
        logger.info(message)
        if self.log_callback:
            self.log_callback(message)

    def _update_progress(self, percent: float, message: str):
        if self.progress_callback:
            self.progress_callback(percent, message)

    def sync_all_vaults(self) -> Dict[str, Any]:
        """Sincroniza todos los vaults que estén marcados como habilitados."""
        self._is_cancelled = False
        enabled_vaults = [v for v in self.config_manager.vaults if v.enabled]
        
        if not enabled_vaults:
            self._log(tr("sync_no_vaults"))
            return {"status": "skipped", "message": tr("sync_no_vaults")}

        if not self.gdrive.is_authenticated():
            err_msg = tr("sync_not_authenticated")
            self._log(f"ERROR: {err_msg}")
            return {"status": "error", "message": err_msg}

        self._log(tr("sync_starting", count=len(enabled_vaults)))
        results = []

        total_vaults = len(enabled_vaults)
        for idx, vault in enumerate(enabled_vaults):
            if self._is_cancelled:
                self._log(tr("sync_cancelled"))
                break

            base_percent = (idx / total_vaults) * 100.0
            self._log(tr("sync_processing_vault", current=idx + 1, total=total_vaults, name=vault.name))

            res = self.sync_single_vault(
                vault,
                step_progress_weight=(1.0 / total_vaults),
                current_base_percent=base_percent
            )
            results.append(res)

        self._update_progress(100.0, tr("sync_finished"))
        return {"status": "done", "results": results}

    def sync_single_vault(
        self,
        vault: VaultConfig,
        step_progress_weight: float = 1.0,
        current_base_percent: float = 0.0
    ) -> Dict[str, Any]:
        start_time = time.time()
        vault.last_status = "running"
        self.config_manager.update_vault(vault)

        vault_path = Path(vault.path)
        if not vault_path.exists():
            err = tr("sync_error_vault_missing", path=vault.path)
            self._log(f"ERROR: {err}")
            vault.last_status = "failed"
            vault.last_error = err
            self.config_manager.update_vault(vault)
            self._record_history(vault, "failed", 0, 0, time.time() - start_time, err)
            return {"vault": vault.name, "status": "failed", "error": err}

        temp_zip: Optional[Path] = None
        try:
            # 1. Obtener o crear carpeta raíz en Google Drive
            root_folder_name = self.config_manager.google_drive.root_folder_name or "Syncdian Obsidian Backups"
            self._update_progress(
                current_base_percent + 5.0 * step_progress_weight,
                tr("sync_verifying_folder", name=root_folder_name)
            )
            root_id = self.gdrive.get_or_create_folder(root_folder_name)
            self.config_manager.google_drive.root_folder_id = root_id
            self.config_manager.save()

            # Carpeta específica para este vault dentro de la raíz
            vault_folder_id = self.gdrive.get_or_create_folder(vault.name, parent_id=root_id)

            exclusions = self.config_manager.settings.exclude_patterns

            # 2. Modo Snapshot ZIP
            if vault.backup_mode == MODE_SNAPSHOT_ZIP:
                self._update_progress(
                    current_base_percent + 15.0 * step_progress_weight,
                    tr("sync_compressing_vault", name=vault.name)
                )

                def zip_cb(current, total, cur_file):
                    pct = 15.0 + (current / max(total, 1)) * 35.0
                    self._update_progress(
                        current_base_percent + pct * step_progress_weight,
                        tr("sync_compressing_file", current=current, total=total, file=Path(cur_file).name)
                    )

                temp_zip, total_files, zip_size = VaultManager.create_vault_zip_snapshot(
                    vault_name=vault.name,
                    vault_path=vault_path,
                    exclusions=exclusions,
                    progress_callback=zip_cb
                )

                # 3. Subida a Google Drive
                self._log(tr(
                    "sync_uploading_file",
                    name=temp_zip.name,
                    size=f"{zip_size / 1024 / 1024:.2f}"
                ))

                def upload_cb(progress, uploaded_bytes, total_bytes):
                    pct = 50.0 + (progress * 40.0)
                    mb_up = uploaded_bytes / (1024 * 1024)
                    mb_tot = total_bytes / (1024 * 1024)
                    self._update_progress(
                        current_base_percent + pct * step_progress_weight,
                        tr(
                            "sync_uploading_progress",
                            uploaded=f"{mb_up:.1f}",
                            total=f"{mb_tot:.1f}",
                            percent=int(progress * 100)
                        )
                    )

                upload_res = self.gdrive.upload_file_resumable(
                    local_path=temp_zip,
                    parent_id=vault_folder_id,
                    mime_type="application/zip",
                    progress_callback=upload_cb
                )

                # 4. Gestión de retención (mantener últimos N)
                deleted_old = self.gdrive.apply_retention_policy(
                    folder_id=vault_folder_id,
                    vault_name=vault.name,
                    keep_count=vault.retention_count
                )
                if deleted_old > 0:
                    self._log(tr("sync_retention_cleanup", count=deleted_old))

                duration = time.time() - start_time
                vault.last_status = "success"
                vault.last_sync = datetime.now().isoformat()
                vault.last_error = None
                self.config_manager.update_vault(vault)

                success_msg = tr(
                    "sync_success_message",
                    files=total_files,
                    size=f"{zip_size / 1024 / 1024:.2f}",
                    duration=f"{duration:.1f}"
                )
                self._log(f"OK: {vault.name} -> {success_msg}")
                self._record_history(vault, "success", total_files, zip_size, duration, success_msg)

                return {
                    "vault": vault.name,
                    "status": "success",
                    "files": total_files,
                    "size_bytes": zip_size,
                    "duration": duration,
                    "drive_file_id": upload_res.get("id")
                }

            # 2b. Modo Mirror (subida directa de archivos y carpetas)
            return self._sync_mirror_vault(
                vault=vault,
                vault_path=vault_path,
                vault_folder_id=vault_folder_id,
                exclusions=exclusions,
                start_time=start_time,
                step_progress_weight=step_progress_weight,
                current_base_percent=current_base_percent,
            )

        except Exception as e:
            duration = time.time() - start_time
            err_msg = tr("sync_error_generic", error=str(e))
            logger.exception(err_msg)
            self._log(tr("sync_error_vault_prefix", name=vault.name, error=err_msg))
            vault.last_status = "failed"
            vault.last_error = str(e)
            self.config_manager.update_vault(vault)
            self._record_history(vault, "failed", 0, 0, duration, err_msg)
            return {"vault": vault.name, "status": "failed", "error": str(e)}

        finally:
            # Limpiar archivo temporal .zip
            if temp_zip and temp_zip.exists():
                try:
                    temp_zip.unlink()
                except Exception as e:
                    logger.debug(f"No se pudo borrar zip temporal {temp_zip}: {e}")

    def _sync_mirror_vault(
        self,
        vault: VaultConfig,
        vault_path: Path,
        vault_folder_id: str,
        exclusions: List[str],
        start_time: float,
        step_progress_weight: float,
        current_base_percent: float,
    ) -> Dict[str, Any]:
        """Sube la estructura de archivos del vault directamente a Drive (modo Mirror)."""
        try:
            files, total_size = VaultManager.scan_vault(vault_path, exclusions)
            total_files = len(files)
            uploaded_files = 0

            for index, file_path in enumerate(files, 1):
                if self._is_cancelled:
                    self._log(tr("sync_cancelled"))
                    break

                rel_path = file_path.relative_to(vault_path)
                parent_id = vault_folder_id

                # Crear (o reutilizar) las carpetas intermedias en Google Drive
                for part in rel_path.parent.parts:
                    if part not in (".", ""):
                        parent_id = self.gdrive.get_or_create_folder(part, parent_id=parent_id)

                percent = 10.0 + (index / max(total_files, 1)) * 85.0
                file_size_mb = file_path.stat().st_size / (1024 * 1024)
                self._update_progress(
                    current_base_percent + percent * step_progress_weight,
                    tr("sync_uploading_file", name=rel_path.as_posix(), size=f"{file_size_mb:.2f}")
                )
                self.gdrive.upload_file_resumable(
                    local_path=file_path,
                    parent_id=parent_id,
                    custom_name=file_path.name
                )
                uploaded_files += 1

            duration = time.time() - start_time
            vault.last_status = "success"
            vault.last_sync = datetime.now().isoformat()
            vault.last_error = None
            self.config_manager.update_vault(vault)

            success_msg = tr(
                "sync_success_message",
                files=uploaded_files,
                size=f"{total_size / 1024 / 1024:.2f}",
                duration=f"{duration:.1f}"
            )
            self._log(f"OK: {vault.name} -> {success_msg}")
            self._record_history(
                vault, "success", uploaded_files, total_size, duration, success_msg
            )

            return {
                "vault": vault.name,
                "status": "success",
                "files": uploaded_files,
                "size_bytes": total_size,
                "duration": duration,
            }

        except Exception as e:
            duration = time.time() - start_time
            err_msg = tr("sync_error_generic", error=str(e))
            logger.exception(err_msg)
            self._log(tr("sync_error_vault_prefix", name=vault.name, error=err_msg))
            vault.last_status = "failed"
            vault.last_error = str(e)
            self.config_manager.update_vault(vault)
            self._record_history(vault, "failed", 0, 0, duration, err_msg)
            return {"vault": vault.name, "status": "failed", "error": str(e)}

    def _record_history(
        self,
        vault: VaultConfig,
        status: str,
        files_count: int,
        size_bytes: int,
        duration: float,
        message: str
    ):
        record = SyncHistoryRecord(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            vault_name=vault.name,
            status=status,
            mode=vault.backup_mode,
            files_count=files_count,
            size_bytes=size_bytes,
            duration_seconds=round(duration, 2),
            message=message
        )
        self.config_manager.add_history_record(record)

