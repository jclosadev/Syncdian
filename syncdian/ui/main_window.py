import logging
from datetime import datetime
from typing import List, Tuple

from PySide6.QtCore import Qt, Signal, QThread, QSize
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QLabel, QLineEdit, QPushButton, QScrollArea, QFrame, QApplication, QMessageBox,
    QButtonGroup
)

from syncdian.config import get_config
from syncdian.constants import APP_DISPLAY_NAME
from syncdian.core.gdrive import GoogleDriveService
from syncdian.core.scheduler import SchedulerService
from syncdian.core.sync_engine import SyncEngine
from syncdian.i18n import tr, set_current_language
from syncdian.ui.icons import get_clean_icon, get_icon, ICON_COLOR, ICON_COLOR_ACTIVE
from syncdian.ui.tabs.about_tab import AboutTab
from syncdian.ui.tabs.dashboard_tab import DashboardTab
from syncdian.ui.tabs.vaults_tab import VaultsTab
from syncdian.ui.tabs.schedule_tab import ScheduleTab
from syncdian.ui.tabs.gdrive_tab import GoogleDriveTab
from syncdian.ui.tabs.history_tab import HistoryTab
from syncdian.ui.tabs.settings_tab import SettingsTab
from syncdian.ui.tray_icon import SyncdianTrayIcon, create_default_app_icon

logger = logging.getLogger(__name__)

# Icono Flaticon/Lucide asociado a cada sección de la barra lateral
NAV_ICONS = {
    0: "about",
    1: "dashboard",
    2: "vaults",
    3: "schedule",
    4: "gdrive",
    5: "history",
    6: "settings",
}


class SyncWorker(QThread):
    progress = Signal(float, str)
    log = Signal(str)
    finished_sync = Signal(dict)

    def __init__(self, gdrive_service: GoogleDriveService):
        super().__init__()
        self.gdrive_service = gdrive_service
        self.engine = None

    def run(self):
        try:
            self.engine = SyncEngine(
                gdrive_service=self.gdrive_service,
                progress_callback=lambda pct, msg: self.progress.emit(pct, msg),
                log_callback=lambda msg: self.log.emit(msg)
            )
            result = self.engine.sync_all_vaults()
        except Exception as e:
            logger.exception("Fallo inesperado durante la sincronización.")
            result = {
                "status": "error",
                "message": tr("sync_error_generic", error=str(e)),
            }
        self.finished_sync.emit(result)

    def cancel(self):
        if self.engine:
            self.engine.cancel()


