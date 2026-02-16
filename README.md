# Sistema di Riconoscimento Facciale

Applicazione desktop per Windows con riconoscimento facciale in tempo reale utilizzando MediaPipe e TensorFlow.

## Caratteristiche

### Funzionalità Principali

1. **Rilevamento e Riconoscimento Facciale in Tempo Reale**
   - Anteprima della webcam in tempo reale
   - Rilevamento facciale usando MediaPipe
   - Riconoscimento AI con embedding FaceNet di TensorFlow
   - Supporto per riconoscimento con e senza occhiali

2. **Sistema di Registrazione Utenti**
   - Prompt automatico per nuovi volti rilevati
   - Campi di registrazione: Nome, Cognome, Foto Profilo
   - Opzione di caricamento foto o utilizzo del frame rilevato
   - Registrazione predefinita come "Sconosciuto" se si salta
   - Prevenzione duplicati - ogni persona deve essere unica

3. **Pannello di Gestione (Pulsante "Gestione")**
   - Visualizzazione utenti registrati con foto profilo
   - Aggiunta manuale di nuovi utenti
   - Eliminazione utenti esistenti
   - Modifica informazioni utente

4. **Database e Archiviazione**
   - Database SQLite per informazioni utenti
   - Archiviazione embedding facciali per confronto accurato
   - Vincolo di unicità sugli utenti

## Requisiti di Sistema

- Windows 10 o successivo
- Python 3.10 o successivo
- Webcam
- Almeno 4GB RAM

## Installazione

### 1. Clonare il Repository

```bash
git clone https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito.git
cd sito
```

### 2. Creare Ambiente Virtuale

```bash
python -m venv venv
venv\Scripts\activate  # Su Windows
```

### 3. Installare Dipendenze

```bash
pip install -r requirements.txt
```

## Utilizzo

### Avviare l'Applicazione

```bash
python main.py
```

### Interfaccia Utente

L'applicazione si compone di tre pannelli principali:

- **Pannello Sinistro**: Anteprima webcam in tempo reale
- **Pannello Centrale**: Stato riconoscimento e informazioni
- **Pannello Destro**: Pulsanti di controllo

### Workflow di Utilizzo

1. **Primo Avvio**
   - L'applicazione inizia a rilevare volti automaticamente
   - Quando viene rilevato un nuovo volto, appare un dialogo di registrazione

2. **Registrazione Nuovo Utente**
   - Inserire Nome e Cognome (obbligatori)
   - Opzionale: Caricare una foto profilo personalizzata
   - Cliccare "Salva" per registrare l'utente
   - Oppure cliccare "Salta (Sconosciuto)" per registrazione predefinita
   - La foto del frame rilevato viene salvata automaticamente se non ne viene caricata una

3. **Riconoscimento**
   - I volti registrati vengono riconosciuti automaticamente
   - Il nome appare sopra il volto rilevato
   - Le informazioni dell'utente vengono mostrate nel pannello centrale

4. **Gestione Utenti**
   - Cliccare il pulsante "Gestione" nel pannello destro
   - Visualizzare tutti gli utenti registrati
   - Aggiungere nuovi utenti manualmente
   - Eliminare utenti esistenti

## Stack Tecnologico

- **Linguaggio**: Python 3.10+
- **GUI**: PyQt6
- **Rilevamento Facciale**: MediaPipe Face Detection
- **Riconoscimento Facciale**: TensorFlow con embedding FaceNet
- **Database**: SQLite3
- **Camera**: OpenCV
- **Elaborazione Immagini**: Pillow, NumPy, SciPy

## Struttura del Progetto

```
sito/
├── main.py                          # Entry point dell'applicazione
├── config.py                        # Impostazioni di configurazione
├── requirements.txt                 # Dipendenze Python
├── README.md                        # Documentazione
├── database/
│   ├── __init__.py
│   └── database.py                  # Operazioni SQLite
├── face_recognition/
│   ├── __init__.py
│   ├── detector.py                  # Rilevamento MediaPipe
│   ├── embedder.py                  # Embedding FaceNet
│   └── matcher.py                   # Logica confronto volti
├── ui/
│   ├── __init__.py
│   ├── main_window.py              # Finestra principale
│   ├── camera_widget.py            # Widget anteprima camera
│   ├── registration_dialog.py      # Dialogo registrazione
│   └── management_dialog.py        # Dialogo gestione utenti
├── models/                          # Archiviazione modelli pre-addestrati
│   └── README.md
└── data/
    ├── users/                       # Foto utenti
    ├── embeddings/                  # Embedding facciali
    └── users.db                     # Database SQLite
```

## Configurazione

Le impostazioni possono essere modificate nel file `config.py`:

- `CAMERA_INDEX`: Indice della webcam (default: 0)
- `CAMERA_WIDTH`: Larghezza frame camera (default: 640)
- `CAMERA_HEIGHT`: Altezza frame camera (default: 480)
- `MIN_DETECTION_CONFIDENCE`: Soglia confidenza rilevamento (default: 0.7)
- `SIMILARITY_THRESHOLD`: Soglia similarità riconoscimento (default: 0.6)
- `WINDOW_WIDTH`: Larghezza finestra (default: 1200)
- `WINDOW_HEIGHT`: Altezza finestra (default: 700)

## Risoluzione Problemi

### Webcam Non Rilevata

Se la webcam non viene rilevata:
1. Verificare che la webcam sia collegata
2. Modificare `CAMERA_INDEX` in `config.py` (provare 0, 1, 2)
3. Verificare i permessi della webcam nelle impostazioni di Windows

### Errori di Importazione

Se si verificano errori di importazione:
```bash
pip install --upgrade -r requirements.txt
```

### Performance Lenta

Se l'applicazione è lenta:
1. Ridurre la risoluzione della camera in `config.py`
2. Aumentare `detection_cooldown` in `main_window.py`
3. Chiudere altre applicazioni che usano la webcam

## Note Tecniche

### Modelli di Riconoscimento

L'applicazione utilizza un'architettura semplificata di FaceNet. Per migliori risultati in produzione:
1. Scaricare i pesi pre-addestrati (vedere `models/README.md`)
2. Implementare il caricamento dei pesi in `embedder.py`

### Sicurezza e Privacy

- Tutti i dati sono archiviati localmente
- Nessuna connessione internet richiesta (dopo l'installazione)
- I dati degli utenti possono essere eliminati tramite il pannello di gestione

## Licenza

Questo progetto è sviluppato per scopi educativi.

## Autore

Federico Scarcella - 3CI 2023-24

## Supporto

Per problemi o domande, aprire un issue nel repository GitHub.
