import os
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

from syncdian.constants import APP_DISPLAY_NAME
from syncdian.i18n import tr


def create_default_app_icon() -> QIcon:
    """Retorna el icono oficial de Syncdian o genera uno por código si no existe."""
    # Buscar icon.ico o icon.png en assets o ruta frozen
    base_dir = Path(__file__).resolve().parent.parent.parent
    ico_path = base_dir / "assets" / "icon.ico"
    png_path = base_dir / "assets" / "icon.png"
    if ico_path.exists():
        return QIcon(str(ico_path))
    if png_path.exists():
        return QIcon(str(png_path))

    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Fondo redondeado ámbar cálido Obsidian
    painter.setBrush(QColor("#df9b20"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 14, 14)

    # Letra 'S' en contraste oscuro
    painter.setPen(QColor("#16110d"))
    font = QFont("Segoe UI", 30, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "S")
    painter.end()

    return QIcon(pixmap)


class SyncdianTrayIcon(QSystemTrayIcon):
    open_window_requested = Signal()
    sync_now_requested = Signal()
    toggle_schedule_requested = Signal()
    quit_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(create_default_app_icon())
        self.setToolTip(f"{APP_DISPLAY_NAME}")
        self.init_menu()
        self.activated.connect(self._on_tray_activated)

    def init_menu(self):
        self.tray_menu = QMenu()

        self.open_action = self.tray_menu.addAction(tr("tray_open"))
        self.open_action.triggered.connect(self.open_window_requested.emit)

        self.sync_action = self.tray_menu.addAction(tr("tray_sync_now"))
        self.sync_action.triggered.connect(self.sync_now_requested.emit)

        self.schedule_action = self.tray_menu.addAction(tr("tray_pause_sched"))
        self.schedule_action.triggered.connect(self.toggle_schedule_requested.emit)

        self.tray_menu.addSeparator()

        self.quit_action = self.tray_menu.addAction(tr("tray_quit"))
        self.quit_action.triggered.connect(self.quit_requested.emit)

        self.setContextMenu(self.tray_menu)

    def retranslate_menu(self, schedule_enabled: bool = True):
        self.open_action.setText(tr("tray_open"))
        self.sync_action.setText(tr("tray_sync_now"))
        self.schedule_action.setText(tr("tray_pause_sched") if schedule_enabled else tr("tray_resume_sched"))
        self.quit_action.setText(tr("tray_quit"))

    def _on_tray_activated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.open_window_requested.emit()

    def update_tooltip(self, text: str):
        self.setToolTip(f"{APP_DISPLAY_NAME}\n{text}")

    def notify(self, title: str, message: str, is_error: bool = False):
        icon = QSystemTrayIcon.Critical if is_error else QSystemTrayIcon.Information
        self.showMessage(title, message, icon, 4000)
