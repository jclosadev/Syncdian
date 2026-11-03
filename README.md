# Syncdian 🚀
### Sincronizador en segundo plano de Obsidian a Google Drive

**Syncdian** es una aplicación de escritorio para Windows diseñada para mantener tus notas y *vaults* de **Obsidian** respaldados de forma continua, automática y segura en **Google Drive**.

Se ejecuta silenciosamente en segundo plano (en la bandeja del sistema / *System Tray* junto al reloj de Windows) y realiza copias programadas según tus preferencias (por ejemplo, **todos los días a las 21:00** o por intervalos periódicos).

---

## ✨ Características Principales

1. **Servicio Silencioso en Segundo Plano**:
   - Vive en la bandeja del sistema (*System Tray*).
   - No interfiere con tu flujo de trabajo mientras escribes en Obsidian.
   - Si cierras la ventana principal, continúa ejecutándose en segundo plano para realizar las copias a la hora programada.

2. **Programación Recurrente Flexible**:
   - **Diaria a una hora fija**: Configurable a la hora exacta que elijas (por ejemplo, todos los días a las **21:00**).
   - **Por intervalos**: Cada 1h, 2h, 4h, 6h, 12h, 24h.
   - **Sincronización manual bajo demanda**: Botón *"Sincronizar Ahora"* para respaldar cambios al instante.

3. **Respaldos Seguros y Versionados**:
   - **Snapshots ZIP (Recomendado)**: Empaqueta tu bóveda con fecha y hora (`MiVault_2026-11-03_21-00-00.zip`). Si borras notas por error o se corrompe un archivo, puedes restaurar exactamente el estado de cualquier día anterior.
   - **Mirror Sync**: Sube los archivos y carpetas del vault directamente a Google Drive replicando su estructura, ideal para consultar tus notas desde cualquier dispositivo sin descomprimir nada.
   - **Política de Retención Automática**: Limpia automáticamente en Google Drive las copias más antiguas conservando el número de versiones que elijas (ej. últimas 10 copias) para no saturar tu espacio de almacenamiento.
   - **Filtros Inteligentes de Exclusión**: Omite por defecto archivos innecesarios como `.trash`, `.git`, memorias caché y temporales.

4. **Detección Automática de Bóvedas de Obsidian**:
   - Lee automáticamente tu configuración local de Obsidian para sugerirte y añadir tus bóvedas con un solo clic.

5. **Integración Oficial con la API de Google Drive**:
   - Flujo OAuth 2.0 seguro mediante navegador.
   - Ámbito restringido (`drive.file`): Syncdian solo tiene acceso a las copias y carpetas que crea en tu Drive, garantizando la privacidad de tus demás documentos personales.

6. **Inicio Automático con Windows**:
   - Opción para arrancar minimizado automáticamente al encender el PC.

7. **Soporte Multilingüe (Español / Inglés)**:
   - Selector de idioma en tiempo real en **Acerca De** (Español e Inglés). Al cambiarlo, todos los menús, botones, notificaciones y opciones se actualizan al instante y recuerdan tu elección.

8. **Interfaz Oscura Inspirada en Obsidian**:
   - Paleta cálida, tipografía y controles al estilo Obsidian, con iconos de línea y detalles en ámbar.

---

## 🚀 Cómo Iniciar la Aplicación

Puedes iniciar Syncdian directamente mediante su ejecutable o los accesos directos:

- **`dist\Syncdian.exe`**: Ejecutable compilado independiente de Windows listo para abrir con doble clic.
- **`Iniciar_Syncdian.bat`**: Acceso directo para iniciar la aplicación (usa el `.exe` de `dist` o Python).
- **`Iniciar_Syncdian_Consola.bat`**: Inicia la aplicación mostrando los mensajes de depuración en una ventana de consola.

O mediante línea de comandos:
```bash
.\dist\Syncdian.exe
```

---

## ☁️ Configurar la Conexión con Google Drive (Paso a Paso)

Para conectar Syncdian con tu cuenta de Google Drive necesitas tus credenciales gratuitas de la API de Google:

