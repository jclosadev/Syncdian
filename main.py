#!/usr/bin/env python3
"""
Syncdian - Obsidian to Google Drive Background Sync Desktop Application.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Configurar logging antes de importar módulos de Qt
from syncdian.constants import LOG_DIR, APP_NAME, MODE_SNAPSHOT_ZIP
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOG_DIR / "syncdian.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    handlers=[
        logging.FileHandler(str(log_file), encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("syncdian")


def auto_import_existing_obsidian_vaults_if_empty():
    """Si la configuración de Syncdian está vacía, auto-detecta las bóvedas de Obsidian."""
    from syncdian.config import get_config
    from syncdian.core.vault_manager import VaultManager

    cfg = get_config()
    if not cfg.vaults:
        detected = VaultManager.detect_obsidian_vaults()
        for item in detected:
            if item.get("exists", False):
                cfg.add_vault(
                    name=item["name"],
                    path=item["path"],
                    backup_mode=MODE_SNAPSHOT_ZIP
                )
                logger.info(f"Bóveda auto-detectada e importada: {item['name']} ({item['path']})")


def main():
    parser = argparse.ArgumentParser(description="Syncdian - Sincronizador de Obsidian a Google Drive")
    parser.add_argument("--minimized", action="store_true", help="Iniciar minimizado en la bandeja del sistema")
    parser.add_argument("--sync-now", action="store_true", help="Ejecutar sincronización inmediata por consola")
    args = parser.parse_args()

    # Si se pide sync por consola sin interfaz gráfica
    if args.sync_now:
        logger.info("Modo ejecución directa por línea de comandos (--sync-now)")
        from syncdian.core.sync_engine import SyncEngine
        from syncdian.core.gdrive import GoogleDriveService

        gdrive = GoogleDriveService()
        if not gdrive.is_authenticated():
            print("ERROR: Google Drive no está autenticado. Inicia primero la aplicación de escritorio para vincular tu cuenta.")
            sys.exit(1)

        engine = SyncEngine(gdrive_service=gdrive)
        res = engine.sync_all_vaults()
        print(f"Resultado de sincronización: {res}")
        sys.exit(0 if res.get("status") == "done" else 1)

    # Iniciar aplicación gráfica con PySide6
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication
    from syncdian.ui.main_window import MainWindow
    from syncdian.ui.theme import DARK_THEME_QSS

    # Soporte High-DPI en Windows
    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    from PySide6.QtGui import QFont
    app.setFont(QFont("Segoe UI", 10))
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)  # Permite que la app siga viva en la bandeja del sistema
    app.setStyleSheet(DARK_THEME_QSS)

    # Auto-detectar bóvedas si es la primera vez que se ejecuta
    auto_import_existing_obsidian_vaults_if_empty()

    window = MainWindow()

    if not args.minimized:
        window.show()
    else:
        logger.info("Iniciando minimizado en segundo plano (System Tray)...")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

