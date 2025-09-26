@echo off
title Agentic Configuration Research System

REM Change to script directory
cd /d "%~dp0"

REM Set window properties
mode con cols=80 lines=30
color 0A

echo.
echo     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo     @                                                                        @
echo     @           🤖 AGENTIC CONFIGURATION RESEARCH SYSTEM 🤖                @
echo     @                                                                        @
echo     @                   AI-Powered Configuration Research                   @
echo     @                        ^& Troubleshooting Platform                     @
echo     @                                                                        @
echo     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
echo.
echo     Starting system...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo     ❌ Python not found!
    echo     Please install Python 3.9+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Run the simple launcher
echo     ✅ Python found, starting application...
echo.
python simple_launcher.py

REM Pause on exit
echo.
pause