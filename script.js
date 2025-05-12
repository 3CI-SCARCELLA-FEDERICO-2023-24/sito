// Stato iniziale e variabili globali
let livello = 1; // Livello attuale
let saldo = 2200; // Saldo iniziale
let livelloMassimo = 1; // Memorizza il livello massimo raggiunto
let magazzino = []; // Magazzino per le porte acquistate
let venditaIncremento = 40; // Percentuale di incremento per la vendita
let agentiAcquistati = []; // Lista di agenti immobiliari acquistati

/*-------------------------------------------*/

/* === INIZIALIZZAZIONE DELLE VARIABILI PER LE GUIDE === */
let guidaPorteMostrata = false;
let guidaCaseMostrata = false;
let guidaAgentiMostrata = false;
let guidaMagazzinoMostrata = false;

let guidaPortaComprataMostrata = false;
let guidaCasaComprataMostrata = false;
let guidaAgenteCompratoMostrata = false;
let guidaVendiMostrata = false;

let instructionCallback = null;

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
const contenitorePc = document.getElementById('schermo-pc');

// Dati delle porte
const portaDati = [
  { id: 1, prezzo: 1000, immagine: '\immage/porta_inglese.png', nome: 'Porta inglese' },
  { id: 2, prezzo: 3000, immagine: '\immage/porta_italiano.png', nome: 'Porta italiana' },
  { id: 3, prezzo: 5000, immagine: '\immage/porta_moderna.png', nome: 'Porta moderna' },
  { id: 4, prezzo: 7000, immagine: '\immage/porta_orientale.png', nome: 'Porta orientale' },
  { id: 5, prezzo: 9000, immagine: '\immage/porta_gotica.png', nome: 'Porta gotica' },
  { id: 6, prezzo: 12000, immagine: '\immage/porta_blindata.png', nome: 'Porta blindata' }
];

// Dati delle case
const caseDati = [
  { id: 1, prezzo: 20000, immagine: '\immage/casa_campagna.jpg', nome: 'Casa di campagna' },
  { id: 2, prezzo: 30000, immagine: '\immage/casa_media.jpg', nome: 'Casa popolare' },
  { id: 3, prezzo: 40000, immagine: '\immage/casa_moderna.jpg', nome: 'Casa moderna' }
];

// Dati degli agenti immobiliari
const agentiDati = [
  { id: 1, nome: 'Alberto', prezzo: 2000, professionalita: 80, trattativa: 70, percentuale: 10 },
  { id: 2, nome: 'Carlo', prezzo: 3000, professionalita: 90, trattativa: 60, percentuale: 15 },
  { id: 3, nome: 'Chiara', prezzo: 2500, professionalita: 75, trattativa: 80, percentuale: 12 }
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
  inflazione(portaDati); // Per le porte
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

// Vendi una porta
function vendiPorta(indice, prezzoVendita) {
  if (indice < magazzino.length) {
    saldo += prezzoVendita;
    magazzino.splice(indice, 1);
    displaySaldo.textContent = saldo.toFixed(2);
    aggiornaLivello();
    alert(`Hai venduto la porta per €${prezzoVendita.toFixed(2)}.`);
    mostraMagazzino();
  }
}

// Mostra le case disponibili
function mostraCase() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione case.");
    return;
  }
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
  inflazione(caseDati);  // Per le case
}

// Acquista una casa
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

// Avvia la vendita automatica della casa con un agente
function iniziaVenditaCasa(agente, casa) {
  const tempoVendita = Math.floor(Math.random() * (180000 - 60000 + 1)) + 60000; // Tempo randomico tra 1 e 3 minuti
  agente.tempoRimanente = tempoVendita;
  const prezzoVenditaCasa = casa.prezzo + (casa.prezzo * venditaIncremento / 100);
  const commissione = prezzoVenditaCasa * (agente.percentuale / 100);
  const guadagnoNetto = prezzoVenditaCasa - commissione;
  // Aggiorna la barra di progresso dinamicamente
  const idBarra = `progresso-${agente.id}`;
  const barraProgresso = document.getElementById(idBarra);
  const intervallo = setInterval(() => {
    agente.tempoRimanente -= 1000; // Aggiorna ogni secondo
    const percentuale = ((tempoVendita - agente.tempoRimanente) / tempoVendita) * 100;
    if (barraProgresso) {
      barraProgresso.style.width = `${percentuale}%`;
      barraProgresso.textContent = `${Math.round(percentuale)}%`;
    }
    if (agente.tempoRimanente <= 0) {
      clearInterval(intervallo); // Ferma il timer
      saldo += guadagnoNetto;
      displaySaldo.textContent = saldo.toFixed(2);
      alert(`La casa ${casa.nome} è stata venduta per €${prezzoVenditaCasa.toFixed(2)}.
Commissione dell'agente: €${commissione.toFixed(2)}.
Guadagno netto: €${guadagnoNetto.toFixed(2)}.`);
      aggiornaLivello();
      agente.tempoRimanente = 0; // L'agente è ora disponibile
    }
  }, 1000);
}