class MainWindow(QMainWindow):
    trigger_sync_signal = Signal()

    def __init__(self):
        super().__init__()
        self.config_manager = get_config()
        # Sincronizar idioma desde la configuración guardada
        if self.config_manager.settings.language:
            set_current_language(self.config_manager.settings.language)

        self.gdrive_service = GoogleDriveService()
        self.sync_worker = None
        self.is_syncing = False
        self._force_close = False
        # (botón, índice, clave de traducción, palabras clave de búsqueda)
        self.nav_buttons: List[Tuple[QPushButton, int, str, str]] = []

        self.setWindowTitle(APP_DISPLAY_NAME)
        self.setWindowIcon(create_default_app_icon())
        self.resize(980, 700)
        self.setMinimumSize(860, 580)

        # Servicio de programación en segundo plano
        self.scheduler_service = SchedulerService(job_func=self._on_scheduled_sync_triggered)
        self.scheduler_service.start()

        self.trigger_sync_signal.connect(self.start_sync)

        self.init_ui()
        self.init_tray()
        self.update_all_views()

        if self.config_manager.schedule.run_on_startup:
            self.start_sync()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------
    def init_ui(self):
        central_widget = QWidget(self)
        central_widget.setObjectName("centralWidget")
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. BARRA LATERAL (misma estructura que Obsidian)
        sidebar = QWidget()
        sidebar.setObjectName("sidebarWidget")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 16, 12, 16)
        sidebar_layout.setSpacing(4)

        # Buscador con icono de lupa
        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBar")
        self.search_box.setPlaceholderText(tr("search_placeholder"))
        self.search_box.setClearButtonEnabled(True)
        search_action = self.search_box.addAction(
            get_icon("search", 15, "#8f8172"), QLineEdit.LeadingPosition
        )
        if search_action:
            search_action.setToolTip(tr("search_placeholder"))
        self.search_box.textChanged.connect(self._filter_nav_items)
        sidebar_layout.addWidget(self.search_box)
        sidebar_layout.addSpacing(10)

        # Grupo de botones mutuamente excluyentes
        self.nav_btn_group = QButtonGroup(self)
        self.nav_btn_group.setExclusive(True)
        self.nav_buttons.clear()

        # Categoría Opciones
        self.lbl_opt = QLabel(tr("category_options"))
        self.lbl_opt.setObjectName("sidebarCategoryHeader")
        sidebar_layout.addWidget(self.lbl_opt)

        self._add_nav_button(sidebar_layout, "nav_about", 0, "version update updates info about")
        self._add_nav_button(sidebar_layout, "nav_dashboard", 1, "dashboard sync now status metrics panel")
        self._add_nav_button(sidebar_layout, "nav_vaults", 2, "vaults notes folders bovedas")
        self._add_nav_button(sidebar_layout, "nav_schedule", 3, "schedule recurring timer 21:00 programacion")
        self._add_nav_button(sidebar_layout, "nav_gdrive", 4, "google drive cloud account token credentials")

        sidebar_layout.addSpacing(12)

        # Categoría Sistema
        self.lbl_sys = QLabel(tr("category_system"))
        self.lbl_sys.setObjectName("sidebarCategoryHeader")
        sidebar_layout.addWidget(self.lbl_sys)

        self._add_nav_button(sidebar_layout, "nav_history", 5, "history logs records historial registros console")
        self._add_nav_button(sidebar_layout, "nav_settings", 6, "settings windows autostart tray exclusion ajustes")

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # 2. PANEL DERECHO
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("contentStack")

        self.about_tab = AboutTab(self)
        self.about_tab.language_changed.connect(self._on_language_changed)

        self.dashboard_tab = DashboardTab(self)
        self.dashboard_tab.request_sync_now.connect(self.start_sync)
        self.dashboard_tab.open_tab_requested.connect(self.select_tab)

        self.vaults_tab = VaultsTab(self)
        self.vaults_tab.vaults_changed.connect(self.update_all_views)

        self.schedule_tab = ScheduleTab(self)
        self.schedule_tab.schedule_updated.connect(self._on_schedule_updated)

        self.gdrive_tab = GoogleDriveTab(self.gdrive_service, self)
        self.gdrive_tab.connection_changed.connect(self._on_gdrive_connection_changed)

        self.history_tab = HistoryTab(self)
        self.settings_tab = SettingsTab(self)

        self.stacked_widget.addWidget(self.about_tab)       # 0
        self.stacked_widget.addWidget(self.dashboard_tab)   # 1
        self.stacked_widget.addWidget(self.vaults_tab)      # 2
        self.stacked_widget.addWidget(self.schedule_tab)    # 3
        self.stacked_widget.addWidget(self.gdrive_tab)      # 4
        self.stacked_widget.addWidget(self.history_tab)     # 5
        self.stacked_widget.addWidget(self.settings_tab)    # 6

        scroll_area = QScrollArea()
        scroll_area.setObjectName("contentScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(self.stacked_widget)
        main_layout.addWidget(scroll_area, stretch=1)

        self.setCentralWidget(central_widget)
        self.select_tab(0)

    def _add_nav_button(self, layout: QVBoxLayout, key: str, index: int, keywords: str):
        text = tr(key)
        btn = QPushButton(text.replace("&", "&&"))
        btn.setObjectName("navButton")
        btn.setCheckable(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setIcon(get_clean_icon(NAV_ICONS.get(index, "about"), 18, ICON_COLOR, ICON_COLOR_ACTIVE))
        btn.setIconSize(QSize(18, 18))
        self.nav_btn_group.addButton(btn, index)
        btn.clicked.connect(lambda: self.select_tab(index))
        layout.addWidget(btn)
        self.nav_buttons.append((btn, index, key, (text + " " + keywords).lower()))

    def select_tab(self, index: int):
        self.stacked_widget.setCurrentIndex(index)
        for btn, idx, _, _ in self.nav_buttons:
            if idx == index:
                btn.setChecked(True)
                break

    def _filter_nav_items(self, query: str):
        q = query.strip().lower()
        for btn, _, _, keywords in self.nav_buttons:
            btn.setVisible(not q or q in keywords)

    # ------------------------------------------------------------------
    # Idioma
    # ------------------------------------------------------------------
    def _on_language_changed(self, lang_code: str):
        set_current_language(lang_code)
        self.config_manager.settings.language = lang_code
        self.config_manager.save()
        self.retranslate_ui()
        self.select_tab(self.stacked_widget.currentIndex())

    def retranslate_ui(self):
        """Vuelve a aplicar todos los textos sin perder el estado de la interfaz."""
        self.search_box.setPlaceholderText(tr("search_placeholder"))
        self.lbl_opt.setText(tr("category_options"))
        self.lbl_sys.setText(tr("category_system"))

        for btn, idx, key, _ in self.nav_buttons:
            btn.setText(tr(key).replace("&", "&&"))
            btn.setIcon(get_clean_icon(
                NAV_ICONS.get(idx, "about"), 18, ICON_COLOR, ICON_COLOR_ACTIVE
            ))

        for tab in (
            self.about_tab, self.dashboard_tab, self.vaults_tab,
            self.schedule_tab, self.gdrive_tab, self.history_tab,
            self.settings_tab,
        ):
            if hasattr(tab, "retranslate"):
                tab.retranslate()

        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.retranslate_menu(self.config_manager.schedule.enabled)

        self.update_all_views()

    # ------------------------------------------------------------------
    # Bandeja del sistema
    # ------------------------------------------------------------------
    def init_tray(self):
        self.tray_icon = SyncdianTrayIcon(self)
        self.tray_icon.open_window_requested.connect(self.show_and_activate)
        self.tray_icon.sync_now_requested.connect(self.start_sync)
        self.tray_icon.toggle_schedule_requested.connect(self._toggle_schedule_from_tray)
        self.tray_icon.quit_requested.connect(self.quit_application)
        self.tray_icon.show()

    def show_and_activate(self):
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()

    def update_all_views(self):
        next_run_str = self.scheduler_service.get_next_run_formatted()
        is_connected = self.gdrive_service.is_authenticated()
        email = self.config_manager.google_drive.user_email

        self.dashboard_tab.refresh_data(next_run_str, is_connected, email)
        self.history_tab.refresh_history_table()
        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.update_tooltip(tr("tray_next_tooltip", time=next_run_str))
            self.tray_icon.retranslate_menu(self.config_manager.schedule.enabled)

    def _on_schedule_updated(self):
        self.scheduler_service.apply_schedule()
        self.update_all_views()

    def _toggle_schedule_from_tray(self):
        sched = self.config_manager.schedule
        sched.enabled = not sched.enabled
        self.config_manager.save()
        self.scheduler_service.apply_schedule()
        self.schedule_tab.toggle_enable.setChecked(sched.enabled)
        self.update_all_views()
        msg = tr("sched_auto_title") + ": " + (tr("state_on") if sched.enabled else tr("state_off"))
        self.tray_icon.notify("Syncdian", msg)

    def _on_gdrive_connection_changed(self, connected: bool):
        self.update_all_views()

    def _on_scheduled_sync_triggered(self):
        logger.info("Disparador de programación recurrente alcanzado.")
        self.trigger_sync_signal.emit()

    # ------------------------------------------------------------------
    # Sincronización
    # ------------------------------------------------------------------
    def start_sync(self):
        if self.is_syncing:
            return

        if not self.gdrive_service.is_authenticated():
            if self.isVisible():
                QMessageBox.warning(
                    self,
                    tr("msg_gdrive_required_title"),
                    tr("msg_gdrive_required_msg")
                )
                self.select_tab(4)
            else:
                self.tray_icon.notify(
                    "Syncdian",
                    f"{tr('disconnected')}: {tr('msg_gdrive_required_msg')}",
                    is_error=True
                )
            return

        enabled_vaults = [v for v in self.config_manager.vaults if v.enabled]
        if not enabled_vaults:
            if self.isVisible():
                QMessageBox.warning(
                    self,
                    tr("msg_no_vaults_title"),
                    tr("vaults_empty")
                )
                self.select_tab(2)
            return

        self.is_syncing = True
        self.dashboard_tab.set_sync_in_progress(True)
        self.history_tab.append_log(f"\n=== SYNC: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")

        self.sync_worker = SyncWorker(self.gdrive_service)
        self.sync_worker.progress.connect(self._on_sync_progress)
        self.sync_worker.log.connect(self.history_tab.append_log)
        self.sync_worker.finished_sync.connect(self._on_sync_finished)
        self.sync_worker.start()

    def _on_sync_progress(self, percent: float, message: str):
        self.dashboard_tab.update_sync_progress(percent, message)

    def _on_sync_finished(self, result: dict):
        self.is_syncing = False
        self.dashboard_tab.set_sync_in_progress(False)
        self.update_all_views()

        status = result.get("status")
        if status == "done":
            msg = tr("tray_sync_success")
            self.history_tab.append_log(f"[OK] {msg}")
            if self.config_manager.settings.notify_on_sync:
                self.tray_icon.notify("Syncdian", msg)
        else:
            err = result.get("message", tr("sync_error_unknown"))
            self.history_tab.append_log(f"[ERROR] {err}")
            if self.config_manager.settings.notify_on_sync:
                self.tray_icon.notify("Syncdian", f"{tr('tray_sync_failed')}: {err}", is_error=True)

    # ------------------------------------------------------------------
    # Cierre
    # ------------------------------------------------------------------
    def closeEvent(self, event: QCloseEvent):
        if self._force_close:
            event.accept()
            return

        if self.config_manager.settings.minimize_to_tray and self.tray_icon.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.notify(
                tr("tray_still_running_title"),
                tr("tray_still_running_msg")
            )
        else:
            self.quit_application()

    def quit_application(self):
        self._force_close = True
        self.scheduler_service.stop()
        if self.sync_worker and self.sync_worker.isRunning():
            self.sync_worker.cancel()
            self.sync_worker.wait(2000)
        if hasattr(self, "tray_icon") and self.tray_icon:
            self.tray_icon.hide()
        QApplication.quit()
