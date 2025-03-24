// Stato iniziale e variabili globali
let livello = 1; // Livello attuale
let saldo = 50000; // Saldo iniziale
let livelloMassimo = 1; // Memorizza il livello massimo raggiunto
let magazzino = []; // Magazzino per le porte acquistate
let venditaIncremento = 20; // Percentuale di incremento per la vendita
let agentiAcquistati = []; // Lista di agenti immobiliari acquistati
let registroVendite = []; // Cronologia di tutte le operazioni (compere, vendite, ecc.)

// Riferimenti agli elementi del DOM
const bottoneApriComputer = document.getElementById('apri-computer');
const schermataComputer = document.getElementById('schermata-computer');
const pulsanteChiudi = document.getElementById('pulsante-chiudi');
const displayLivello = document.getElementById('livello');
const displaySaldo = document.getElementById('saldo');
const bottoneMostraPorte = document.getElementById('mostra-porte');
const bottoneMostraCase = document.getElementById('mostra-case');
const bottoneMostraAgenti = document.getElementById('mostra-agenti');
const bottoneMostraMagazzino = document.getElementById('mostra-magazzino');
const bottoneRegistroVendite = document.getElementById('registro-vendite');
const contenitorePc = document.getElementById('schermo-pc');

// Dati simulati delle porte, case e agenti immobiliari
const portaDati = [
  { id: 1, prezzo: 1000, immagine: '/immage/porta_inglese.png', nome: 'Porta 1' },
  { id: 2, prezzo: 3000, immagine: '/immage/porta_italiano.png', nome: 'Porta 2' },
  { id: 3, prezzo: 5000, immagine: '/immage/porta_moderna.png', nome: 'Porta 3' },
  { id: 4, prezzo: 7000, immagine: '/immage/porta_orientale.png', nome: 'Porta 4' },
  { id: 5, prezzo: 9000, immagine: '/immage/porta_gotica.png', nome: 'Porta 5' },
  { id: 6, prezzo: 12000, immagine: '/immage/porta_blindata.png', nome: 'Porta 6' }
];

const caseDati = [
  { id: 1, prezzo: 20000, immagine: '/immage/casa_classica.png', nome: 'Casa 1' },
  { id: 2, prezzo: 30000, immagine: '/immage/casa_moderna.png', nome: 'Casa 2' },
  { id: 3, prezzo: 40000, immagine: '/immage/casa_lussuosa.png', nome: 'Casa 3' }
];

const agentiDati = [
  { id: 1, nome: 'Agente Alpha', prezzo: 2000, professionalita: 80, trattativa: 70, percentuale: 10 },
  { id: 2, nome: 'Agente Beta', prezzo: 3000, professionalita: 90, trattativa: 60, percentuale: 15 },
  { id: 3, nome: 'Agente Gamma', prezzo: 2500, professionalita: 75, trattativa: 80, percentuale: 12 }
];
// Funzione per aggiornare il livello in base al saldo
function aggiornaLivello() {
  if (saldo >= 100000) {
    livello = 3;
  } else if (saldo >= 10000) {
    livello = 2;
  } else {
    livello = 1;
  }

  // Memorizza il livello massimo raggiunto
  if (livello > livelloMassimo) {
    livelloMassimo = livello;
  }

  // Imposta il livello attuale al massimo raggiunto
  livello = livelloMassimo;

  // Aggiorna la visualizzazione del livello
  displayLivello.textContent = livello;
}

// Mostra le porte disponibili
function mostraPorte() {
  contenitorePc.innerHTML = '';
  portaDati.forEach((porta) => {
    const elementoPorta = document.createElement('div');
    elementoPorta.classList.add('contenitore-porta');
    elementoPorta.innerHTML = `
      <img src="${porta.immagine}" alt="${porta.nome}">
      <p>${porta.nome}</p>
      <p>Prezzo: €${porta.prezzo}</p>
      <button class="compra-btn" data-id="${porta.id}" data-prezzo="${porta.prezzo}">Compra</button>
    `;
    contenitorePc.appendChild(elementoPorta);
  });

  const compraBtns = document.querySelectorAll('.compra-btn');
  compraBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const idPorta = parseInt(btn.getAttribute('data-id'));
      const prezzoPorta = parseFloat(btn.getAttribute('data-prezzo'));
      compraPorta(idPorta, prezzoPorta);
    });
  });
}