/* —— GESTIONE DEGLI AGENTI IMMOBILIARI —— */
// Mostra gli agenti immobiliari acquistati e disponibili
function mostraAgenti() {   
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione agenti immobiliari.");
    return;
  }
  contenitorePc.innerHTML = ''; // Pulisce il contenitore
  // Sezione degli agenti acquistati
  if (agentiAcquistati.length > 0) {
    const titoloAcquistati = document.createElement('h3');
    titoloAcquistati.textContent = 'Agenti Acquistati';
    contenitorePc.appendChild(titoloAcquistati);
    agentiAcquistati.forEach(agente => {
      const elementoAgente = document.createElement('div');
      elementoAgente.classList.add('contenitore-porta');
      elementoAgente.innerHTML = `
        <p>${agente.nome}</p>
        <p>Professionalità: ${agente.professionalita}</p>
        <p>Trattativa: ${agente.trattativa}</p>
        <p>Commissione: ${agente.percentuale}%</p>
        <div class="barra-progresso-container">
          <div class="barra-progresso" id="progresso-${agente.id}" style="width: 0%;"></div>
        </div>
      `;
      contenitorePc.appendChild(elementoAgente);
      // Aggiorna dinamicamente la barra di progresso
      const barraProgresso = document.getElementById(`progresso-${agente.id}`);
      aggiornaBarraProgresso(barraProgresso, agente.tempoRimanente);
    });
  }
  // Sezione degli agenti disponibili
  const titoloDisponibili = document.createElement('h3');
  titoloDisponibili.textContent = 'Agenti Disponibili';
  contenitorePc.appendChild(titoloDisponibili);
  agentiDati.forEach(agente => {
    const elementoAgente = document.createElement('div');
    elementoAgente.classList.add('contenitore-porta');
    elementoAgente.innerHTML = `
      <p>${agente.nome}</p>
      <p>Prezzo: €${agente.prezzo}</p>
      <p>Professionalità: ${agente.professionalita}</p>
      <p>Trattativa: ${agente.trattativa}</p>
      <p>Commissione: ${agente.percentuale}%</p>
      <button class="compra-agente-btn" data-id="${agente.id}" data-prezzo="${agente.prezzo}">Compra Agente</button>
    `;
    contenitorePc.appendChild(elementoAgente);
  });
  const compraAgenteBtns = document.querySelectorAll('.compra-agente-btn');
  compraAgenteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const idAgente = parseInt(btn.getAttribute('data-id'));
      const prezzoAgente = parseFloat(btn.getAttribute('data-prezzo'));
      compraAgente(idAgente, prezzoAgente);
    });
  });
  inflazione(agentiDati); // Per gli agenti 
}

// Acquista un agente immobiliare
function compraAgente(idAgente, prezzoAgente) {
  if (saldo < prezzoAgente) {
    alert('Saldo insufficiente per acquistare questo agente.');
    return;
  }
  saldo -= prezzoAgente;
  displaySaldo.textContent = saldo.toFixed(2);
  const agente = agentiDati.find(a => a.id === idAgente);
  if (agente) {
    agentiAcquistati.push({ ...agente, tempoRimanente: 0 }); // Aggiungi l'agente alla lista
    alert(`Hai acquistato l'agente immobiliare ${agente.nome}. Ora puoi utilizzarlo per vendere case.`);
  }
}

