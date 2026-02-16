# Sistema di Riconoscimento Facciale

Applicazione desktop per il riconoscimento facciale real-time con registrazione automatica e gestione delle persone.

## 🎯 Caratteristiche

- **Riconoscimento Real-time**: Cattura video dalla webcam e riconosce i volti in tempo reale
- **Registrazione Automatica**: I volti sconosciuti vengono automaticamente registrati nel database
- **Gestione Persone**: Interfaccia per modificare nomi, cognomi e foto delle persone registrate
- **IA Avanzata**: Utilizza MediaPipe per il rilevamento e DeepFace per il riconoscimento
- **Cross-platform**: Funziona su Windows, Linux e macOS
- **Database Locale**: Archiviazione sicura con SQLite

## 🛠️ Tecnologie Utilizzate

- **Python 3.8+**
- **PyQt6**: Interfaccia grafica moderna
- **OpenCV**: Elaborazione video e immagini
- **MediaPipe**: Rilevamento volti ad alte prestazioni
- **DeepFace**: Riconoscimento facciale con modelli pre-addestrati
- **TensorFlow**: Backend per machine learning
- **SQLite**: Database locale

## 📋 Requisiti

### Sistema Operativo
- Windows 10/11
- Linux (Ubuntu 20.04+, Debian, Fedora)
- macOS 10.15+

### Hardware
- Webcam (integrata o USB)
- RAM: minimo 4GB (consigliato 8GB+)
- CPU: processore multi-core
- GPU: opzionale (per accelerazione CUDA)

### Software
- Python 3.8 o superiore
- pip (gestore pacchetti Python)

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
cd sito/application
```

### 2. Crea un ambiente virtuale (consigliato)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

> **Nota**: Il primo avvio potrebbe richiedere alcuni minuti per scaricare i modelli pre-addestrati.

### 4. Avvia l'applicazione

```bash
python main.py
```

## 📖 Utilizzo

### Avvio dell'Applicazione

1. Avvia l'applicazione con `python main.py`
2. La webcam si attiverà automaticamente
3. L'interfaccia mostrerà il feed video sulla sinistra

### Riconoscimento Automatico

- **Volti Conosciuti**: Evidenziati con bordo verde e nome
- **Volti Sconosciuti**: Evidenziati con bordo giallo e registrati automaticamente come "Sconosciuto"

### Gestione Persone

1. Clicca su **"Gestione Persone"** per aprire il pannello di gestione
2. Seleziona una persona dalla lista
3. Modifica nome e cognome
4. Carica una foto personalizzata (opzionale)
5. Clicca **"Salva Modifiche"**
6. Usa **"Elimina"** per rimuovere una persona dal database

### Statistiche

Il pannello di controllo mostra:
- Numero totale di persone registrate
- Numero di persone sconosciute
- FPS (fotogrammi per secondo) nella barra di stato

## ⚙️ Configurazione

Modifica `modules/config.py` per personalizzare:

```python
# Impostazioni webcam
CAMERA_INDEX = 0  # Cambia se hai più webcam
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Impostazioni riconoscimento
RECOGNITION_THRESHOLD = 0.4  # Più basso = più rigoroso (0.0-1.0)
RECOGNITION_MODEL = "Facenet512"  # Modello di riconoscimento

# Performance
PROCESS_EVERY_N_FRAMES = 2  # Elabora ogni N frame
ENABLE_GPU = True  # Abilita GPU se disponibile
```

### Modelli Disponibili

- **VGG-Face**: Accurato, lento
- **Facenet**: Bilanciato
- **Facenet512**: Alta accuratezza (predefinito)
- **OpenFace**: Veloce, meno accurato
- **DeepFace**: Accurato
- **ArcFace**: Molto accurato

## 📁 Struttura del Progetto

```
application/
├── main.py                 # Entry point dell'applicazione
├── requirements.txt        # Dipendenze Python
├── ui/
│   ├── main_window.py     # Finestra principale
│   ├── management_panel.py # Pannello di gestione
│   └── styles.qss         # Stylesheet PyQt6
├── modules/
│   ├── config.py          # Configurazione
│   ├── database.py        # Gestione database SQLite
│   ├── camera.py          # Gestione webcam
│   ├── face_detector.py   # Rilevamento volti (MediaPipe)
│   └── face_recognizer.py # Riconoscimento volti (DeepFace)
└── data/                   # Directory dati (auto-generata)
    ├── faces/             # Foto salvate
    └── faces.db           # Database SQLite
```

## 🔧 Risoluzione Problemi

### La webcam non si avvia

- Verifica che la webcam sia collegata e funzionante
- Controlla che nessun'altra applicazione stia usando la webcam
- Prova a cambiare `CAMERA_INDEX` in `config.py`

### Errori durante l'installazione

- Assicurati di avere Python 3.8+: `python --version`
- Aggiorna pip: `pip install --upgrade pip`
- Su Linux, potrebbe essere necessario: `sudo apt-get install python3-dev`

### Performance lente

- Aumenta `PROCESS_EVERY_N_FRAMES` in `config.py`
- Riduci risoluzione webcam
- Abilita GPU se disponibile
- Usa un modello più veloce (es. OpenFace invece di Facenet512)

### Errori TensorFlow/GPU

Se non hai una GPU NVIDIA o CUDA:
```bash
pip uninstall tensorflow-gpu
pip install tensorflow
```

## 🔒 Privacy e Sicurezza

- Tutti i dati sono archiviati localmente
- Nessun dato viene inviato a server esterni
- Il database SQLite è nel file `data/faces.db`
- Le foto sono salvate in `data/faces/`

## 🚀 Sviluppo Futuro

- [ ] Supporto per Raspberry Pi
- [ ] Riconoscimento con mascherine
- [ ] Rilevamento multi-volto simultaneo
- [ ] Export/Import database
- [ ] API REST per integrazioni
- [ ] Dashboard web
- [ ] Notifiche real-time
- [ ] Log degli accessi

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file LICENSE per maggiori dettagli.

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 👥 Autori

- Federico Scarcella - Sviluppo iniziale

## 🙏 Ringraziamenti

- MediaPipe team per il framework di rilevamento volti
- DeepFace team per i modelli di riconoscimento
- TensorFlow e PyQt6 communities

## 📞 Supporto

Per bug, domande o suggerimenti, apri una issue su GitHub.

---

**Made with ❤️ in Python**
