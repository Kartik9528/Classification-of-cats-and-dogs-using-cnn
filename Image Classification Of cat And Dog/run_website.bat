@echo off
echo ================================================
echo  Cat and Dog CNN Classification - Web App
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Starting setup...
echo.

REM Try to run the quick start script
python quick_start.py

if errorlevel 1 (
    echo.
    echo Quick start failed. Trying full setup...
    python setup_and_run.py
)

pause
