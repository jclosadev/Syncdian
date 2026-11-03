@echo off
setlocal
cd /d "%~dp0"

if exist "Syncdian.exe" (
    start "" "Syncdian.exe" %*
) else if exist "dist\Syncdian.exe" (
    start "" "dist\Syncdian.exe" %*
) else if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py %*
) else (
    echo Iniciando con Python...
    python main.py %*
)
