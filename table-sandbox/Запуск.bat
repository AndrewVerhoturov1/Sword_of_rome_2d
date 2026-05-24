@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Table Sandbox 0.1 — Runtime/Data Bootstrap
echo ============================================
echo.
echo Запуск Vite dev-сервера...
echo Открой http://localhost:5173 в браузере
echo.
call npm run dev
pause