// Acquista una porta
function compraPorta(idPorta, prezzoPorta) {
  if (magazzino.length >= 10) {
    alert('Il magazzino è pieno! Capienza massima: 10 porte.');
    return;
  }
  if (saldo < prezzoPorta) {
    alert('Saldo insufficiente per acquistare questa porta.');
    return;
  }
  saldo -= prezzoPorta;
  displaySaldo.textContent = saldo.toFixed(2);
  const portaAcquistata = portaDati.find(porta => porta.id === idPorta);
  if (portaAcquistata) {
    magazzino.push(portaAcquistata);
    registroVendite.push(`Hai acquistato una porta: ${portaAcquistata.nome}. Prezzo: €${prezzoPorta}.`);
    alert(`Hai acquistato ${portaAcquistata.nome}.`);
    aggiornaLivello();
  }
}

// Mostra il contenuto del magazzino
function mostraMagazzino() {
  contenitorePc.innerHTML = '';
  if (magazzino.length === 0) {
    contenitorePc.innerHTML = '<p>Il magazzino è vuoto.</p>';
  } else {
    magazzino.forEach((item, indice) => {
      const prezzoVendita = item.prezzo + (item.prezzo * venditaIncremento / 100);
      const elementoItem = document.createElement('div');
      elementoItem.classList.add('contenitore-porta');
      elementoItem.innerHTML = `
        <img src="${item.immagine}" alt="${item.nome}">
        <p>${item.nome}</p>
        <p>Prezzo originale: €${item.prezzo}</p>
        <p>Prezzo di vendita: €${prezzoVendita.toFixed(2)}</p>
        <button class="vendi-btn" data-indice="${indice}" data-vendita="${prezzoVendita}">Vendi</button>
      `;
      contenitorePc.appendChild(elementoItem);
    });
    const vendiBtns = document.querySelectorAll('.vendi-btn');
    vendiBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const indice = parseInt(btn.getAttribute('data-indice'));
        const prezzoVendita = parseFloat(btn.getAttribute('data-vendita'));
        vendiPorta(indice, prezzoVendita);
      });
    });
  }
}

// Mostra la cronologia di tutte le operazioni
function mostraRegistroVendite() {
  contenitorePc.innerHTML = '<h3>Registro Vendite</h3>';
  registroVendite.forEach((operazione) => {
    const elementoOperazione = document.createElement('p');
    elementoOperazione.textContent = operazione;
    contenitorePc.appendChild(elementoOperazione);
  });
}
// Event listener per la schermata computer
bottoneApriComputer.addEventListener('click', () => {
  schermataComputer.classList.remove('nascosto');
});

pulsanteChiudi.addEventListener('click', () => {
  schermataComputer.classList.add('nascosto');
});

// Event listener per mostrare porte, case, magazzino e registro vendite
bottoneMostraPorte.addEventListener('click', mostraPorte);
bottoneMostraCase.addEventListener('click', () => {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione case.");
    return;
  }
  mostraCase();
});
bottoneMostraAgenti.addEventListener('click', () => {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione agenti immobiliari.");
    return;
  }
  mostraAgenti();
});
bottoneMostraMagazzino.addEventListener('click', mostraMagazzino);
bottoneRegistroVendite.addEventListener('click', mostraRegistroVendite);

// Mostra saldo iniziale
displaySaldo.textContent = saldo.toFixed(2);