// Aggiorna dinamicamente la barra di progresso
function aggiornaBarraProgresso(barraProgresso, tempoRimanente) {
  if (tempoRimanente <= 0) {
    barraProgresso.style.width = '100%';
    barraProgresso.textContent = 'Vendita completata!';
  } else {
    const percentuale = ((180000 - tempoRimanente) / 180000) * 100; // Calcola la percentuale
    barraProgresso.style.width = `${percentuale}%`;
    barraProgresso.textContent = `${Math.round(percentuale)}%`;
  }
}

// inflazione
function inflazione(dati) {
  // Salva i prezzi originali
  const prezziOriginali = dati.map(item => item.prezzo);
  // Funzione per generare un incremento casuale
  const incrementoCasuale = () => Math.floor(Math.random() * 300 + 1);
  // Aumenta il prezzo casualmente
  dati.forEach(item => {
    item.prezzo += incrementoCasuale();
  });
  console.log("Prezzi aumentati:", dati);
  // Timer per riportare il prezzo casualmente al valore originale
  setTimeout(() => {
    dati.forEach((item, index) => {
      item.prezzo = prezziOriginali[index];
    });
    console.log("Prezzi ripristinati:", dati);
  }, Math.random() * 2000 + 500); // Tempo di attesa casuale tra 2-7 secondi
}

// Event listener per la schermata computer
bottoneApriComputer.addEventListener('click', () => {
  schermataComputer.classList.remove('nascosto');
  // Mostra il modal informativo
  document.getElementById('infoModal').style.display = 'block';
});

pulsanteChiudi.addEventListener('click', () => {
  schermataComputer.classList.add('nascosto');
});

bottoneMostraPorte.addEventListener('click', mostraPorte);
bottoneMostraCase.addEventListener('click', mostraCase);
bottoneMostraAgenti.addEventListener('click', mostraAgenti);
bottoneMostraMagazzino.addEventListener('click', mostraMagazzino);

// Event listener per il pulsante OK del modal
document.getElementById('modalOk').addEventListener('click', () => {
  document.getElementById('infoModal').style.display = 'none';
});

// Imposta saldo iniziale
displaySaldo.textContent = saldo.toFixed(2);

/*---------------------------------------------------------------*/

/* === FUNZIONE PER MOSTRARE LA MODALE ISTRUTTIVA === */
function showInstructionModal(message, callback) {
  const modal = document.getElementById('infoModal');
  modal.querySelector('.modal-content p').innerHTML = message;
  instructionCallback = callback || null;
  modal.style.display = 'block';
}

document.getElementById('modalOk').addEventListener('click', function() {
  const modal = document.getElementById('infoModal');
  modal.style.display = 'none';
  if (instructionCallback) {
    instructionCallback();
    instructionCallback = null;
  }
});


/* WRAPPING DELLE FUNZIONI PER MOSTRARE LE SEZIONI CON GUIDA */

/* Sezione "Porte" */
function mostraPorte() {
  if (!guidaPorteMostrata) {
    guidaPorteMostrata = true;
    showInstructionModal(
      "Premi il tasto <strong>ACQUISTA PORTE</strong> per acquistare delle porte e iniziare la tua prima vendita.",
      function() {
        actuallyShowPorte();
      }
    );
  } else {
    actuallyShowPorte();
  }
}

function actuallyShowPorte() {
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
  inflazione(portaDati);
}


/* Sezione "Case" */
function mostraCase() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione case.");
    return;
  }
  if (!guidaCaseMostrata) {
    guidaCaseMostrata = true;
    showInstructionModal(
      "Premi il tasto <strong>ACQUISTA CASE</strong> per acquistare una casa e avviare la vendita automatica.",
      function() {
        actuallyShowCase();
      }
    );
  } else {
    actuallyShowCase();
  }
}

function actuallyShowCase() {
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
  inflazione(caseDati);
}


/* Sezione "Agenti Immobiliari" */
function mostraAgenti() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione agenti immobiliari.");
    return;
  }
  if (!guidaAgentiMostrata) {
    guidaAgentiMostrata = true;
    showInstructionModal(
      "Premi il tasto <strong>COMPRA AGENTE</strong> per acquistare un agente immobiliare che ti aiuterà a vendere le case.",
      function() {
        actuallyShowAgenti();
      }
    );
  } else {
    actuallyShowAgenti();
  }
}

