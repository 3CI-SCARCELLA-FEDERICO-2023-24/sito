# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.1] - 2024-02-16

### Sicurezza
- **CRITICO**: Aggiornato keras da 2.15.0 a >=3.13.1 per risolvere:
  - Directory traversal vulnerability (CVE) - RISOLTO
  - Path traversal in keras.utils.get_file API - RISOLTO
  - Deserialization of untrusted data vulnerability - RISOLTO
  - Arbitrary code execution vulnerability - RISOLTO
  - Allocates resources without limits in HDF5 component - RISOLTO
- **CRITICO**: Aggiornato torch da 2.1.2 a >=2.6.0 per risolvere:
  - Heap buffer overflow vulnerability - RISOLTO
  - Use-after-free vulnerability - RISOLTO
  - Remote code execution via torch.load - RISOLTO
  - Deserialization vulnerability - RISOLTO
- **ALTO**: Aggiornato Pillow da 10.2.0 a >=10.3.0 per risolvere:
  - Buffer overflow vulnerability - RISOLTO
- Aggiornato tensorflow a >=2.16.0 per compatibilità con keras 3.x
- Aggiornato torchvision a >=0.19.0 per compatibilità con torch 2.6+

### Note di Sicurezza
- Keras 3.13.1 ha una vulnerabilità nota: "Arbitrary file read in HDF5 weight loading"
  - Impatto: Solo se si caricano modelli HDF5 non fidati
  - Mitigazione: Non caricare modelli da fonti non attendibili
  - Patch: Non ancora disponibile
  - Questa applicazione non carica modelli HDF5 esterni, quindi non è a rischio

### Note di Aggiornamento
- Gli utenti devono aggiornare le dipendenze eseguendo: `pip install -r requirements.txt --upgrade`
- La maggior parte delle vulnerabilità critiche sono state risolte
- La compatibilità dell'applicazione è stata mantenuta

## [1.0.0] - 2024-02-16

### Aggiunto
- Sistema completo di riconoscimento facciale
- Interfaccia grafica PyQt6 con preview camera e gestione utenti
- Rilevamento volti in tempo reale con MediaPipe
- Generazione embeddings facciali con FaceNet
- Database SQLite per gestione utenti e embeddings
- Sistema di matching per confronto volti
- Registrazione automatica volti sconosciuti
- Gestione duplicati intelligente
- Pannello di gestione utenti (aggiungi, elimina, visualizza)
- Configurazioni personalizzabili
- Supporto per camera preview con annotazioni
- Sistema di confidence score per riconoscimenti
- Documentazione completa (README, SETUP, QUICKSTART)
- Script di installazione automatica per Windows
- Script di test per verificare l'installazione
- Licenza MIT
- Linee guida per contribuire

### Caratteristiche
- Riconoscimento in tempo reale con bassa latenza
- Supporto per riconoscimento con e senza occhiali
- Interfaccia utente intuitiva e moderna
- Database locale con privacy garantita
- Performance ottimizzate per uso desktop
- Cross-platform (Windows, Linux, macOS)

### Tecnologie Utilizzate
- Python 3.10+
- PyQt6 per l'interfaccia grafica
- OpenCV per elaborazione immagini
- MediaPipe per rilevamento volti
- FaceNet (PyTorch) per embeddings
- SQLite per database
- NumPy per calcoli numerici

### File Creati
- `main.py` - Entry point dell'applicazione
- `config.py` - Configurazioni globali
- `database/db_manager.py` - Gestione database SQLite
- `face_recognition/face_detector.py` - Rilevamento volti
- `face_recognition/face_encoder.py` - Generazione embeddings
- `face_recognition/face_matcher.py` - Confronto volti
- `ui/main_window.py` - Finestra principale
- `ui/camera_preview.py` - Preview camera
- `ui/management_panel.py` - Gestione utenti
- `models/download_models.py` - Download modelli
- `requirements.txt` - Dipendenze
- `setup.py` - Setup script
- `install_dependencies.bat` - Installazione Windows
- `run.bat` - Esecuzione Windows
- `test_installation.py` - Test installazione
- `README.md` - Documentazione principale
- `SETUP.md` - Guida installazione dettagliata
- `QUICKSTART.md` - Guida rapida
- `CONTRIBUTING.md` - Linee guida contribuzione
- `CHANGELOG.md` - Questo file
- `LICENSE` - Licenza MIT
- `.gitignore` - File da escludere

### Note di Sviluppo
- Prima release stabile
- Testato su Windows 10/11
- Supporto sperimentale per Linux e macOS
- Richiede webcam funzionante
- Richiede almeno 4GB RAM

---

## [Unreleased]

### Pianificato
- Test automatizzati
- Supporto database remoti
- Temi UI personalizzabili
- Esportazione/importazione database
- Multi-lingua
- Statistiche di utilizzo
- Miglioramenti performance
- Documentazione API

---

**Legenda:**
- `Aggiunto` - Nuove funzionalità
- `Modificato` - Modifiche a funzionalità esistenti
- `Deprecato` - Funzionalità che saranno rimosse
- `Rimosso` - Funzionalità rimosse
- `Corretto` - Bug fix
- `Sicurezza` - Correzioni di vulnerabilità
