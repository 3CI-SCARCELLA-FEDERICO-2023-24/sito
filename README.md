# Sistema di Riconoscimento Facciale

Un'applicazione desktop completa per il riconoscimento facciale in tempo reale, sviluppata con Python, PyQt6, MediaPipe e FaceNet.

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Security](https://img.shields.io/badge/security-patched-green.svg)
![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)

## 🔒 Security Notice

**Version 1.0.1** includes critical security updates. If you're using version 1.0.0, please update immediately.  
See [SECURITY.md](SECURITY.md) for details.

## 📚 Documentazione

- **[Guida Rapida (QUICKSTART.md)](QUICKSTART.md)** - Inizia subito! ⚡
- **[Guida Installazione (SETUP.md)](SETUP.md)** - Istruzioni dettagliate
- **[Risoluzione Problemi (TROUBLESHOOTING.md)](TROUBLESHOOTING.md)** - Soluzioni ai problemi comuni
- **[Sicurezza (SECURITY.md)](SECURITY.md)** - Policy di sicurezza e aggiornamenti
- **[Contribuire (CONTRIBUTING.md)](CONTRIBUTING.md)** - Come contribuire al progetto
- **[Changelog (CHANGELOG.md)](CHANGELOG.md)** - Storia delle versioni
- **[Questo README](#)** - Panoramica completa

## 🎯 Caratteristiche Principali

- **Riconoscimento Facciale in Tempo Reale**: Utilizza MediaPipe per il rilevamento dei volti e FaceNet per il riconoscimento
- **Interfaccia Grafica Intuitiva**: GUI moderna sviluppata con PyQt6
- **Gestione Database Utenti**: Database SQLite locale con embeddings facciali
- **Registrazione Automatica**: Possibilità di registrare automaticamente volti sconosciuti
- **Gestione Duplicati**: Sistema intelligente per evitare duplicati nel database
- **Supporto Occhiali**: Riconoscimento affidabile anche con occhiali
- **Performance Ottimizzate**: Elaborazione in tempo reale con bassa latenza

## 🖼️ Screenshot

L'applicazione presenta:
- **Anteprima Camera** (sinistra): Live feed della camera con rilevamento volti in tempo reale
- **Panel di Gestione** (destra): Lista utenti registrati e controlli di gestione

## 📋 Requisiti di Sistema

### Requisiti Minimi
- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **Python**: 3.10 o superiore
- **RAM**: 4 GB (8 GB raccomandati)
- **Webcam**: Qualsiasi webcam compatibile con OpenCV
- **Spazio Disco**: 2 GB per i modelli e le dipendenze

### Requisiti Opzionali
- **GPU NVIDIA**: Per accelerazione CUDA (opzionale ma raccomandato)

## 🚀 Installazione

### Windows

1. **Clona il repository**:
   ```bash
   git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
   cd sito
   ```

2. **Esegui lo script di installazione**:
   ```bash
   install_dependencies.bat
   ```

   Lo script:
   - Crea un ambiente virtuale Python
   - Installa tutte le dipendenze
   - Scarica i modelli pre-addestrati
   - Configura le directory necessarie

3. **Avvia l'applicazione**:
   ```bash
   run.bat
   ```

### Linux / macOS

1. **Clona il repository**:
   ```bash
   git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
   cd sito
   ```

2. **Crea ambiente virtuale**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Installa dipendenze**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Download modelli** (opzionale):
   ```bash
   python models/download_models.py
   ```

5. **Avvia l'applicazione**:
   ```bash
   python main.py
   ```

## 🏗️ Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Window (PyQt6)                     │
├──────────────────────────┬──────────────────────────────────┤
│   Camera Preview         │    Management Panel              │
│   ┌──────────────────┐   │   ┌──────────────────────────┐   │
│   │  Live Camera     │   │   │  User List               │   │
│   │  Feed            │   │   │  - User 1                │   │
│   │                  │   │   │  - User 2                │   │
│   │  ┌─────────┐     │   │   │  - User 3                │   │
│   │  │ Face    │     │   │   └──────────────────────────┘   │
│   │  │ Box     │     │   │   ┌──────────────────────────┐   │
│   │  └─────────┘     │   │   │  Actions                 │   │
│   │  Name: John      │   │   │  [Add] [Delete] [Refresh]│   │
│   │  Conf: 95%       │   │   └──────────────────────────┘   │
│   └──────────────────┘   │                                  │
└──────────────────────────┴──────────────────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────┐            ┌──────────────────┐
│ Face Detection  │            │ Database Manager │
│   (MediaPipe)   │            │    (SQLite)      │
└────────┬────────┘            └────────┬─────────┘
         │                              │
         ▼                              │
┌─────────────────┐                     │
│ Face Encoding   │                     │
│   (FaceNet)     │                     │
└────────┬────────┘                     │
         │                              │
         ▼                              │
┌─────────────────┐                     │
│ Face Matching   │◄────────────────────┘
│  (Embeddings)   │
└─────────────────┘
```

## 📚 Struttura del Progetto

```
sito/
├── main.py                          # Entry point dell'applicazione
├── config.py                        # Configurazioni globali
├── requirements.txt                 # Dipendenze Python
├── setup.py                         # Script di setup
├── install_dependencies.bat         # Script installazione Windows
├── run.bat                          # Script esecuzione Windows
├── README.md                        # Documentazione principale
├── SETUP.md                         # Guida setup dettagliata
├── .gitignore                       # File da escludere da Git
│
├── database/                        # Gestione database
│   ├── __init__.py
│   └── db_manager.py               # Manager SQLite
│
├── face_recognition/               # Moduli riconoscimento facciale
│   ├── __init__.py
│   ├── face_detector.py           # Rilevamento volti (MediaPipe)
│   ├── face_encoder.py            # Generazione embeddings (FaceNet)
│   └── face_matcher.py            # Confronto embeddings
│
├── ui/                             # Interfaccia grafica
│   ├── __init__.py
│   ├── main_window.py             # Finestra principale
│   ├── camera_preview.py          # Widget anteprima camera
│   └── management_panel.py        # Panel gestione utenti
│
└── models/                         # Modelli pre-addestrati
    ├── __init__.py
    └── download_models.py         # Script download modelli
```

## 🎮 Utilizzo

### Avvio dell'Applicazione

1. Esegui `run.bat` (Windows) o `python main.py` (Linux/macOS)
2. La finestra principale si aprirà con due sezioni:
   - **Sinistra**: Anteprima camera
   - **Destra**: Gestione utenti

### Riconoscimento Facciale

1. Clicca su **"Avvia Camera"** nella sezione di anteprima
2. L'applicazione inizierà a rilevare e riconoscere i volti
3. I volti riconosciuti mostreranno il nome e il punteggio di confidenza
4. I volti sconosciuti verranno marcati come "Sconosciuto"

### Registrazione Utenti

#### Registrazione Automatica (Volto Sconosciuto)
1. Quando viene rilevato un volto sconosciuto, apparirà un popup
2. Clicca "Sì" per registrare l'utente
3. Inserisci nome e cognome
4. La foto del volto verrà salvata automaticamente
5. Clicca "OK" per completare la registrazione

#### Registrazione Manuale
1. Nel panel di gestione, clicca **"Aggiungi Utente"**
2. Inserisci nome e cognome
3. Carica una foto del volto (opzionale)
4. Clicca "OK" per salvare

### Gestione Database

- **Visualizza Utenti**: La lista mostra tutti gli utenti registrati
- **Elimina Utente**: Seleziona un utente e clicca "Elimina Utente"
- **Aggiorna Lista**: Clicca "Aggiorna Lista" per ricaricare dal database

## ⚙️ Configurazione

Le configurazioni si trovano in `config.py`:

```python
# Impostazioni Camera
CAMERA_INDEX = 0                    # Indice della camera
CAMERA_WIDTH = 640                  # Larghezza frame
CAMERA_HEIGHT = 480                 # Altezza frame
CAMERA_FPS = 30                     # Frame per secondo

# Impostazioni Riconoscimento
FACE_RECOGNITION_THRESHOLD = 0.6    # Soglia riconoscimento (0-1)
MIN_FACE_SIZE = 20                  # Dimensione minima volto

# Database
MAX_DUPLICATE_DISTANCE = 0.4        # Soglia duplicati
```

## 🔧 Tecnologie Utilizzate

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)**: Framework GUI
- **[OpenCV](https://opencv.org/)**: Elaborazione immagini e video
- **[MediaPipe](https://google.github.io/mediapipe/)**: Rilevamento volti
- **[FaceNet](https://github.com/timesler/facenet-pytorch)**: Generazione embeddings facciali
- **[PyTorch](https://pytorch.org/)**: Framework deep learning
- **[SQLite](https://www.sqlite.org/)**: Database locale
- **[NumPy](https://numpy.org/)**: Elaborazione array numerici

## 🐛 Risoluzione Problemi

### Camera Non Funziona
- Verifica che la webcam sia connessa e funzionante
- Controlla che nessun'altra applicazione stia usando la camera
- Modifica `CAMERA_INDEX` in `config.py` se hai più camere

### Dipendenze Non Installate
- Assicurati di usare Python 3.10+
- Reinstalla le dipendenze: `pip install -r requirements.txt`
- Su Windows, potrebbe essere necessario installare Visual C++ Build Tools

### Riconoscimento Impreciso
- Regola `FACE_RECOGNITION_THRESHOLD` in `config.py`
- Valori più bassi = riconoscimento più rigido
- Valori più alti = riconoscimento più permissivo

### Performance Lente
- Riduci `CAMERA_WIDTH` e `CAMERA_HEIGHT` in `config.py`
- Chiudi altre applicazioni pesanti
- Considera l'uso di una GPU NVIDIA con CUDA

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 👥 Contributori

- Sistema di Riconoscimento Facciale Team

## 🙏 Ringraziamenti

- Google MediaPipe per il rilevamento volti
- FaceNet per gli embeddings facciali
- OpenCV community per gli strumenti di computer vision
- PyQt per il framework GUI

## 📧 Supporto

Per problemi, domande o suggerimenti, apri una issue su GitHub.

---

**Nota**: Questo software è fornito "così com'è" senza garanzie. L'uso del riconoscimento facciale deve rispettare le leggi sulla privacy applicabili.
