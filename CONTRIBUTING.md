# Contribuire al Progetto

Grazie per il tuo interesse nel contribuire al Sistema di Riconoscimento Facciale! 

## 🤝 Come Contribuire

### Segnalare Bug

Se trovi un bug, per favore:
1. Verifica che non sia già stato segnalato nelle [Issues](https://github.com/3CI-SCARCELLA-FEDERICO-2023-24/sito/issues)
2. Apri una nuova issue con:
   - Titolo descrittivo
   - Passi per riprodurre il bug
   - Comportamento atteso vs comportamento effettivo
   - Versione Python e sistema operativo
   - Screenshot se rilevante

### Suggerire Funzionalità

Per suggerire nuove funzionalità:
1. Apri una issue con tag `enhancement`
2. Descrivi la funzionalità proposta
3. Spiega perché sarebbe utile
4. Se possibile, suggerisci un'implementazione

### Contribuire Codice

1. **Fork** il repository
2. **Crea** un branch per la tua funzionalità: `git checkout -b feature/nome-funzionalita`
3. **Implementa** le modifiche
4. **Testa** il codice
5. **Commit** con messaggi descrittivi
6. **Push** al tuo fork
7. Apri una **Pull Request**

## 📝 Linee Guida per il Codice

### Stile Python

- Segui [PEP 8](https://peps.python.org/pep-0008/)
- Usa docstring per funzioni e classi
- Commenta il codice complesso
- Mantieni funzioni brevi e focalizzate

### Esempio di Docstring

```python
def funzione_esempio(parametro1: str, parametro2: int) -> bool:
    """
    Breve descrizione della funzione.
    
    Args:
        parametro1: Descrizione del primo parametro
        parametro2: Descrizione del secondo parametro
        
    Returns:
        Descrizione del valore di ritorno
        
    Raises:
        ValueError: Quando il parametro non è valido
    """
    pass
```

### Commit Messages

- Usa il presente: "Add feature" non "Added feature"
- Sii descrittivo ma conciso
- Raggruppa modifiche logicamente correlate

Esempi:
```
Add face recognition threshold configuration
Fix camera preview aspect ratio bug
Update README with installation instructions
```

### Testing

- Testa manualmente tutte le modifiche
- Verifica che non ci siano regressioni
- Assicurati che il codice funzioni su Windows/Linux/macOS

## 🏗️ Aree di Sviluppo

Aree dove contributi sono particolarmente benvenuti:

### Alta Priorità
- [ ] Test automatizzati
- [ ] Supporto per database remoti
- [ ] Miglioramento performance
- [ ] Documentazione API

### Media Priorità
- [ ] Temi UI personalizzabili
- [ ] Esportazione/importazione database
- [ ] Statistiche di utilizzo
- [ ] Multi-lingua

### Bassa Priorità
- [ ] Plugin system
- [ ] Notifiche desktop
- [ ] Logging avanzato
- [ ] Dashboard web

## 🔍 Processo di Review

Le Pull Request saranno revisionate per:
- Qualità del codice
- Aderenza alle linee guida
- Funzionalità e test
- Documentazione

## 📧 Comunicazione

- **GitHub Issues**: Per bug e funzionalità
- **Pull Requests**: Per contributi codice
- **Discussions**: Per domande generali

## 📜 Licenza

Contribuendo, accetti che i tuoi contributi saranno rilasciati sotto la licenza MIT del progetto.

## 🙏 Riconoscimenti

Tutti i contributori saranno riconosciuti nel README.

Grazie per il tuo contributo! 🎉
