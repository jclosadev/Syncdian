"""
Sistema de internacionalización (i18n) para Syncdian.
Textos profesionales y limpios (sin emojis de móvil).
"""

from typing import Dict, Any

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "es": {
        # Sidebar y Búsqueda
        "search_placeholder": "Buscar ajustes...",
        "category_options": "OPCIONES",
        "category_system": "SISTEMA",
        "nav_about": "Acerca De",
        "nav_dashboard": "Sincronización y Estado",
        "nav_vaults": "Bóvedas de Obsidian",
        "nav_schedule": "Programación",
        "nav_gdrive": "Google Drive",
        "nav_history": "Historial y Registros",
        "nav_settings": "Ajustes Generales",

        # Dashboard
        "dash_title": "Sincronización y Estado",
        "dash_sync_title": "Copia y Sincronización Inmediata",
        "dash_sync_desc": "Empaqueta tus bóvedas activas de Obsidian y sube los cambios a tu nube de Google Drive.",
        "dash_sync_link": "Ver detalles de la última copia de seguridad.",
        "dash_sync_btn": "Sincronizar Ahora",
        "dash_syncing_btn": "Sincronizando...",
        "dash_next_title": "Próxima Sincronización Automática",
        "dash_next_desc": "El servicio en segundo plano se ejecutará automáticamente a la hora prevista sin interrumpirte.",
        "dash_drive_title": "Estado de Google Drive",
        "dash_drive_desc": "Almacenamiento seguro en tu nube personal con cifrado y control de versiones.",
        "dash_vaults_title": "Bóvedas Vinculadas",
        "dash_manage_vaults": "Gestionar Bóvedas",
        "table_name": "Nombre",
        "table_path": "Ruta Local",
        "table_last_sync": "Última Sincronización",
        "table_status": "Estado",
        "status_success": "Completado",
        "status_failed": "Fallido",
        "status_running": "En curso",
        "status_never": "Pendiente",
        "connected": "Conectado",
        "disconnected": "Desconectado",
        "never": "Nunca",

        # Bóvedas (Vaults)
        "vaults_title": "Bóvedas de Obsidian",
        "vaults_autodetect_title": "Auto-detectar Bóvedas de Obsidian",
        "vaults_autodetect_desc": "Lee la configuración oficial de Obsidian en tu equipo e importa automáticamente tus bóvedas.",
        "vaults_autodetect_btn": "Auto-detectar",
        "vaults_add_title": "Añadir Nueva Bóveda",
        "vaults_add_desc": "Especifica manualmente una ruta local de notas para respaldarla en Google Drive.",
        "vaults_add_btn": "Añadir Manualmente",
        "vaults_empty": "No hay bóvedas configuradas aún.\nHaz clic en 'Auto-detectar' o 'Añadir Manualmente' para comenzar.",
        "vault_mode_zip": "Snapshots ZIP",
        "vault_mode_mirror": "Mirror",
        "vault_edit": "Editar",
        "vault_delete": "Eliminar",
        "vault_saved_versions": "versiones guardadas",
        "dlg_add_vault": "Añadir Nueva Bóveda",
        "dlg_edit_vault": "Configurar Bóveda de Obsidian",
        "dlg_vault_name": "Nombre de la Bóveda",
        "dlg_vault_path": "Ruta de la Carpeta",
        "dlg_browse": "Examinar...",
        "dlg_backup_mode": "Modo de Respaldo",
        "dlg_retention": "Copias a conservar",
        "dlg_active": "Activar Sincronización",
        "dlg_save": "Guardar Bóveda",
        "dlg_cancel": "Cancelar",

        # Programación (Schedule)
        "sched_title": "Programación Recurrente",
        "sched_auto_title": "Sincronización Automática Programada",
        "sched_auto_desc": "Si lo desactiva, el servicio en segundo plano pausará las copias recurrentes.",
        "sched_time_title": "Hora de Copia Diaria Recurrente",
        "sched_time_desc": "Hora programada en la que Syncdian empaquetará y subirá tus notas a Google Drive.",
        "sched_time_link": "Por defecto configurado todos los días a las 21:00.",
        "sched_freq_title": "Frecuencia de Respaldo",
        "sched_freq_desc": "Elige entre una copia diaria única o repetición a intervalos regulares.",
        "sched_freq_daily": "Diaria (a la hora fija elegida)",
        "sched_freq_hours": "Repetir cada {h} horas",
        "sched_startup_title": "Copia Inmediata al Iniciar Syncdian",
        "sched_startup_desc": "Realiza una verificación y respaldo al abrir el programa o arrancar Windows.",
        "sched_save_btn": "Guardar Programación",
        "sched_saved_msg": "La programación ha sido actualizada y aplicada al servicio en segundo plano.",

        # Google Drive
        "gdrive_title": "Google Drive",
        "gdrive_acc_title": "Cuenta de Google Drive Vinculada",
        "gdrive_acc_desc": "Sesión activa como: {email}",
        "gdrive_disconnect": "Desconectar Cuenta",
        "gdrive_storage_title": "Espacio de Almacenamiento",
        "gdrive_storage_desc": "Uso actual de almacenamiento en tu cuenta de Google Drive.",
        "gdrive_folder_title": "Carpeta Destino en Drive",
        "gdrive_folder_desc": "Nombre de la carpeta principal creada en tu Google Drive donde se guardarán los vaults.",
        "gdrive_save_folder": "Guardar",
        "gdrive_json_title": "Vincular con credentials.json",
        "gdrive_json_desc": "Carga el archivo de credenciales de escritorio descargado de Google Cloud Console.",
        "gdrive_json_link": "Opción recomendada y más rápida.",
        "gdrive_connect_btn": "Conectar",
        "gdrive_keys_title": "Vincular con Client ID y Secret",
        "gdrive_keys_desc": "Ingresa manualmente tus identificadores de cliente de OAuth.",
        "gdrive_keys_btn": "Iniciar Sesión con Claves",

        # Historial (History)
        "hist_title": "Historial de Respaldos y Consola",
        "hist_export": "Exportar Logs",
        "hist_clear": "Limpiar",
        "hist_col_date": "Fecha y Hora",
        "hist_col_vault": "Bóveda",
        "hist_col_status": "Estado",
        "hist_col_files": "Archivos",
        "hist_col_size": "Tamaño",
        "hist_col_details": "Detalle",

        # Ajustes (Settings)
        "set_title": "Ajustes de la Aplicación",
        "set_win_autostart_title": "Iniciar con Windows en Segundo Plano",
        "set_win_autostart_desc": "Arranca Syncdian automáticamente y minimizado al encender el equipo.",
        "set_tray_title": "Minimizar a la Bandeja del Sistema",
        "set_tray_desc": "Al pulsar la 'X' para cerrar la ventana, Syncdian se oculta en el área de notificación para seguir trabajando.",
        "set_notify_title": "Notificaciones de Escritorio",
        "set_notify_desc": "Muestra avisos del sistema al completar o fallar una sincronización programada.",
        "set_excl_title": "Filtros de Exclusión",
        "set_excl_desc": "Los archivos y carpetas que coincidan con estos patrones no se subirán a Google Drive:",
        "set_excl_reset": "Restablecer",
        "set_excl_add": "Añadir",
        "set_excl_del": "Eliminar",

        # Acerca de (About)
        "about_version_title": "Versión {version}",
        "about_version_desc": "Syncdian Desktop Background Service para Obsidian.",
        "about_version_link": "Leer el registro de cambios (Changelog).",
        "about_check_updates": "Buscar actualizaciones",
        "about_vault_title": "Bóveda de Obsidian Detectada",
        "about_vault_desc": "Ruta activa: {path}",
        "about_vault_link": "Aprender más sobre cómo restaurar copias de seguridad de notas.",
        "about_open_folder": "Abrir Carpeta",
        "about_startup_check_title": "Comprobación automática al iniciar",
        "about_startup_check_desc": "Verifica silenciosamente el estado de conexión con Google Drive al arrancar el servicio.",
        "about_lang_title": "Idioma de la Interfaz",
        "about_lang_desc": "Selecciona el idioma mostrado en Syncdian.",
        "about_lang_link": "Cambiar idioma al instante.",

        # Bandeja del sistema (Tray)
        "tray_open": "Abrir Syncdian",
        "tray_sync_now": "Sincronizar Ahora",
        "tray_pause_sched": "Pausar Programación",
        "tray_resume_sched": "Reanudar Programación",
        "tray_quit": "Salir de Syncdian",
        "tray_still_running_title": "Syncdian sigue activo",
        "tray_still_running_msg": "Syncdian continuará ejecutándose en segundo plano para realizar tus copias programadas.",
        "tray_sync_success": "Copia de seguridad completada con éxito en Google Drive.",
        "tray_sync_failed": "No se pudo completar la copia de seguridad."
    },
    "en": {
        # Sidebar & Search
        "search_placeholder": "Search settings...",
        "category_options": "OPTIONS",
        "category_system": "SYSTEM",
        "nav_about": "About",
        "nav_dashboard": "Sync & Status",
        "nav_vaults": "Obsidian Vaults",
        "nav_schedule": "Scheduling",
        "nav_gdrive": "Google Drive",
        "nav_history": "History & Logs",
        "nav_settings": "General Settings",

        # Dashboard
        "dash_title": "Sync & Status",
        "dash_sync_title": "Immediate Backup & Sync",
        "dash_sync_desc": "Package your active Obsidian vaults and upload changes to your Google Drive cloud.",
        "dash_sync_link": "View backup details and logs.",
        "dash_sync_btn": "Sync Now",
        "dash_syncing_btn": "Syncing...",
        "dash_next_title": "Next Scheduled Sync",
        "dash_next_desc": "The background service will automatically run at the scheduled time without interrupting you.",
        "dash_drive_title": "Google Drive Status",
        "dash_drive_desc": "Secure cloud storage in your personal drive with encryption and versioning.",
        "dash_vaults_title": "Linked Vaults",
        "dash_manage_vaults": "Manage Vaults",
        "table_name": "Name",
        "table_path": "Local Path",
        "table_last_sync": "Last Backup",
        "table_status": "Status",
        "status_success": "Success",
        "status_failed": "Failed",
        "status_running": "In progress",
        "status_never": "Pending",
        "connected": "Connected",
        "disconnected": "Disconnected",
        "never": "Never",

        # Vaults
        "vaults_title": "Obsidian Vaults",
        "vaults_autodetect_title": "Auto-detect Obsidian Vaults",
        "vaults_autodetect_desc": "Reads the official Obsidian configuration on your machine and imports your vaults automatically.",
        "vaults_autodetect_btn": "Auto-detect",
        "vaults_add_title": "Add New Vault",
        "vaults_add_desc": "Manually specify a local notes folder to backup to Google Drive.",
        "vaults_add_btn": "Add Manually",
        "vaults_empty": "No vaults configured yet.\nClick 'Auto-detect' or 'Add Manually' to get started.",
        "vault_mode_zip": "ZIP Snapshots",
        "vault_mode_mirror": "Mirror",
        "vault_edit": "Edit",
        "vault_delete": "Delete",
        "vault_saved_versions": "versions saved",
        "dlg_add_vault": "Add New Vault",
        "dlg_edit_vault": "Configure Obsidian Vault",
        "dlg_vault_name": "Vault Name",
        "dlg_vault_path": "Folder Path",
        "dlg_browse": "Browse...",
        "dlg_backup_mode": "Backup Mode",
        "dlg_retention": "Versions to keep",
        "dlg_active": "Enable Sync",
        "dlg_save": "Save Vault",
        "dlg_cancel": "Cancel",

        # Schedule
        "sched_title": "Recurring Schedule",
        "sched_auto_title": "Automatic Scheduled Sync",
        "sched_auto_desc": "If disabled, the background service will pause all recurring backups.",
        "sched_time_title": "Daily Recurring Time",
        "sched_time_desc": "Scheduled time when Syncdian will package and upload your notes to Google Drive.",
        "sched_time_link": "Default configured every day at 21:00.",
        "sched_freq_title": "Backup Frequency",
        "sched_freq_desc": "Choose between a single daily backup or repeating at regular intervals.",
        "sched_freq_daily": "Daily (at fixed chosen time)",
        "sched_freq_hours": "Repeat every {h} hours",
        "sched_startup_title": "Immediate Backup on Syncdian Launch",
        "sched_startup_desc": "Performs a check and backup when opening the app or booting Windows.",
        "sched_save_btn": "Save Schedule",
        "sched_saved_msg": "The schedule has been updated and applied to the background service.",

        # Google Drive
        "gdrive_title": "Google Drive",
        "gdrive_acc_title": "Linked Google Drive Account",
        "gdrive_acc_desc": "Active session as: {email}",
        "gdrive_disconnect": "Disconnect Account",
        "gdrive_storage_title": "Storage Space",
        "gdrive_storage_desc": "Current storage space used in your Google Drive account.",
        "gdrive_folder_title": "Target Folder in Drive",
        "gdrive_folder_desc": "Name of the main root folder created in Google Drive to store vaults.",
        "gdrive_save_folder": "Save",
        "gdrive_json_title": "Link with credentials.json",
        "gdrive_json_desc": "Load the desktop credentials file downloaded from Google Cloud Console.",
        "gdrive_json_link": "Recommended and fastest option.",
        "gdrive_connect_btn": "Connect",
        "gdrive_keys_title": "Link with Client ID & Secret",
        "gdrive_keys_desc": "Manually enter your OAuth Client ID and Secret.",
        "gdrive_keys_btn": "Sign in with Keys",

        # History
        "hist_title": "Backup History & Console",
        "hist_export": "Export Logs",
        "hist_clear": "Clear",
        "hist_col_date": "Date & Time",
        "hist_col_vault": "Vault",
        "hist_col_status": "Status",
        "hist_col_files": "Files",
        "hist_col_size": "Size",
        "hist_col_details": "Details",

        # Settings
        "set_title": "Application Settings",
        "set_win_autostart_title": "Start with Windows in Background",
        "set_win_autostart_desc": "Launches Syncdian automatically and minimized when starting your computer.",
        "set_tray_title": "Minimize to System Tray",
        "set_tray_desc": "Closing the main window hides Syncdian in the system notification area to keep running.",
        "set_notify_title": "Desktop Notifications",
        "set_notify_desc": "Shows Windows notifications when a scheduled backup completes or fails.",
        "set_excl_title": "Exclusion Filters",
        "set_excl_desc": "Files and folders matching these patterns will not be uploaded to Google Drive:",
        "set_excl_reset": "Reset",
        "set_excl_add": "Add",
        "set_excl_del": "Remove",

        # About
        "about_version_title": "Version {version}",
        "about_version_desc": "Syncdian Desktop Background Service for Obsidian.",
        "about_version_link": "Read the changelog.",
        "about_check_updates": "Check for updates",
        "about_vault_title": "Detected Obsidian Vault",
        "about_vault_desc": "Active path: {path}",
        "about_vault_link": "Learn more about restoring note backups.",
        "about_open_folder": "Open Folder",
        "about_startup_check_title": "Automatic startup check",
        "about_startup_check_desc": "Silently verifies Google Drive connection status when the service starts.",
        "about_lang_title": "Interface Language",
        "about_lang_desc": "Select the language displayed in Syncdian.",
        "about_lang_link": "Change language instantly.",

        # Tray
        "tray_open": "Open Syncdian",
        "tray_sync_now": "Sync Now",
        "tray_pause_sched": "Pause Schedule",
        "tray_resume_sched": "Resume Schedule",
        "tray_quit": "Quit Syncdian",
        "tray_still_running_title": "Syncdian is still running",
        "tray_still_running_msg": "Syncdian will continue running in the background to perform your scheduled backups.",
        "tray_sync_success": "Backup successfully completed to Google Drive.",
        "tray_sync_failed": "Could not complete the backup to Google Drive."
    }
}

_CURRENT_LANGUAGE = "es"


def get_current_language() -> str:
    return _CURRENT_LANGUAGE


def set_current_language(lang_code: str):
    global _CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        _CURRENT_LANGUAGE = lang_code


def tr(key: str, **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(_CURRENT_LANGUAGE, TRANSLATIONS["es"])
    text = lang_dict.get(key, TRANSLATIONS["es"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
