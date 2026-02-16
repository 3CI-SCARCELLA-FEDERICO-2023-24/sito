@echo off
REM Facial Recognition Application Launcher for Windows
REM This script activates the virtual environment and starts the application

echo ================================================
echo  Sistema di Riconoscimento Facciale
echo ================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please create a virtual environment first:
    echo    python -m venv venv
    echo.
    echo Then install dependencies:
    echo    venv\Scripts\activate.bat
    echo    pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Run the application
echo Starting application...
echo.
python main.py

REM Deactivate virtual environment on exit
deactivate

pause
