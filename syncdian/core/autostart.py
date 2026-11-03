import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_REG_NAME = "Syncdian"


class WindowsAutostart:
    @staticmethod
    def get_run_command() -> str:
        """Determina el comando para iniciar Syncdian minimizado en segundo plano."""
        # Si se ejecuta como ejecutable congelado (PyInstaller)
        if getattr(sys, "frozen", False):
            exe_path = sys.executable
            return f'"{exe_path}" --minimized'
        else:
            # Script python: usar pythonw.exe si existe para evitar ventana de consola negra
            python_exe = sys.executable
            pythonw_exe = Path(python_exe).parent / "pythonw.exe"
            runner = str(pythonw_exe) if pythonw_exe.exists() else python_exe
            main_script = Path(__file__).resolve().parent.parent.parent / "main.py"
            return f'"{runner}" "{main_script}" --minimized'

    @classmethod
    def is_enabled(cls) -> bool:
        if sys.platform != "win32":
            return False
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, APP_REG_NAME)
                return bool(val)
        except Exception:
            return False

    @classmethod
    def set_enabled(cls, enable: bool) -> bool:
        if sys.platform != "win32":
            return False
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
                if enable:
                    cmd = cls.get_run_command()
                    winreg.SetValueEx(key, APP_REG_NAME, 0, winreg.REG_SZ, cmd)
                    logger.info(f"Autostart activado en Windows: {cmd}")
                else:
                    try:
                        winreg.DeleteValue(key, APP_REG_NAME)
                        logger.info("Autostart desactivado en Windows.")
                    except FileNotFoundError:
                        pass
            return True
        except Exception as e:
            logger.error(f"Error modificando registro de Windows para autostart: {e}")
            return False

