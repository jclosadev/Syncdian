import tempfile
import unittest
from pathlib import Path

from syncdian.config import ConfigManager, VaultConfig
from syncdian.constants import MODE_MIRROR_SYNC
from syncdian.core.sync_engine import SyncEngine


class FakeDrive:
    """Google Drive mínimo en memoria para probar el modo Mirror sin red."""

    def __init__(self):
        self.folders = {}
        self.uploads = []
        self._next = 0

    def is_authenticated(self):
        return True

    def get_or_create_folder(self, name, parent_id=None):
        key = (parent_id, name)
        if key not in self.folders:
            self._next += 1
            self.folders[key] = f"folder_{self._next}"
        return self.folders[key]

    def upload_file_resumable(
        self, local_path, parent_id, mime_type=None,
        custom_name=None, progress_callback=None
    ):
        path = Path(local_path)
        data = path.read_bytes() if path.exists() else b""
        if progress_callback:
            progress_callback(1.0, len(data), len(data))
        self.uploads.append({
            "name": custom_name or path.name,
            "parent": parent_id,
            "bytes": len(data),
        })
        return {"id": f"file_{len(self.uploads)}"}


class TestMirrorMode(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.config = ConfigManager(self.tmp / "config.json")

        self.vault_path = self.tmp / "Vault"
        (self.vault_path / "notes" / "sub").mkdir(parents=True)
        (self.vault_path / "attach").mkdir()
        (self.vault_path / "notes" / "hello.md").write_text("hola", encoding="utf-8")
        (self.vault_path / "notes" / "sub" / "deep.md").write_text("fondo", encoding="utf-8")
        (self.vault_path / "attach" / "image.bin").write_bytes(b"\x00" * 64)
        (self.vault_path / ".git").mkdir()
        (self.vault_path / ".git" / "config").write_text("excluido", encoding="utf-8")
        (self.vault_path / ".obsidian").mkdir()
        (self.vault_path / ".obsidian" / "workspace.json").write_text("{}", encoding="utf-8")
        (self.vault_path / ".obsidian" / "app.json").write_text("{}", encoding="utf-8")

        self.vault = VaultConfig(
            id="v1",
            name="Vault",
            path=str(self.vault_path),
            backup_mode=MODE_MIRROR_SYNC,
        )
        self.config.vaults = [self.vault]
        self.drive = FakeDrive()
        self.engine = SyncEngine(gdrive_service=self.drive, log_callback=lambda _m: None)
        self.engine.config_manager = self.config

    def tearDown(self):
        self._tmp.cleanup()

    def _uploaded_names(self):
        return sorted(u["name"] for u in self.drive.uploads)

    def test_uploads_structure_and_respects_exclusions(self):
        result = self.engine.sync_all_vaults()

        self.assertEqual(result["status"], "done")
        self.assertEqual(result["results"][0]["status"], "success")
        self.assertEqual(
            self._uploaded_names(),
            ["app.json", "deep.md", "hello.md", "image.bin"],
        )
        self.assertNotIn("config", self._uploaded_names())
        self.assertNotIn("workspace.json", self._uploaded_names())

        self.assertEqual(self.config.vaults[0].last_status, "success")
        self.assertIsNone(self.config.vaults[0].last_error)
        self.assertEqual(len(self.config.history), 1)
        self.assertEqual(self.config.history[0].status, "success")
        self.assertEqual(self.config.history[0].mode, MODE_MIRROR_SYNC)

        # Las carpetas del vault se replican y no se duplican entre ejecuciones.
        folder_count = len(self.drive.folders)
        self.engine.sync_all_vaults()
        self.assertEqual(len(self.drive.folders), folder_count)

    def test_records_failure_when_vault_missing(self):
        self.vault.path = str(self.tmp / "NoExiste")
        self.config.vaults = [self.vault]

        result = self.engine.sync_all_vaults()

        self.assertEqual(result["status"], "done")
        self.assertEqual(result["results"][0]["status"], "failed")
        self.assertEqual(self.config.history[-1].status, "failed")


if __name__ == "__main__":
    unittest.main()
