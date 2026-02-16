# Guida alla Risoluzione Problemi

Questa guida ti aiuterà a risolvere i problemi più comuni.

## 📋 Indice

1. [Problemi di Installazione](#problemi-di-installazione)
2. [Problemi con la Camera](#problemi-con-la-camera)
3. [Problemi di Riconoscimento](#problemi-di-riconoscimento)
4. [Problemi di Performance](#problemi-di-performance)
5. [Problemi UI](#problemi-ui)
6. [Problemi Database](#problemi-database)

## Problemi di Installazione

### ❌ "Python non trovato" o "python is not recognized"

**Causa**: Python non è installato o non è nel PATH di sistema.

**Soluzione**:
1. Installa Python 3.10+ da [python.org](https://www.python.org/)
2. Durante l'installazione, spunta "Add Python to PATH"
3. Riavvia il terminale/prompt dei comandi
4. Verifica: `python --version`

### ❌ "pip non trovato" o "No module named pip"

**Soluzione**:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### ❌ Errore durante `pip install -r requirements.txt`

**Windows - Visual C++ Build Tools mancanti**:
1. Scarica [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Installa "Desktop development with C++"
3. Riavvia e riprova

**Linux - Dipendenze di sistema**:
```bash
sudo apt-get update
sudo apt-get install python3-dev build-essential
```

### ❌ "Could not find a version that satisfies the requirement"

**Causa**: Versione Python incompatibile o repository PyPI non raggiungibile.

**Soluzione**:
1. Verifica versione Python: `python --version` (richiede 3.10+)
2. Aggiorna pip: `python -m pip install --upgrade pip`
3. Prova a installare le dipendenze una alla volta

## Problemi con la Camera

### ❌ "Camera non disponibile" o schermo nero

**Soluzioni**:

**1. Verifica che la camera funzioni**:
- Prova con un'altra applicazione (es. Skype, Zoom)
- Controlla che la camera sia connessa

**2. Chiudi altre applicazioni**:
- Chiudi tutte le app che potrebbero usare la camera
- Su Windows, controlla il Task Manager

**3. Prova un altro indice camera**:
Modifica `config.py`:
```python
CAMERA_INDEX = 1  # Prova 0, 1, 2, etc.
```

**4. Linux - Permessi camera**:
```bash
sudo usermod -a -G video $USER
# Logout e login
```

**5. Windows - Permessi privacy**:
- Impostazioni → Privacy → Camera
- Assicurati che le app desktop possano accedere alla camera

### ❌ La camera si blocca o congela

**Soluzioni**:
1. Riduci risoluzione in `config.py`:
   ```python
   CAMERA_WIDTH = 320
   CAMERA_HEIGHT = 240
   ```
2. Riavvia l'applicazione
3. Riavvia il computer

### ❌ Immagine capovolta o ruotata

**Soluzione**: Modifica `ui/camera_preview.py` per aggiungere rotazione:
```python
# Ruota l'immagine
frame = cv2.rotate(frame, cv2.ROTATE_180)
```

## Problemi di Riconoscimento

### ❌ "Sconosciuto" anche per utenti registrati

**Cause e Soluzioni**:

**1. Soglia troppo rigida**:
Modifica `config.py`:
```python
FACE_RECOGNITION_THRESHOLD = 0.7  # Aumenta (max 1.0)
```

**2. Scarsa illuminazione**:
- Assicurati di avere buona illuminazione
- Luce frontale, non dietro

**3. Volto non frontale**:
- Mantieni il volto frontale alla camera
- Evita angolazioni estreme

**4. Embedding non generato correttamente**:
- Elimina l'utente
- Registra di nuovo con foto migliore

**5. Database non aggiornato**:
- Clicca "Aggiorna Lista" nel pannello di gestione
- Riavvia l'applicazione

### ❌ Riconoscimento troppo permissivo (false positive)

**Soluzione**: Riduci la soglia in `config.py`:
```python
FACE_RECOGNITION_THRESHOLD = 0.4  # Riduci (min 0.0)
```

### ❌ Volti non rilevati

**Cause e Soluzioni**:

**1. Volto troppo piccolo**:
- Avvicinati alla camera
- Riduci `MIN_FACE_SIZE` in `config.py`

**2. Scarsa qualità immagine**:
- Migliora l'illuminazione
- Pulisci la lente della camera

**3. Confidence MediaPipe bassa**:
Modifica `config.py`:
```python
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.3  # Riduci da 0.5
```

## Problemi di Performance

### ❌ Applicazione lenta o lag

**Soluzioni**:

**1. Riduci risoluzione camera**:
```python
# config.py
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_FPS = 15
```

**2. Chiudi applicazioni non necessarie**:
- Controlla Task Manager/System Monitor
- Chiudi browser con molte tab

**3. Usa GPU (se disponibile)**:
Installa PyTorch con CUDA:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

**4. Riduci numero massimo volti**:
```python
# config.py
MEDIAPIPE_MAX_FACES = 1  # Riduci da 5
```

### ❌ Alto utilizzo CPU

**Soluzioni**:
1. Riduci FPS in `config.py`
2. Riduci risoluzione
3. Chiudi l'applicazione quando non in uso

### ❌ Alto utilizzo RAM

**Soluzioni**:
1. Riavvia l'applicazione periodicamente
2. Riduci il numero di utenti nel database (se molto grande)
3. Chiudi altre applicazioni

## Problemi UI

### ❌ Finestra non si apre o crash immediato

**Cause**:

**1. PyQt6 non installato correttamente**:
```bash
pip uninstall PyQt6
pip install PyQt6
```

**2. Windows - DLL mancanti**:
Installa [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

**3. Linux - Librerie sistema**:
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0
```

### ❌ Testo sfocato o UI troppo piccola

**Windows - Scaling alto DPI**:
1. Click destro su `python.exe`
2. Proprietà → Compatibilità
3. "Change high DPI settings"
4. Spunta "Override high DPI scaling behavior"

### ❌ Preview camera distorta

**Soluzione**: Modifica aspect ratio in `ui/camera_preview.py`:
```python
Qt.AspectRatioMode.KeepAspectRatio  # Mantieni proporzioni
# oppure
Qt.AspectRatioMode.IgnoreAspectRatio  # Ignora proporzioni
```

## Problemi Database

### ❌ "Database is locked"

**Causa**: Multipla istanze dell'applicazione.

**Soluzione**:
1. Chiudi tutte le istanze dell'applicazione
2. Se persiste, elimina il file lock: `database/face_recognition.db-journal`

### ❌ Database corrotto

**Soluzione**:
1. Backup del database se possibile
2. Elimina `database/face_recognition.db`
3. Riavvia l'applicazione (crea nuovo database)
4. Registra di nuovo gli utenti

### ❌ "UNIQUE constraint failed"

**Causa**: Tentativo di registrare utente duplicato.

**Soluzione**: Usa nome/cognome diversi o elimina l'utente esistente prima.

## 🔍 Debug Avanzato

### Attivare Logging Dettagliato

Modifica all'inizio di `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Componenti Individuali

```bash
# Test database
python -c "from database.db_manager import DatabaseManager; db = DatabaseManager(); print('DB OK')"

# Test camera
python -c "import cv2; cam = cv2.VideoCapture(0); print('Camera OK' if cam.isOpened() else 'Camera FAIL')"

# Test MediaPipe
python -c "import mediapipe as mp; print('MediaPipe OK')"

# Test PyTorch
python -c "import torch; print('PyTorch OK')"
```

### Raccogliere Informazioni per Bug Report

```bash
python test_installation.py > debug_info.txt 2>&1
```

## 📧 Ottenere Aiuto

Se nessuna soluzione funziona:

1. **Verifica documentazione**: README.md, SETUP.md
2. **Cerca nelle Issues**: [GitHub Issues](https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito/issues)
3. **Apri una nuova Issue** con:
   - Sistema operativo e versione
   - Versione Python
   - Output di `python test_installation.py`
   - Messaggio di errore completo
   - Passi per riprodurre

---

**Suggerimento**: Mantieni sempre l'applicazione e le dipendenze aggiornate!
