# Guida Rapida

Questa guida ti aiuterà ad avviare rapidamente il Sistema di Riconoscimento Facciale.

## 🚀 Avvio Rapido (Windows)

### Opzione 1: Script Automatico

```cmd
# 1. Installa (solo la prima volta)
install_dependencies.bat

# 2. Avvia l'applicazione
run.bat
```

### Opzione 2: Manuale

```cmd
# 1. Attiva ambiente virtuale
venv\Scripts\activate.bat

# 2. Avvia applicazione
python main.py
```

## 🐧 Avvio Rapido (Linux/macOS)

```bash
# 1. Crea ambiente virtuale (solo la prima volta)
python3 -m venv venv

# 2. Attiva ambiente virtuale
source venv/bin/activate

# 3. Installa dipendenze (solo la prima volta)
pip install -r requirements.txt

# 4. Avvia applicazione
python main.py
```

## 📖 Primo Utilizzo

### 1. Avvia la Camera
- Clicca su **"Avvia Camera"** nel pannello di sinistra
- La webcam si attiverà e inizierà il rilevamento volti

### 2. Registra il Primo Utente
- Clicca su **"Aggiungi Utente"** nel pannello di destra
- Inserisci nome e cognome
- Carica una foto del volto
- Clicca **"OK"**

### 3. Testa il Riconoscimento
- Mettiti davanti alla camera
- Il sistema dovrebbe riconoscerti e mostrare il tuo nome

## 🎯 Funzioni Principali

### Pannello Sinistra (Camera)
- **Avvia Camera**: Attiva la webcam
- **Ferma Camera**: Disattiva la webcam
- **Live Preview**: Mostra i volti rilevati in tempo reale
- **Nome + Confidenza**: Per volti riconosciuti
- **"Sconosciuto"**: Per volti non registrati

### Pannello Destra (Gestione)
- **Lista Utenti**: Mostra tutti gli utenti registrati
- **Aggiungi Utente**: Registra un nuovo utente
- **Elimina Utente**: Rimuove un utente selezionato
- **Aggiorna Lista**: Ricarica la lista dal database

## ⚙️ Impostazioni Rapide

### Cambiare Camera
Modifica `config.py`:
```python
CAMERA_INDEX = 0  # Cambia a 1, 2, etc. per altre camere
```

### Regolare Sensibilità
Modifica `config.py`:
```python
# Più basso = più rigido (raccomandato: 0.5-0.7)
FACE_RECOGNITION_THRESHOLD = 0.6
```

### Migliorare Performance
Modifica `config.py`:
```python
# Riduci risoluzione
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
```

## 🔧 Problemi Comuni

### Camera non funziona
1. Chiudi altre app che usano la camera
2. Prova `CAMERA_INDEX = 1` in `config.py`
3. Verifica permessi camera

### Riconoscimento lento
1. Chiudi altre applicazioni
2. Riduci risoluzione in `config.py`
3. Usa una GPU se disponibile

### Riconoscimento impreciso
1. Migliora illuminazione
2. Mantieni volto frontale
3. Regola `FACE_RECOGNITION_THRESHOLD`

## 📚 Documentazione Completa

- **README.md**: Panoramica completa del progetto
- **SETUP.md**: Istruzioni dettagliate di installazione
- **Menu Aiuto → Informazioni**: Info sull'applicazione

## 💡 Suggerimenti

✅ **DO**:
- Usa buona illuminazione
- Mantieni volto frontale
- Registra con foto di qualità
- Fai backup del database

❌ **DON'T**:
- Non registrare stessa persona più volte
- Non usare foto sfocate
- Non usare in condizioni di scarsa luce

## 🆘 Aiuto

Hai problemi? Consulta:
1. Questa guida rapida
2. `SETUP.md` per problemi di installazione
3. `README.md` per informazioni complete
4. Apri una issue su GitHub

---

Buon utilizzo! 🎉