// Funzione per mostrare le case disponibili
function mostraCase() {
  contenitorePc.innerHTML = '';
  caseDati.forEach((casa) => {
    const elementoCasa = document.createElement('div');
    elementoCasa.classList.add('contenitore-porta');
    elementoCasa.innerHTML = `
      <img src="${casa.immagine}" alt="${casa.nome}">
      <p>${casa.nome}</p>
      <p>Prezzo: €${casa.prezzo}</p>
      <button class="compra-casa-btn" data-id="${casa.id}" data-prezzo="${casa.prezzo}">Compra</button>
    `;
    contenitorePc.appendChild(elementoCasa);
  });

  const compraCasaBtns = document.querySelectorAll('.compra-casa-btn');
  compraCasaBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const idCasa = parseInt(btn.getAttribute('data-id'));
      const prezzoCasa = parseFloat(btn.getAttribute('data-prezzo'));
      compraCasa(idCasa, prezzoCasa);
    });
  });
}

// Funzione per acquistare una casa
function compraCasa(idCasa, prezzoCasa) {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per acquistare una casa.");
    return;
  }
  if (saldo < prezzoCasa) {
    alert('Saldo insufficiente per acquistare questa casa.');
    return;
  }
  if (agentiAcquistati.length === 0) {
    alert('Devi acquistare almeno un agente immobiliare per procedere con l\'acquisto di una casa.');
    return;
  }

  saldo -= prezzoCasa;
  displaySaldo.textContent = saldo.toFixed(2);
  const casaAcquistata = caseDati.find(casa => casa.id === idCasa);
  if (casaAcquistata) {
    alert(`Hai acquistato ${casaAcquistata.nome}. La vendita sarà gestita automaticamente.`);
    registroVendite.push(`Hai acquistato una casa: ${casaAcquistata.nome}. Prezzo: €${prezzoCasa}.`);
    aggiornaLivello();

    // Assegna la casa al primo agente disponibile
    const agenteDisponibile = agentiAcquistati.find(agente => !agente.tempoRimanente || agente.tempoRimanente <= 0);
    if (agenteDisponibile) {
      iniziaVenditaCasa(agenteDisponibile, casaAcquistata);
    } else {
      alert('Tutti gli agenti sono attualmente impegnati nella vendita. La casa sarà venduta quando un agente sarà disponibile.');
    }
  }
}

// Avvia la vendita automatica della casa
function iniziaVenditaCasa(agente, casa) {
  const tempoVendita = Math.floor(Math.random() * (180000 - 60000 + 1)) + 60000; // Tempo randomico tra 1 e 3 minuti
  agente.tempoRimanente = tempoVendita;

  const prezzoVenditaCasa = casa.prezzo + (casa.prezzo * venditaIncremento / 100);
  const commissione = prezzoVenditaCasa * (agente.percentuale / 100);
  const guadagnoNetto = prezzoVenditaCasa - commissione;

  // Aggiorna la barra di progresso dinamicamente
  registroVendite.push(`Vendita iniziata: ${casa.nome} assegnata all'agente ${agente.nome}. Prezzo previsto: €${prezzoVenditaCasa.toFixed(2)}.`);
  const idBarra = `progresso-${agente.id}`;
  const barraProgresso = document.createElement('div');
  barraProgresso.id = idBarra;
  barraProgresso.className = 'barra-progresso';
  barraProgresso.style.width = '0%';
  contenitorePc.appendChild(barraProgresso);

  const intervallo = setInterval(() => {
    agente.tempoRimanente -= 1000; // Aggiorna ogni secondo
    const percentuale = ((tempoVendita - agente.tempoRimanente) / tempoVendita) * 100;

    // Aggiorna barra di progresso
    barraProgresso.style.width = `${percentuale}%`;
    barraProgresso.textContent = `${Math.round(percentuale)}%`;

    if (agente.tempoRimanente <= 0) {
      clearInterval(intervallo); // Ferma il timer
      saldo += guadagnoNetto;
      displaySaldo.textContent = saldo.toFixed(2);
      registroVendite.push(`Vendita completata: ${casa.nome}. Guadagno netto: €${guadagnoNetto.toFixed(2)}.`);
      alert(`La casa ${casa.nome} è stata venduta per €${prezzoVenditaCasa.toFixed(2)}.
Commissione dell'agente: €${commissione.toFixed(2)}.
Guadagno netto: €${guadagnoNetto.toFixed(2)}.`);
      aggiornaLivello();
      agente.tempoRimanente = 0; // L'agente è ora disponibile
    }
  }, 1000);
}
