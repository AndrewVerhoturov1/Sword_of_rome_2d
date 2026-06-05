@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "scripts\codex_token_monitor_server.py" (
    echo [ERROR] Server script not found: scripts\codex_token_monitor_server.py
    pause
    exit /b 1
)

echo Starting Codex Token Monitor Server v1...
echo http://127.0.0.1:8765
echo Press Ctrl+C to stop.
echo.

python scripts\codex_token_monitor_server.py --host 127.0.0.1 --port 8765 --open-browser

echo.
echo Server stopped.
pause
