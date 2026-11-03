# Syncdian
[Imgur](https://imgur.com/uH9RD1m)

### Background Synchronizer from Obsidian to Google Drive

**Syncdian** is a Windows desktop application designed to keep your **Obsidian** notes and vaults continuously, automatically, and securely backed up to **Google Drive**.

It runs silently in the background (in the System Tray next to the Windows clock) and performs scheduled backups based on your preferences (for example, **every day at 21:00** or at periodic intervals).

---

## Key Features

1. **Silent Background Service**:
   - Lives in the System Tray.
   - Does not interfere with your workflow while writing in Obsidian.
   - If you close the main window, it continues running in the background to perform backups at the scheduled time.

2. **Flexible Recurrent Scheduling**:
   - **Daily at a fixed time**: Configurable to the exact hour you choose (for example, every day at **21:00**).
   - **By intervals**: Every 1h, 2h, 4h, 6h, 12h, 24h.
   - **On-demand manual synchronization**: *"Sync Now"* button to back up changes instantly.

3. **Secure and Versioned Backups**:
   - **ZIP Snapshots (Recommended)**: Packages your vault with timestamp (`MyVault_2026-11-03_21-00-00.zip`). If you delete notes by mistake or a file gets corrupted, you can restore the exact state from any previous day.
   - **Automatic Retention Policy**: Automatically cleans up older backups on Google Drive while keeping the specified number of versions (e.g., last 10 copies) to avoid cluttering your storage space.
   - **Smart Exclusion Filters**: Default filtering to ignore unnecessary files such as `.trash`, `.git`, cache, and temporary files.

4. **Automatic Obsidian Vault Detection**:
   - Automatically reads your local Obsidian configuration to suggest and add your vaults with a single click.

5. **Official Google Drive API Integration**:
   - Secure OAuth 2.0 flow via browser.
   - Restricted scope (`drive.file`): Syncdian only has access to the backups and folders it creates in your Drive, guaranteeing the privacy of your other personal documents.

6. **Auto-Start with Windows**:
   - Option to launch minimized automatically when turning on your PC.

7. **Multilingual Support (Spanish / English)**:
   - Real-time language selector within the application (Spanish and English). Switching languages instantly updates all menus, buttons, notifications, and settings, remembering your choice.

---

## How to Launch the Application

You can launch Syncdian directly using its executable or shortcut files:

- **`Syncdian.exe`**: Standalone compiled Windows executable ready to run with a double-click.
- **`Iniciar_Syncdian.bat`**: Shortcut to launch the application.
- **`Iniciar_Syncdian_Consola.bat`**: Launches the application showing debug messages in a console window.

Or via command line:
```bash
.\Syncdian.exe
```

---

## ☁️ Setting Up Google Drive Connection (Step-by-Step)

To connect Syncdian with your Google Drive account, you need your free credentials from the Google API:

1. **Access Google Cloud Console**:
   - Go to [https://console.cloud.google.com/](https://console.cloud.google.com/) and log in with your Google account.
2. **Create a Project**:
   - In the top bar, click on the project selector and then click **"New Project"**.
   - Name it **"Syncdian"** and click **Create**.
3. **Enable Google Drive API**:
   - In the left sidebar menu (☰), go to **APIs & Services** > **Library**.
   - Search for **"Google Drive API"**, select it, and click **Enable**.
4. **OAuth Consent Screen**:
   - In **APIs & Services**, go to **OAuth consent screen**.
   - User Type: Select **External** and click **Create**.
   - Fill in the *App name* (e.g., `Syncdian`) and your email address. Click *Save and Continue*.
   - In the **Test users** step, add your own Gmail address. Click *Save and Continue*.
5. **Create Desktop Credentials**:
   - Go to **APIs & Services** > **Credentials**.
   - Click **+ Create Credentials** > **OAuth client ID**.
   - Application type: Select **Desktop app**.
   - Name: `Syncdian Desktop`.
   - Click **Create**.
6. **Link with Syncdian**:
   - Click **Download JSON** (you will get a file like `client_secret_xxx.json`).
   - Open Syncdian, navigate to the **Google Drive** tab, and select your JSON file (or copy and paste the *Client ID* and *Client Secret*).
   - Click **"Sign in with Google"**. Your browser will open to grant permissions.
   - Done! Your account will be permanently saved and authorized.

---

## How to Restore a Backup

1. In your Google Drive, you will find a folder named **`Syncdian Obsidian Backups`**.
2. Inside, there will be a folder for each of your vaults.
3. To restore:
   - Download the `.zip` file from your desired date.
   - Extract the contents into your vault directory or a new folder.
   - Open Obsidian and select *"Open folder as vault"*. All your notes, plugins, settings, and links will be intact!

---

## 🛠️ Project Structure

```
Syncdian/
│
├── main.py                     # Entry point of the application
├── requirements.txt            # Python dependencies
├── Iniciar_Syncdian.bat        # Shortcut to launch without console
├── Iniciar_Syncdian_Consola.bat# Shortcut to launch with console
├── README.md                   # This guide
│
├── syncdian/
│   ├── constants.py            # AppData paths, scopes, and constants
│   ├── config.py               # Persistent configuration manager
│   │
│   ├── core/
│   │   ├── vault_manager.py    # Vault auto-detection and ZIP packaging
│   │   ├── gdrive.py           # Official connection and Google Drive API uploads
│   │   ├── scheduler.py        # Background recurring scheduler
│   │   ├── sync_engine.py      # Backup execution engine
│   │   └── autostart.py        # Windows startup integration
│   │
│   └── ui/
│       ├── theme.py            # Dark visual theme inspired by Obsidian
│       ├── main_window.py      # Main desktop window
│       ├── tray_icon.py        # System tray icon and context menu
│       └── tabs/
│           ├── dashboard_tab.py# Summary, metrics, and sync button
│           ├── vaults_tab.py   # Vault management and auto-detection
│           ├── schedule_tab.py # Recurring schedules (e.g., 21:00)
│           ├── gdrive_tab.py   # Google Drive account setup
│           ├── history_tab.py  # History log and live console
│           └── settings_tab.py # Autostart settings and exclusions
│
└── tests/
    ├── test_core.py            # Unit tests for compression and configuration
    └── test_ui.py              # UI initialization unit tests
```