function actuallyShowAgenti() {
  contenitorePc.innerHTML = '';
  if (agentiAcquistati.length > 0) {
    const titoloAcquistati = document.createElement('h3');
    titoloAcquistati.textContent = 'Agenti Acquistati';
    contenitorePc.appendChild(titoloAcquistati);
    agentiAcquistati.forEach(agente => {
      const elementoAgente = document.createElement('div');
      elementoAgente.classList.add('contenitore-porta');
      elementoAgente.innerHTML = `
        <p>${agente.nome}</p>
        <p>Professionalità: ${agente.professionalita}</p>
        <p>Trattativa: ${agente.trattativa}</p>
        <p>Commissione: ${agente.percentuale}%</p>
        <div class="barra-progresso-container">
          <div class="barra-progresso" id="progresso-${agente.id}" style="width: 0%;"></div>
        </div>
      `;
      contenitorePc.appendChild(elementoAgente);
      const barraProgresso = document.getElementById(`progresso-${agente.id}`);
      aggiornaBarraProgresso(barraProgresso, agente.tempoRimanente);
    });
  }
  const titoloDisponibili = document.createElement('h3');
  titoloDisponibili.textContent = 'Agenti Disponibili';
  contenitorePc.appendChild(titoloDisponibili);
  agentiDati.forEach(agente => {
    const elementoAgente = document.createElement('div');
    elementoAgente.classList.add('contenitore-porta');
    elementoAgente.innerHTML = `
      <p>${agente.nome}</p>
      <p>Prezzo: €${agente.prezzo}</p>
      <p>Professionalità: ${agente.professionalita}</p>
      <p>Trattativa: ${agente.trattativa}</p>
      <p>Commissione: ${agente.percentuale}%</p>
      <button class="compra-agente-btn" data-id="${agente.id}" data-prezzo="${agente.prezzo}">Compra Agente</button>
    `;
    contenitorePc.appendChild(elementoAgente);
  });
  const compraAgenteBtns = document.querySelectorAll('.compra-agente-btn');
  compraAgenteBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const idAgente = parseInt(btn.getAttribute('data-id'));
      const prezzoAgente = parseFloat(btn.getAttribute('data-prezzo'));
      compraAgente(idAgente, prezzoAgente);
    });
  });
  inflazione(agentiDati);
}


/* Sezione "Magazzino" */
function mostraMagazzino() {
  if (!guidaMagazzinoMostrata) {
    guidaMagazzinoMostrata = true;
    showInstructionModal(
      "Questo è il tuo <strong>MAGAZZINO</strong>. Qui troverai le porte acquistate e potrai venderle quando il loro prezzo cresce.",
      function() {
        actuallyShowMagazzino();
      }
    );
  } else {
    actuallyShowMagazzino();
  }
}

