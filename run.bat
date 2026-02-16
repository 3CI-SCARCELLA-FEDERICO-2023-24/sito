@echo off
REM Script per eseguire l'applicazione

echo Avvio Sistema di Riconoscimento Facciale...
echo.

REM Attiva l'ambiente virtuale se esiste
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Esegui l'applicazione
python main.py

pause