1. **Entra a Google Cloud Console**:
   - Ve a [https://console.cloud.google.com/](https://console.cloud.google.com/) e inicia sesión con tu cuenta de Google.
2. **Crea un Proyecto**:
   - En la barra superior, haz clic en el selector de proyectos y luego en **"Nuevo proyecto"**.
   - Nómbralo **"Syncdian"** y haz clic en **Crear**.
3. **Habilita la API de Google Drive**:
   - En el menú lateral izquierdo (☰), ve a **APIs y servicios** > **Biblioteca**.
   - Busca **"Google Drive API"**, selecciónala y pulsa **Habilitar**.
4. **Pantalla de Consentimiento de OAuth**:
   - En **APIs y servicios**, ve a **Pantalla de consentimiento de OAuth**.
   - Tipo de usuario: Selecciona **Externo** y pulsa **Crear**.
   - Rellena el *Nombre de la app* (ej. `Syncdian`) y tu correo electrónico. Pulsa *Guardar y continuar*.
   - En el paso **Usuarios de prueba**, añade tu propio correo de Gmail. Pulsa *Guardar y continuar*.
5. **Crear Credenciales de Escritorio**:
   - Ve a **APIs y servicios** > **Credenciales**.
   - Haz clic en **+ Crear credenciales** > **ID de cliente de OAuth**.
   - Tipo de aplicación: Selecciona **App de escritorio** (Desktop app).
   - Nombre: `Syncdian Desktop`.
   - Pulsa **Crear**.
6. **Vincular en Syncdian**:
   - Haz clic en **Descargar JSON** (obtendrás un archivo similar a `client_secret_xxx.json`).
   - Abre Syncdian, ve a la pestaña **Google Drive** y selecciona tu archivo JSON (o copia y pega el *Client ID* y *Client Secret*).
   - Haz clic en **"Iniciar Sesión en Google"**. Se abrirá tu navegador para aceptar los permisos.
   - ¡Listo! Tu cuenta quedará guardada y autorizada de forma permanente.

---

## 📂 ¿Cómo Restaurar una Copia de Seguridad?

1. En tu Google Drive encontrarás la carpeta llamada **`Syncdian Obsidian Backups`**.
2. Dentro habrá una carpeta para cada una de tus bóvedas.
3. Para restaurar:
   - Descarga el archivo `.zip` de la fecha que desees.
   - Descomprime el contenido en la carpeta de tu vault o en una nueva carpeta.
   - Abre Obsidian y selecciona *"Abrir carpeta como bóveda"*. ¡Todas tus notas, plugins, configuraciones y enlaces estarán intactos!

---

## 🛠️ Estructura del Proyecto

```
Syncdian/
│
├── main.py                     # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias de Python
├── Iniciar_Syncdian.bat        # Acceso directo para iniciar sin consola
├── Iniciar_Syncdian_Consola.bat# Acceso directo para iniciar con consola
├── README.md                   # Esta guía
│
├── syncdian/
│   ├── constants.py            # Rutas en AppData, ámbitos y constantes
│   ├── config.py               # Gestor de configuración persistente
│   ├── i18n.py                 # Traducciones completas Español / Inglés
│   │
│   ├── core/
│   │   ├── vault_manager.py    # Auto-detección de vaults y empaquetado ZIP
│   │   ├── gdrive.py           # Conexión oficial y subida a Google Drive API
│   │   ├── scheduler.py        # Programador recurrente en segundo plano
│   │   ├── sync_engine.py      # Motor de respaldos (Snapshot ZIP y Mirror)
│   │   └── autostart.py        # Integración con el inicio de Windows
│   │
│   └── ui/
│       ├── theme.py            # Tema visual oscuro inspirado en Obsidian
│       ├── icons.py            # Iconos SVG de línea estilo Flaticon/Lucide
│       ├── main_window.py      # Ventana principal de escritorio
│       ├── tray_icon.py        # Icono y menú de la bandeja del sistema
│       ├── widgets/            # Filas de ajustes y conmutadores estilo Obsidian
│       └── tabs/
│           ├── dashboard_tab.py# Resumen, métricas y botón de sincronizar
│           ├── vaults_tab.py   # Gestión y auto-detección de bóvedas
│           ├── schedule_tab.py # Horarios recurrentes (ej. 21:00)
│           ├── gdrive_tab.py   # Configuración de cuenta de Google Drive
│           ├── history_tab.py  # Historial y consola en vivo
│           ├── settings_tab.py # Ajustes de autostart y exclusiones
│           └── about_tab.py    # Información y selector de idioma
│
└── tests/
    ├── test_core.py            # Pruebas unitarias de compresión y configuración
    ├── test_i18n.py            # Comprobación de traducciones Español/Inglés
    ├── test_mirror.py          # Pruebas del modo Mirror sin conexión real
    └── test_ui.py              # Pruebas de inicialización de la interfaz
```