function actuallyShowMagazzino() {
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


/* WRAPPING DELLE FUNZIONI PER LE AZIONI SUI PULSANTI */

/* Acquisto di una Porta */
/* La funzione "compraPorta" già esistente mostra il messaggio:
   "La porta acquistata la potrai trovare cliccando sul MAGAZZINO."
   se non ancora mostrato, altrimenti procede normalmente. */


/* Acquisto di un Agente Immobiliare */
function compraAgente(idAgente, prezzoAgente) {
  if (saldo < prezzoAgente) {
    alert('Saldo insufficiente per acquistare questo agente.');
    return;
  }
  if (!guidaAgenteCompratoMostrata) {
    guidaAgenteCompratoMostrata = true;
    showInstructionModal(
      "Hai acquistato il tuo primo agente immobiliare. Ora potrai utilizzarlo per assegnare la vendita delle case e guadagnare commissioni.",
      function() {
        actuallyCompraAgente(idAgente, prezzoAgente);
      }
    );
  } else {
    actuallyCompraAgente(idAgente, prezzoAgente);
  }
}

function actuallyCompraAgente(idAgente, prezzoAgente) {
  saldo -= prezzoAgente;
  displaySaldo.textContent = saldo.toFixed(2);
  const agente = agentiDati.find(a => a.id === idAgente);
  if (agente) {
    agentiAcquistati.push({ ...agente, tempoRimanente: 0 });
    alert(`Hai acquistato l'agente immobiliare ${agente.nome}. Ora puoi utilizzarlo per vendere case.`);
  }
}


/* Vendita di una Porta */
function vendiPorta(indice, prezzoVendita) {
  if (!guidaVendiMostrata) {
    guidaVendiMostrata = true;
    showInstructionModal(
      "Premi il pulsante <strong>VENDI</strong> per vendere la porta selezionata e realizzare un profitto.",
      function() {
        actuallyVendiPorta(indice, prezzoVendita);
      }
    );
  } else {
    actuallyVendiPorta(indice, prezzoVendita);
  }
}

function actuallyVendiPorta(indice, prezzoVendita) {
  if (indice < magazzino.length) {
    saldo += prezzoVendita;
    magazzino.splice(indice, 1);
    displaySaldo.textContent = saldo.toFixed(2);
    aggiornaLivello();
    alert(`Hai venduto la porta per €${prezzoVendita.toFixed(2)}.`);
    mostraMagazzino();
  }
}
// Funzione per verificare la bancarotta
function verificaBancarotta() {
  // Controlla se non hai abbastanza soldi per acquistare neanche la porta più economica
  const portaMinEconomica = portaDati[0]; // La prima porta nell'array (presumibilmente la più economica)
  
  if (saldo < portaMinEconomica.prezzo) {
    // Se non hai soldi per acquistare nemmeno la porta più economica, sei in bancarotta
    mostraPaginaBancarotta();
  }
}

// Funzione per mostrare la pagina di bancarotta
function mostraPaginaBancarotta() {
  // Nascondi la schermata del computer
  schermataComputer.classList.add('nascosto');
  
  // Crea un overlay per la schermata di bancarotta
  const bancarottaOverlay = document.createElement('div');
  bancarottaOverlay.id = 'bancarotta-overlay';
  bancarottaOverlay.innerHTML = `
    <div class="bancarotta-container">
      <h1>Bancarotta!</h1>
      <p>Purtroppo hai esaurito le tue risorse finanziarie.</p>
      <div class="spiegazione-bancarotta">
        <h2>Cos'è la Bancarotta?</h2>
        <p>La bancarotta è una situazione finanziaria in cui un individuo o un'azienda non è più in grado di pagare i propri debiti o sostenere le proprie spese.</p>
        
        <h3>Perché capita?</h3>
        <ul>
          <li>Spese eccessive rispetto alle entrate</li>
          <li>Investimenti non redditizi</li>
          <li>Mancanza di gestione finanziaria</li>
          <li>Improvvisi cali di reddito</li>
        </ul>
        
        <h3>Cosa fare ora?</h3>
        <p>Riparti dall'inizio! Impara dalla tua esperienza e migliora la tua strategia finanziaria.</p>
      </div>
      <button id="ricominciaGioco">Ricomincia da Capo</button>
    </div>
  `;
  
  // Aggiungi l'overlay al corpo del documento
  document.body.appendChild(bancarottaOverlay);
  
  // Aggiungi event listener per ricominciare il gioco
  document.getElementById('ricominciaGioco').addEventListener('click', resetGioco);
}

// Funzione per resettare il gioco
function resetGioco() {
  // Ripristina tutte le variabili iniziali
  saldo = 2200;
  livello = 1;
  livelloMassimo = 1;
  magazzino = [];
  agentiAcquistati = [];
  
  // Aggiorna la visualizzazione
  displaySaldo.textContent = saldo.toFixed(2);
  displayLivello.textContent = livello;
  
  // Rimuovi l'overlay di bancarotta
  const bancarottaOverlay = document.getElementById('bancarotta-overlay');
  if (bancarottaOverlay) {
    bancarottaOverlay.remove();
  }
}

// Aggiungi la chiamata a verificaBancarotta in punti chiave del gioco
// Ad esempio, dopo ogni acquisto o vendita
function aggiungiVerificaBancarotta() {
  // Modifica le funzioni esistenti per chiamare verificaBancarotta
  const originalCompraPorta = compraPorta;
  compraPorta = function(idPorta, prezzoPorta) {
    originalCompraPorta(idPorta, prezzoPorta);
    verificaBancarotta();
  };

  const originalCompraCasa = compraCasa;
  compraCasa = function(idCasa, prezzoCasa) {
    originalCompraCasa(idCasa, prezzoCasa);
    verificaBancarotta();
  };

  const originalCompraAgente = compraAgente;
  compraAgente = function(idAgente, prezzoAgente) {
    originalCompraAgente(idAgente, prezzoAgente);
    verificaBancarotta();
  };
}

// Chiama questa funzione all'avvio del gioco
aggiungiVerificaBancarotta();
