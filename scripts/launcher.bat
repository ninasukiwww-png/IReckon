@echo off
title IReckon AI Factory
echo ============================================
echo   IReckon AI Factory
echo ============================================
echo.
start "" "%~dp0ireckon-backend\ireckon-backend.exe"
echo [BACKEND] Starting... (port 8000)
timeout /t 3 /nobreak >nul
start "" "%~dp0ireckon-frontend\ireckon-frontend.exe"
echo [FRONTEND] Starting... (port 8501)
timeout /t 5 /nobreak >nul
echo.
echo   Backend: http://localhost:8000/docs
echo   Frontend: http://localhost:8501
echo.
start http://localhost:8501
echo Close this window to stop
echo.
pause >nul
taskkill /f /im ireckon-backend.exe >nul 2>&1
taskkill /f /im ireckon-frontend.exe >nul 2>&1
