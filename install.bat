@echo off
REM Installation script for Windows
REM This script sets up the virtual environment and installs dependencies

echo ================================================
echo  Facial Recognition Application - Installation
echo ================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python 3.10 or later from python.org
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

echo ✓ Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take several minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    echo Try installing dependencies manually:
    echo    venv\Scripts\activate.bat
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ================================================
echo  Installation Complete!
echo ================================================
echo.
echo To start the application, run:
echo    run.bat
echo.
echo Or manually:
echo    venv\Scripts\activate.bat
echo    python main.py
echo.

REM Run verification script
echo Running installation verification...
echo.
python verify_installation.py

deactivate

echo.
pause
