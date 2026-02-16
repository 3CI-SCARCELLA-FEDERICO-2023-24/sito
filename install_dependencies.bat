@echo off
REM Script di installazione automatica per Windows

echo ================================================
echo Installazione Sistema di Riconoscimento Facciale
echo ================================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python 3.10 o superiore da https://www.python.org/
    pause
    exit /b 1
)

echo Python trovato!
python --version
echo.

REM Crea ambiente virtuale
echo Creazione ambiente virtuale...
python -m venv venv

REM Attiva ambiente virtuale
echo Attivazione ambiente virtuale...
call venv\Scripts\activate.bat

REM Aggiorna pip
echo Aggiornamento pip...
python -m pip install --upgrade pip

REM Installa dipendenze
echo.
echo Installazione dipendenze...
echo Questo potrebbe richiedere diversi minuti...
echo.

pip install -r requirements.txt

REM Controlla se l'installazione è riuscita
if errorlevel 1 (
    echo.
    echo ERRORE durante l'installazione delle dipendenze!
    echo Controlla i messaggi di errore sopra.
    pause
    exit /b 1
)

REM Download modelli
echo.
echo Download modelli pre-addestrati...
python models/download_models.py

REM Crea le directory necessarie
echo.
echo Creazione directory...
if not exist "database" mkdir database
if not exist "data" mkdir data
if not exist "data\faces" mkdir "data\faces"
if not exist "models" mkdir models

echo.
echo ================================================
echo Installazione completata con successo!
echo ================================================
echo.
echo Per avviare l'applicazione:
echo 1. Attiva l'ambiente virtuale: venv\Scripts\activate.bat
echo 2. Esegui: python main.py
echo.
echo Oppure usa il file run.bat
echo.
pause
