# Guida Completa all'Installazione

Questa guida fornisce istruzioni dettagliate per l'installazione e la configurazione del Sistema di Riconoscimento Facciale.

## 📋 Indice

1. [Prerequisiti](#prerequisiti)
2. [Installazione Python](#installazione-python)
3. [Installazione Applicazione](#installazione-applicazione)
4. [Configurazione](#configurazione)
5. [Verifica Installazione](#verifica-installazione)
6. [Risoluzione Problemi](#risoluzione-problemi)

## Prerequisiti

### Hardware Necessario

- **Computer**: PC Windows/Linux/macOS
- **Webcam**: Webcam integrata o USB
- **RAM**: Minimo 4 GB (8 GB raccomandato)
- **Spazio Disco**: 2 GB liberi
- **GPU** (opzionale): NVIDIA con supporto CUDA per prestazioni migliori

### Software Necessario

- **Python 3.10 o superiore**
- **pip** (package manager Python)
- **Git** (per clonare il repository)

## Installazione Python

### Windows

1. **Download Python**:
   - Vai su [python.org/downloads](https://www.python.org/downloads/)
   - Scarica Python 3.10 o superiore per Windows
   - **IMPORTANTE**: Durante l'installazione, spunta "Add Python to PATH"

2. **Verifica Installazione**:
   ```cmd
   python --version
   pip --version
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
python3 --version
```

### macOS

```bash
# Usando Homebrew
brew install python@3.10

# Verifica
python3 --version
```

## Installazione Applicazione

### Metodo 1: Installazione Automatica (Windows)

1. **Clona il repository**:
   ```cmd
   git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
   cd sito
   ```

2. **Esegui script di installazione**:
   ```cmd
   install_dependencies.bat
   ```

   Lo script eseguirà automaticamente:
   - Creazione ambiente virtuale
   - Installazione dipendenze
   - Download modelli
   - Configurazione directory

3. **Avvia l'applicazione**:
   ```cmd
   run.bat
   ```

### Metodo 2: Installazione Manuale

#### Windows

```cmd
# 1. Clona repository
git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
cd sito

# 2. Crea ambiente virtuale
python -m venv venv

# 3. Attiva ambiente virtuale
venv\Scripts\activate.bat

# 4. Aggiorna pip
python -m pip install --upgrade pip

# 5. Installa dipendenze
pip install -r requirements.txt

# 6. Download modelli (opzionale)
python models/download_models.py

# 7. Avvia applicazione
python main.py
```

#### Linux/macOS

```bash
# 1. Clona repository
git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
cd sito

# 2. Crea ambiente virtuale
python3 -m venv venv

# 3. Attiva ambiente virtuale
source venv/bin/activate

# 4. Aggiorna pip
pip install --upgrade pip

# 5. Installa dipendenze
pip install -r requirements.txt

# 6. Download modelli (opzionale)
python models/download_models.py

# 7. Avvia applicazione
python main.py
```

## Configurazione

### Configurazione Camera

Modifica `config.py` per configurare la camera:

```python
# Indice della camera (0 = camera predefinita)
CAMERA_INDEX = 0

# Risoluzione
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Frame rate
CAMERA_FPS = 30
```

**Nota**: Se hai più camere, cambia `CAMERA_INDEX` a 1, 2, etc.

### Configurazione Riconoscimento

```python
# Soglia di riconoscimento (0.0 - 1.0)
# Valori bassi = più rigido
# Valori alti = più permissivo
FACE_RECOGNITION_THRESHOLD = 0.6

# Dimensione minima del volto in pixel
MIN_FACE_SIZE = 20

# Soglia per considerare duplicati
MAX_DUPLICATE_DISTANCE = 0.4
```

### Configurazione Interfaccia

```python
# Dimensioni finestra
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Dimensioni preview camera
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480
```

## Verifica Installazione

### Test 1: Verifica Dipendenze

```python
# test_dependencies.py
try:
    import cv2
    print("✓ OpenCV installato")
    
    import mediapipe
    print("✓ MediaPipe installato")
    
    import torch
    print("✓ PyTorch installato")
    
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 installato")
    
    print("\n✅ Tutte le dipendenze sono installate correttamente!")
    
except ImportError as e:
    print(f"❌ Errore: {e}")
```

Esegui:
```bash
python test_dependencies.py
```

### Test 2: Verifica Camera

```python
# test_camera.py
import cv2

camera = cv2.VideoCapture(0)

if camera.isOpened():
    print("✅ Camera funzionante!")
    ret, frame = camera.read()
    if ret:
        print(f"✅ Frame catturato: {frame.shape}")
    camera.release()
else:
    print("❌ Errore: Camera non disponibile")
```

Esegui:
```bash
python test_camera.py
```

### Test 3: Verifica Database

```python
# test_database.py
from database.db_manager import DatabaseManager

db = DatabaseManager()
print("✅ Database inizializzato correttamente!")

users = db.get_all_users()
print(f"✅ Utenti nel database: {len(users)}")

db.close()
```

Esegui:
```bash
python test_database.py
```

## Installazione GPU (Opzionale)

Per migliorare le prestazioni con GPU NVIDIA:

### 1. Verifica CUDA

```bash
nvidia-smi
```

### 2. Installa PyTorch con CUDA

```bash
# Per CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Per CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 3. Verifica GPU

```python
import torch
print(f"CUDA disponibile: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")
```

## Risoluzione Problemi

### Problema: "Python non trovato"

**Soluzione**:
- Assicurati che Python sia installato
- Aggiungi Python al PATH di sistema
- Riavvia il terminale/prompt dei comandi

### Problema: "pip non trovato"

**Soluzione**:
```bash
python -m ensurepip --upgrade
```

### Problema: Errore durante installazione dipendenze

**Windows - Visual C++ Build Tools**:
1. Scarica [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
2. Installa "Desktop development with C++"

**Linux - Dipendenze di sistema**:
```bash
sudo apt-get install python3-dev build-essential
```

### Problema: "ModuleNotFoundError"

**Soluzione**:
```bash
# Attiva l'ambiente virtuale
# Windows
venv\Scripts\activate.bat

# Linux/macOS
source venv/bin/activate

# Reinstalla dipendenze
pip install -r requirements.txt
```

### Problema: Camera non funziona

**Soluzioni**:
1. Verifica permessi camera
2. Chiudi altre app che usano la camera
3. Prova un altro indice camera in `config.py`
4. Su Linux, aggiungi il tuo utente al gruppo video:
   ```bash
   sudo usermod -a -G video $USER
   ```

### Problema: PyQt6 non si avvia

**Windows - DLL mancanti**:
- Installa [Microsoft Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

**Linux - Librerie mancanti**:
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

### Problema: Prestazioni lente

**Soluzioni**:
1. Riduci risoluzione camera in `config.py`
2. Chiudi applicazioni non necessarie
3. Usa una GPU (vedi sezione GPU)
4. Riduci il numero di volti rilevati contemporaneamente

### Problema: Riconoscimento impreciso

**Soluzioni**:
1. Regola `FACE_RECOGNITION_THRESHOLD` in `config.py`
2. Assicurati che la luce sia buona
3. Mantieni il volto frontale alla camera
4. Riregistra gli utenti con foto migliori

## Aggiornamento

Per aggiornare l'applicazione:

```bash
# 1. Ferma l'applicazione se in esecuzione

# 2. Aggiorna da Git
git pull origin main

# 3. Aggiorna dipendenze
pip install -r requirements.txt --upgrade

# 4. Riavvia l'applicazione
python main.py
```

## Disinstallazione

```bash
# 1. Elimina l'ambiente virtuale
# Windows
rmdir /s venv

# Linux/macOS
rm -rf venv

# 2. (Opzionale) Elimina la directory del progetto
cd ..
# Windows
rmdir /s sito

# Linux/macOS
rm -rf sito
```

## Supporto

Per ulteriore assistenza:
- Consulta il [README.md](README.md)
- Apri una issue su GitHub
- Controlla i log di errore

## Best Practices

1. **Sempre usare l'ambiente virtuale** per evitare conflitti di dipendenze
2. **Backup del database** periodico (copia `database/face_recognition.db`)
3. **Buona illuminazione** per miglior riconoscimento
4. **Foto di qualità** durante la registrazione
5. **Aggiornamenti regolari** del software

---

Buona installazione! 🚀
