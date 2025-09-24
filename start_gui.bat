@echo off
title Agentic Configuration Research System
cd /d "%~dp0"

echo 🤖 Agentic Configuration Research System
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.9+
    echo    Download from: https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Starting GUI application...
echo.
python gui_app.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application ended with error
    pause
)