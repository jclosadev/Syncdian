@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo             Iniciando Syncdian con Consola
echo ========================================================
echo.

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py %*
) else (
    python main.py %*
)

pause

