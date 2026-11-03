import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from syncdian.config import ConfigManager, VaultConfig
from syncdian.constants import MODE_SNAPSHOT_ZIP, SCHEDULE_DAILY, SCHEDULE_INTERVAL
from syncdian.core.vault_manager import VaultManager
from syncdian.core.scheduler import SchedulerService


class TestVaultManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.vault_path = Path(self.test_dir.name) / "TestVault"
        self.vault_path.mkdir()

        # Crear estructura de prueba
        (self.vault_path / "Note1.md").write_text("# Hola Obsidian", encoding="utf-8")
        (self.vault_path / "Subfolder").mkdir()
        (self.vault_path / "Subfolder" / "Note2.md").write_text("# Nota en subcarpeta", encoding="utf-8")
        
        # Archivos que deberían ser excluidos
        trash_dir = self.vault_path / ".trash"
        trash_dir.mkdir()
        (trash_dir / "deleted.md").write_text("basura", encoding="utf-8")

        git_dir = self.vault_path / ".git"
        git_dir.mkdir()
        (git_dir / "HEAD").write_text("ref: refs/heads/main", encoding="utf-8")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_exclusion_matching(self):
        exclusions = [".git", ".trash", ".obsidian/workspace*"]
        self.assertTrue(VaultManager.is_excluded(".git/HEAD", exclusions))
        self.assertTrue(VaultManager.is_excluded(".trash/deleted.md", exclusions))
        self.assertTrue(VaultManager.is_excluded("Subfolder/.git/config", exclusions))
        self.assertTrue(VaultManager.is_excluded(".obsidian/workspace.json", exclusions))
        self.assertFalse(VaultManager.is_excluded("Note1.md", exclusions))
        self.assertFalse(VaultManager.is_excluded("Subfolder/Note2.md", exclusions))

    def test_scan_vault(self):
        exclusions = [".git", ".trash"]
        files, total_size = VaultManager.scan_vault(self.vault_path, exclusions)
        file_names = [f.name for f in files]
        self.assertIn("Note1.md", file_names)
        self.assertIn("Note2.md", file_names)
        self.assertNotIn("deleted.md", file_names)
        self.assertNotIn("HEAD", file_names)
        self.assertEqual(len(files), 2)
        self.assertGreater(total_size, 0)

    def test_create_zip_snapshot(self):
        exclusions = [".git", ".trash"]
        zip_path, total_files, size_bytes = VaultManager.create_vault_zip_snapshot(
            vault_name="TestVault",
            vault_path=self.vault_path,
            exclusions=exclusions
        )
        self.assertTrue(zip_path.exists())
        self.assertEqual(total_files, 2)
        self.assertGreater(size_bytes, 0)

        # Verificar que el zip contiene las notas
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()
            norm_names = [n.replace("\\", "/") for n in namelist]
            self.assertIn("Note1.md", norm_names)
            self.assertIn("Subfolder/Note2.md", norm_names)
            self.assertNotIn(".trash/deleted.md", norm_names)

        # Limpiar
        if zip_path.exists():
            zip_path.unlink()


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.cfg_file = Path(self.test_dir.name) / "test_config.json"
        self.cfg = ConfigManager(config_path=self.cfg_file)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_save_and_load(self):
        self.cfg.schedule.daily_time = "21:00"
        self.cfg.schedule.mode = SCHEDULE_DAILY
        self.cfg.add_vault("Mi Vault", "C:\\Fake\\Vault")
        self.cfg.save()

        # Recargar desde archivo
        new_cfg = ConfigManager(config_path=self.cfg_file)
        self.assertEqual(new_cfg.schedule.daily_time, "21:00")
        self.assertEqual(len(new_cfg.vaults), 1)
        self.assertEqual(new_cfg.vaults[0].name, "Mi Vault")


class TestSchedulerService(unittest.TestCase):
    def test_scheduler_triggers(self):
        called = False
        def dummy_job():
            nonlocal called
            called = True

        service = SchedulerService(job_func=dummy_job)
        service.config_manager.schedule.enabled = True
        service.config_manager.schedule.mode = SCHEDULE_DAILY
        service.config_manager.schedule.daily_time = "21:00"
        service.start()

        next_run = service.get_next_run_time()
        self.assertIsNotNone(next_run)
        self.assertEqual(next_run.hour, 21)
        self.assertEqual(next_run.minute, 0)

        formatted = service.get_next_run_formatted()
        self.assertIn("21:00", formatted)

        service.stop()


if __name__ == "__main__":
    unittest.main()

