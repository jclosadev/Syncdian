"""
Sistema de internacionalización (i18n) para Syncdian.

Todos los textos visibles de la aplicación (interfaz, diálogos, bandeja del
sistema, notificaciones y consola) están centralizados aquí en Español e Inglés.
El idioma se cambia en tiempo real desde la sección "Acerca de".
"""

from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "es": {
        # ------------------------------------------------------------
        # Comunes
        # ------------------------------------------------------------
        "loading": "Cargando...",
        "preparing": "Preparando...",
        "verifying": "Verificando...",
        "connected": "Conectado",
        "disconnected": "Desconectado",
        "never": "Nunca",
        "cancel": "Cancelar",
        "save": "Guardar",
        "ok": "Aceptar",
        "state_on": "Activado",
        "state_off": "Desactivado",
        "app_tagline": "Sincronización de Obsidian con Google Drive",

        # ------------------------------------------------------------
        # Barra lateral y búsqueda
        # ------------------------------------------------------------
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

        # ------------------------------------------------------------
        # Panel principal
        # ------------------------------------------------------------
        "dash_title": "Sincronización y Estado",
        "dash_sync_title": "Copia y Sincronización Inmediata",
        "dash_sync_desc": "Empaqueta tus bóvedas activas de Obsidian y sube los cambios a tu nube de Google Drive.",
        "dash_sync_link": "Ver detalles de la última copia de seguridad.",
        "dash_sync_btn": "Sincronizar Ahora",
        "dash_syncing_btn": "Sincronizando...",
        "dash_next_title": "Próxima Sincronización Automática",
        "dash_next_desc": "El servicio en segundo plano se ejecutará automáticamente a la hora prevista sin interrumpirte.",
        "dash_drive_title": "Estado de Google Drive",
        "dash_drive_desc": "Almacenamiento seguro en tu nube personal con control de versiones.",
        "dash_vaults_title": "Bóvedas Vinculadas",
        "dash_manage_vaults": "Gestionar Bóvedas",
        "dash_next_today": "Hoy a las {time}",
        "dash_next_date": "{date} a las {time}",
        "dash_schedule_disabled": "Programación desactivada",
        "dash_schedule_not_set": "No programado",
        "dash_drive_connected": "Conectado",
        "dash_drive_disconnected": "Desconectado",
        "dash_drive_email": " ({email})",
        "dash_sync_done": "Sincronización finalizada.",
        "table_name": "Nombre",
        "table_path": "Ruta Local",
        "table_last_sync": "Última Sincronización",
        "table_status": "Estado",
        "status_success": "Completado",
        "status_failed": "Fallido",
        "status_running": "En curso",
        "status_never": "Pendiente",

        # ------------------------------------------------------------
        # Bóvedas de Obsidian
        # ------------------------------------------------------------
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
        "vault_saved_versions": "{count} versiones guardadas",
        "vault_path_prefix": "Ruta: {path}",
        "vault_mode_prefix": "Modo: {mode}",
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
        "dlg_name_placeholder": "Ej: Mis Notas Personales",
        "dlg_path_placeholder": "C:\\Ruta\\A\\Tu\\Vault",
        "dlg_name_hint": "Etiqueta identificativa",
        "dlg_path_hint": "Ubicación local en tu disco",
        "dlg_mode_hint": "Estrategia de copia en Google Drive",
        "dlg_retention_hint": "Elimina automáticamente las copias más antiguas",
        "dlg_active_hint": "Habilita la copia para esta bóveda",
        "dlg_mode_zip_option": "Snapshots ZIP con versiones (Recomendado)",
        "dlg_mode_mirror_option": "Mirror de archivos directos",
        "dlg_select_folder_title": "Seleccionar carpeta de la bóveda",
        "dlg_name_required_title": "Aviso",
        "dlg_name_required_msg": "Por favor ingresa un nombre para la bóveda.",
        "dlg_path_invalid_msg": "La ruta especificada no existe en tu equipo.",
        "dlg_delete_title": "Confirmar eliminación",
        "dlg_delete_msg": "¿Deseas desvincular '{name}' de Syncdian?\n(Tus notas y copias en Drive NO se eliminarán).",
        "vaults_autodetect_none_title": "Auto-detección",
        "vaults_autodetect_none_msg": "No se encontraron bóvedas registradas en Obsidian.",
        "vaults_autodetect_added_title": "Bóvedas detectadas",
        "vaults_autodetect_added_msg": "Se han importado {count} bóveda(s) de Obsidian.",
        "vaults_autodetect_existing_msg": "Todas tus bóvedas ya estaban agregadas.",

        # ------------------------------------------------------------
        # Programación
        # ------------------------------------------------------------
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
        "sched_saved_title": "Programación guardada",
        "sched_saved_msg": "La programación ha sido actualizada y aplicada al servicio en segundo plano.",

        # ------------------------------------------------------------
        # Google Drive
        # ------------------------------------------------------------
        "gdrive_title": "Google Drive",
        "gdrive_acc_title": "Cuenta de Google Drive Vinculada",
        "gdrive_acc_desc": "Sesión activa como: {email}",
        "gdrive_disconnect": "Desconectar Cuenta",
        "gdrive_api_scope": "Google Drive API conectada de forma segura (ámbito: drive.file).",
        "gdrive_storage_title": "Espacio de Almacenamiento",
        "gdrive_storage_desc": "Uso actual de almacenamiento en tu cuenta de Google Drive.",
        "gdrive_storage_of": "{used} GB de {total} GB",
        "gdrive_storage_used": "{used} GB usados",
        "gdrive_storage_available": "Disponible",
        "gdrive_account_connected": "Cuenta conectada",
        "gdrive_folder_title": "Carpeta Destino en Drive",
        "gdrive_folder_desc": "Nombre de la carpeta principal creada en tu Google Drive donde se guardarán las bóvedas.",
        "gdrive_save_folder": "Guardar",
        "gdrive_json_title": "Vincular con credentials.json",
        "gdrive_json_desc": "Carga el archivo de credenciales de escritorio descargado de Google Cloud Console.",
        "gdrive_json_link": "Opción recomendada y más rápida.",
        "gdrive_json_placeholder": "Ruta a credentials.json...",
        "gdrive_connect_btn": "Conectar",
        "gdrive_keys_title": "Vincular con Client ID y Secret",
        "gdrive_keys_desc": "Ingresa manualmente tus identificadores de cliente de OAuth.",
        "gdrive_keys_btn": "Iniciar Sesión con Claves",
        "gdrive_guide_title": "Pasos para obtener tus credenciales en Google Cloud Console:",
        "gdrive_guide_steps": (
            "1. Abre <a style='color:#e2a01b;' href='https://console.cloud.google.com/'>Google Cloud Console</a> "
            "y crea un proyecto llamado <b>Syncdian</b>.<br>"
            "2. En <b>Biblioteca de APIs</b>, busca y activa <b>Google Drive API</b>.<br>"
            "3. En <b>Pantalla de consentimiento de OAuth</b>, elige 'Externo' y añade tu correo en 'Usuarios de prueba'.<br>"
            "4. En <b>Credenciales</b>, pulsa <b>+ Crear credenciales</b> &gt; <b>ID de cliente de OAuth</b> "
            "y selecciona <b>App de escritorio</b>.<br>"
            "5. Descarga el JSON o copia tus claves, selecciona el archivo arriba y pulsa <b>Conectar</b>."
        ),
        "gdrive_browse_json_title": "Seleccionar credentials.json",
        "gdrive_json_filter": "Archivos JSON (*.json);;Todos los archivos (*.*)",
        "gdrive_invalid_json_title": "Aviso",
        "gdrive_invalid_json_msg": "Por favor selecciona un archivo credentials.json válido.",
        "gdrive_missing_keys_title": "Aviso",
        "gdrive_missing_keys_msg": "Por favor ingresa Client ID y Client Secret.",
        "gdrive_auth_title": "Autenticación con Google",
        "gdrive_auth_msg": "Se abrirá tu navegador para que inicies sesión en Google y autorices a Syncdian.",
        "gdrive_auth_success_title": "¡Conexión exitosa!",
        "gdrive_auth_success_msg": "Google Drive vinculado exitosamente con:\n{email}",
        "gdrive_auth_error_title": "Error de conexión",
        "gdrive_auth_error_msg": "No se pudo completar la conexión:\n{error}",
        "gdrive_disconnect_title": "Desconectar",
        "gdrive_disconnect_msg": "¿Deseas desconectar tu cuenta de Google Drive?",
        "gdrive_updated_title": "Actualizado",
        "gdrive_folder_saved": "Nombre de la carpeta destino guardado.",
        "gdrive_user_default": "Usuario",

        # ------------------------------------------------------------
        # Historial y consola
        # ------------------------------------------------------------
        "hist_title": "Historial de Respaldos y Consola",
        "hist_export": "Exportar Logs",
        "hist_clear": "Limpiar",
        "hist_col_date": "Fecha y Hora",
        "hist_col_vault": "Bóveda",
        "hist_col_status": "Estado",
        "hist_col_files": "Archivos",
        "hist_col_size": "Tamaño",
        "hist_col_details": "Detalle",
        "hist_clear_title": "Limpiar historial",
        "hist_clear_msg": "¿Seguro que deseas vaciar el historial?",
        "hist_export_title": "Guardar logs",
        "hist_default_filename": "syncdian_log.txt",
        "hist_export_filter": "Archivos de texto (*.txt);;Todos los archivos (*.*)",
        "hist_exported_title": "Exportado",
        "hist_exported_msg": "Logs guardados correctamente.",
        "hist_export_error_title": "Error",
        "hist_export_error_msg": "No se pudo guardar: {error}",

        # ------------------------------------------------------------
        # Ajustes generales
        # ------------------------------------------------------------
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
        "set_excl_placeholder": "Ej: .trash, *.tmp, .git",
        "set_autostart_error_title": "Aviso",
        "set_autostart_error_msg": "No se pudo modificar el registro de inicio de Windows.",

        # ------------------------------------------------------------
        # Acerca de
        # ------------------------------------------------------------
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
        "about_up_to_date_title": "Actualizaciones",
        "about_up_to_date_msg": "¡Syncdian v{version} está actualizado!\nTienes la versión más reciente instalada.",
        "about_path_not_exist_title": "Syncdian",
        "about_path_not_exist_msg": "La ruta {path} no existe.",
        "about_no_vaults_title": "Syncdian",
        "about_no_vaults_msg": "No hay bóvedas configuradas.",

        # ------------------------------------------------------------
        # Bandeja del sistema
        # ------------------------------------------------------------
        "tray_open": "Abrir Syncdian",
        "tray_sync_now": "Sincronizar Ahora",
        "tray_pause_sched": "Pausar Programación",
        "tray_resume_sched": "Reanudar Programación",
        "tray_quit": "Salir de Syncdian",
        "tray_still_running_title": "Syncdian sigue activo",
        "tray_still_running_msg": "Syncdian continuará ejecutándose en segundo plano para realizar tus copias programadas.",
        "tray_sync_success": "Copia de seguridad completada con éxito en Google Drive.",
        "tray_sync_failed": "No se pudo completar la copia de seguridad.",
        "tray_next_tooltip": "Próxima copia: {time}",

        # ------------------------------------------------------------
        # Avisos de la ventana principal
        # ------------------------------------------------------------
        "msg_gdrive_required_title": "Google Drive",
        "msg_gdrive_required_msg": "Conecta tu cuenta de Google Drive para comenzar a sincronizar.",
        "msg_no_vaults_title": "Syncdian",
        "sync_error_unknown": "Error desconocido",

        # ------------------------------------------------------------
        # Motor de sincronización (consola)
        # ------------------------------------------------------------
        "sync_no_vaults": "No hay ninguna bóveda de Obsidian configurada o habilitada para sincronizar.",
        "sync_not_authenticated": "Google Drive no está conectado o la sesión ha expirado.",
        "sync_starting": "Iniciando sincronización de {count} bóveda(s)...",
        "sync_processing_vault": "--- Procesando bóveda [{current}/{total}]: {name} ---",
        "sync_finished": "Sincronización finalizada.",
        "sync_cancelled": "Sincronización cancelada por el usuario.",
        "sync_verifying_folder": "Verificando carpeta en Google Drive ({name})...",
        "sync_compressing_vault": "Comprimiendo bóveda '{name}'...",
        "sync_compressing_file": "Comprimiendo [{current}/{total}]: {file}",
        "sync_uploading_file": "Subiendo {name} ({size} MB) a Google Drive...",
        "sync_uploading_progress": "Subiendo a Google Drive: {uploaded} MB / {total} MB ({percent}%)",
        "sync_retention_cleanup": "Política de retención: se limpiaron {count} copias antiguas.",
        "sync_success_message": "Copia completada con éxito ({files} archivos, {size} MB en {duration}s)",
        "sync_error_vault_missing": "La carpeta de la bóveda '{path}' no existe en el disco.",
        "sync_error_generic": "Error durante la sincronización: {error}",
        "sync_error_vault_prefix": "ERROR en {name}: {error}",
    },
    "en": {
        # ------------------------------------------------------------
        # Common
        # ------------------------------------------------------------
        "loading": "Loading...",
        "preparing": "Preparing...",
        "verifying": "Verifying...",
        "connected": "Connected",
        "disconnected": "Disconnected",
        "never": "Never",
        "cancel": "Cancel",
        "save": "Save",
        "ok": "OK",
        "state_on": "On",
        "state_off": "Off",
        "app_tagline": "Obsidian to Google Drive sync",

        # ------------------------------------------------------------
        # Sidebar and search
        # ------------------------------------------------------------
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

        # ------------------------------------------------------------
        # Dashboard
        # ------------------------------------------------------------
        "dash_title": "Sync & Status",
        "dash_sync_title": "Immediate Backup & Sync",
        "dash_sync_desc": "Package your active Obsidian vaults and upload changes to your Google Drive cloud.",
        "dash_sync_link": "View details of the last backup.",
        "dash_sync_btn": "Sync Now",
        "dash_syncing_btn": "Syncing...",
        "dash_next_title": "Next Scheduled Sync",
        "dash_next_desc": "The background service will automatically run at the scheduled time without interrupting you.",
        "dash_drive_title": "Google Drive Status",
        "dash_drive_desc": "Secure cloud storage in your personal drive with version control.",
        "dash_vaults_title": "Linked Vaults",
        "dash_manage_vaults": "Manage Vaults",
        "dash_next_today": "Today at {time}",
        "dash_next_date": "{date} at {time}",
        "dash_schedule_disabled": "Schedule disabled",
        "dash_schedule_not_set": "Not scheduled",
        "dash_drive_connected": "Connected",
        "dash_drive_disconnected": "Disconnected",
        "dash_drive_email": " ({email})",
        "dash_sync_done": "Sync completed.",
        "table_name": "Name",
        "table_path": "Local Path",
        "table_last_sync": "Last Backup",
        "table_status": "Status",
        "status_success": "Success",
        "status_failed": "Failed",
        "status_running": "In progress",
        "status_never": "Pending",

        # ------------------------------------------------------------
        # Obsidian vaults
        # ------------------------------------------------------------
        "vaults_title": "Obsidian Vaults",
        "vaults_autodetect_title": "Auto-detect Obsidian Vaults",
        "vaults_autodetect_desc": "Reads the official Obsidian configuration on your machine and imports your vaults automatically.",
        "vaults_autodetect_btn": "Auto-detect",
        "vaults_add_title": "Add New Vault",
        "vaults_add_desc": "Manually specify a local notes folder to back up to Google Drive.",
        "vaults_add_btn": "Add Manually",
        "vaults_empty": "No vaults configured yet.\nClick 'Auto-detect' or 'Add Manually' to get started.",
        "vault_mode_zip": "ZIP Snapshots",
        "vault_mode_mirror": "Mirror",
        "vault_edit": "Edit",
        "vault_delete": "Delete",
        "vault_saved_versions": "{count} versions saved",
        "vault_path_prefix": "Path: {path}",
        "vault_mode_prefix": "Mode: {mode}",
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
        "dlg_name_placeholder": "e.g. My Personal Notes",
        "dlg_path_placeholder": "C:\\Path\\To\\Your\\Vault",
        "dlg_name_hint": "Display name",
        "dlg_path_hint": "Local folder on your disk",
        "dlg_mode_hint": "Backup strategy on Google Drive",
        "dlg_retention_hint": "Automatically removes the oldest backups",
        "dlg_active_hint": "Enables backups for this vault",
        "dlg_mode_zip_option": "ZIP snapshots with versions (Recommended)",
        "dlg_mode_mirror_option": "Direct file mirror",
        "dlg_select_folder_title": "Select vault folder",
        "dlg_name_required_title": "Notice",
        "dlg_name_required_msg": "Please enter a name for the vault.",
        "dlg_path_invalid_msg": "The specified path does not exist on your computer.",
        "dlg_delete_title": "Confirm removal",
        "dlg_delete_msg": "Do you want to unlink '{name}' from Syncdian?\n(Your notes and Google Drive backups will NOT be deleted).",
        "vaults_autodetect_none_title": "Auto-detection",
        "vaults_autodetect_none_msg": "No vaults registered in Obsidian were found.",
        "vaults_autodetect_added_title": "Vaults detected",
        "vaults_autodetect_added_msg": "{count} Obsidian vault(s) imported.",
        "vaults_autodetect_existing_msg": "All your vaults were already added.",

        # ------------------------------------------------------------
        # Scheduling
        # ------------------------------------------------------------
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
        "sched_saved_title": "Schedule saved",
        "sched_saved_msg": "The schedule has been updated and applied to the background service.",

        # ------------------------------------------------------------
        # Google Drive
        # ------------------------------------------------------------
        "gdrive_title": "Google Drive",
        "gdrive_acc_title": "Linked Google Drive Account",
        "gdrive_acc_desc": "Active session as: {email}",
        "gdrive_disconnect": "Disconnect Account",
        "gdrive_api_scope": "Google Drive API connected securely (scope: drive.file).",
        "gdrive_storage_title": "Storage Space",
        "gdrive_storage_desc": "Current storage usage in your Google Drive account.",
        "gdrive_storage_of": "{used} GB of {total} GB",
        "gdrive_storage_used": "{used} GB used",
        "gdrive_storage_available": "Available",
        "gdrive_account_connected": "Account connected",
        "gdrive_folder_title": "Target Folder in Drive",
        "gdrive_folder_desc": "Name of the main folder created in your Google Drive to store vaults.",
        "gdrive_save_folder": "Save",
        "gdrive_json_title": "Link with credentials.json",
        "gdrive_json_desc": "Load the desktop credentials file downloaded from Google Cloud Console.",
        "gdrive_json_link": "Recommended and fastest option.",
        "gdrive_json_placeholder": "Path to credentials.json...",
        "gdrive_connect_btn": "Connect",
        "gdrive_keys_title": "Link with Client ID & Secret",
        "gdrive_keys_desc": "Manually enter your OAuth client identifiers.",
        "gdrive_keys_btn": "Sign in with Keys",
        "gdrive_guide_title": "Steps to get your credentials in Google Cloud Console:",
        "gdrive_guide_steps": (
            "1. Open <a style='color:#e2a01b;' href='https://console.cloud.google.com/'>Google Cloud Console</a> "
            "and create a project named <b>Syncdian</b>.<br>"
            "2. In <b>API Library</b>, search for and enable <b>Google Drive API</b>.<br>"
            "3. In <b>OAuth consent screen</b>, choose 'External' and add your email under 'Test users'.<br>"
            "4. In <b>Credentials</b>, click <b>+ Create credentials</b> &gt; <b>OAuth client ID</b> "
            "and select <b>Desktop app</b>.<br>"
            "5. Download the JSON or copy your keys, select the file above and click <b>Connect</b>."
        ),
        "gdrive_browse_json_title": "Select credentials.json",
        "gdrive_json_filter": "JSON files (*.json);;All files (*.*)",
        "gdrive_invalid_json_title": "Notice",
        "gdrive_invalid_json_msg": "Please select a valid credentials.json file.",
        "gdrive_missing_keys_title": "Notice",
        "gdrive_missing_keys_msg": "Please enter the Client ID and Client Secret.",
        "gdrive_auth_title": "Google authentication",
        "gdrive_auth_msg": "Your browser will open so you can sign in to Google and authorize Syncdian.",
        "gdrive_auth_success_title": "Connection successful!",
        "gdrive_auth_success_msg": "Google Drive linked successfully with:\n{email}",
        "gdrive_auth_error_title": "Connection error",
        "gdrive_auth_error_msg": "Could not complete the connection:\n{error}",
        "gdrive_disconnect_title": "Disconnect",
        "gdrive_disconnect_msg": "Do you want to disconnect your Google Drive account?",
        "gdrive_updated_title": "Updated",
        "gdrive_folder_saved": "Target folder name saved.",
        "gdrive_user_default": "User",

        # ------------------------------------------------------------
        # History and console
        # ------------------------------------------------------------
        "hist_title": "Backup History & Console",
        "hist_export": "Export Logs",
        "hist_clear": "Clear",
        "hist_col_date": "Date & Time",
        "hist_col_vault": "Vault",
        "hist_col_status": "Status",
        "hist_col_files": "Files",
        "hist_col_size": "Size",
        "hist_col_details": "Details",
        "hist_clear_title": "Clear history",
        "hist_clear_msg": "Are you sure you want to clear the history?",
        "hist_export_title": "Save logs",
        "hist_default_filename": "syncdian_log.txt",
        "hist_export_filter": "Text files (*.txt);;All files (*.*)",
        "hist_exported_title": "Exported",
        "hist_exported_msg": "Logs saved successfully.",
        "hist_export_error_title": "Error",
        "hist_export_error_msg": "Could not save: {error}",

        # ------------------------------------------------------------
        # General settings
        # ------------------------------------------------------------
        "set_title": "Application Settings",
        "set_win_autostart_title": "Start with Windows in Background",
        "set_win_autostart_desc": "Launches Syncdian automatically and minimized when starting your computer.",
        "set_tray_title": "Minimize to System Tray",
        "set_tray_desc": "Closing the main window hides Syncdian in the notification area to keep running.",
        "set_notify_title": "Desktop Notifications",
        "set_notify_desc": "Shows system notifications when a scheduled backup completes or fails.",
        "set_excl_title": "Exclusion Filters",
        "set_excl_desc": "Files and folders matching these patterns will not be uploaded to Google Drive:",
        "set_excl_reset": "Reset",
        "set_excl_add": "Add",
        "set_excl_del": "Remove",
        "set_excl_placeholder": "e.g. .trash, *.tmp, .git",
        "set_autostart_error_title": "Notice",
        "set_autostart_error_msg": "Could not modify the Windows startup registry entry.",

        # ------------------------------------------------------------
        # About
        # ------------------------------------------------------------
        "about_version_title": "Version {version}",
        "about_version_desc": "Syncdian Desktop Background Service for Obsidian.",
        "about_version_link": "Read the changelog.",
        "about_check_updates": "Check for updates",
        "about_vault_title": "Detected Obsidian Vault",
        "about_vault_desc": "Active path: {path}",
        "about_vault_link": "Learn more about restoring note backups.",
        "about_open_folder": "Open Folder",
        "about_startup_check_title": "Automatic startup check",
        "about_startup_check_desc": "Silently verifies the Google Drive connection status when the service starts.",
        "about_lang_title": "Interface Language",
        "about_lang_desc": "Select the language displayed in Syncdian.",
        "about_lang_link": "Change language instantly.",
        "about_up_to_date_title": "Updates",
        "about_up_to_date_msg": "Syncdian v{version} is up to date!\nYou have the latest version installed.",
        "about_path_not_exist_title": "Syncdian",
        "about_path_not_exist_msg": "Path {path} does not exist.",
        "about_no_vaults_title": "Syncdian",
        "about_no_vaults_msg": "No vaults configured.",

        # ------------------------------------------------------------
        # System tray
        # ------------------------------------------------------------
        "tray_open": "Open Syncdian",
        "tray_sync_now": "Sync Now",
        "tray_pause_sched": "Pause Schedule",
        "tray_resume_sched": "Resume Schedule",
        "tray_quit": "Quit Syncdian",
        "tray_still_running_title": "Syncdian is still running",
        "tray_still_running_msg": "Syncdian will continue running in the background to perform your scheduled backups.",
        "tray_sync_success": "Backup successfully completed to Google Drive.",
        "tray_sync_failed": "Could not complete the backup to Google Drive.",
        "tray_next_tooltip": "Next backup: {time}",

        # ------------------------------------------------------------
        # Main window notices
        # ------------------------------------------------------------
        "msg_gdrive_required_title": "Google Drive",
        "msg_gdrive_required_msg": "Connect your Google Drive account to start syncing.",
        "msg_no_vaults_title": "Syncdian",
        "sync_error_unknown": "Unknown error",

        # ------------------------------------------------------------
        # Sync engine (console)
        # ------------------------------------------------------------
        "sync_no_vaults": "No Obsidian vault is configured or enabled for syncing.",
        "sync_not_authenticated": "Google Drive is not connected or the session has expired.",
        "sync_starting": "Starting sync of {count} vault(s)...",
        "sync_processing_vault": "--- Processing vault [{current}/{total}]: {name} ---",
        "sync_finished": "Sync completed.",
        "sync_cancelled": "Sync cancelled by the user.",
        "sync_verifying_folder": "Verifying folder in Google Drive ({name})...",
        "sync_compressing_vault": "Compressing vault '{name}'...",
        "sync_compressing_file": "Compressing [{current}/{total}]: {file}",
        "sync_uploading_file": "Uploading {name} ({size} MB) to Google Drive...",
        "sync_uploading_progress": "Uploading to Google Drive: {uploaded} MB / {total} MB ({percent}%)",
        "sync_retention_cleanup": "Retention policy: cleaned up {count} old backups.",
        "sync_success_message": "Backup completed successfully ({files} files, {size} MB in {duration}s)",
        "sync_error_vault_missing": "The vault folder '{path}' does not exist on disk.",
        "sync_error_generic": "Error during synchronization: {error}",
        "sync_error_vault_prefix": "ERROR in {name}: {error}",
    },
}

_CURRENT_LANGUAGE = "es"


def get_current_language() -> str:
    return _CURRENT_LANGUAGE


def set_current_language(lang_code: str):
    global _CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        _CURRENT_LANGUAGE = lang_code


def available_languages() -> Dict[str, str]:
    """Devuelve los idiomas disponibles con su nombre nativo."""
    return {"es": "Español", "en": "English"}


def tr(key: str, **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(_CURRENT_LANGUAGE, TRANSLATIONS["es"])
    text = lang_dict.get(key, TRANSLATIONS["es"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
