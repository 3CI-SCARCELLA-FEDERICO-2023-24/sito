// Stato iniziale e variabili globali
let livello = 1;
let saldo = 5000;
let magazzino = [];         // Magazzino per le porte
let venditaIncremento = 20;  // Percentuale di incremento (applicata sia a porte che a case)

let agenteAttivo = null;     // Agente immobiliare acquistato (necessario per comprare una casa)
let casaInVendita = false;   // Flag per indicare se è in corso la vendita di una casa

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
  { id: 1, prezzo: 1000, immagine: '/immage/porta_inglese.png', nome: 'Porta 1' },
  { id: 2, prezzo: 3000, immagine: '/immage/porta_italiano.png', nome: 'Porta 2' },
  { id: 3, prezzo: 5000, immagine: '/immage/porta_moderna.png', nome: 'Porta 3' },
  { id: 4, prezzo: 7000, immagine: '/immage/porta_orientale.png', nome: 'Porta 4' },
  { id: 5, prezzo: 9000, immagine: '/immage/porta_gotica.png', nome: 'Porta 5' },
  { id: 6, prezzo: 12000, immagine: '/immage/porta_blindata.png', nome: 'Porta 6' }
];

// Dati delle case (prezzi più alti)
const caseDati = [
  { id: 1, prezzo: 20000, immagine: '/immage/casa_classica.png', nome: 'Casa 1' },
  { id: 2, prezzo: 30000, immagine: '/immage/casa_moderna.png', nome: 'Casa 2' },
  { id: 3, prezzo: 40000, immagine: '/immage/casa_lussuosa.png', nome: 'Casa 3' }
];

// Dati degli agenti immobiliari
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
  displayLivello.textContent = livello;
}

// Imposta il saldo iniziale
displaySaldo.textContent = saldo.toFixed(2);

/* —— GESTIONE DELLE PORTE —— */
// Visualizza le porte disponibili
function mostraPorte() {
  contenitorePc.innerHTML = ''; // Pulisce lo schermo PC
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
  
  // Aggiungo gli event listener per i pulsanti "Compra"
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
    alert(`Hai acquistato ${portaAcquistata.nome}.`);
    aggiornaLivello();
  }
}

// Mostra il contenuto del magazzino (porte)
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

/* —— GESTIONE DELLE CASE —— */
// Visualizza le case disponibili: se il livello è inferiore a 2, blocca l'accesso
function mostraCase() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione case.");
    return;
  }
  
  contenitorePc.innerHTML = ''; // Pulisce lo schermo PC
  caseDati.forEach((casa) => {
    const elementoCasa = document.createElement('div');
    // Riutilizziamo lo stesso container delle porte per coerenza grafica
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

// Acquista una casa: è possibile solo se esiste un agente e se non è già in corso una vendita
function compraCasa(idCasa, prezzoCasa) {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per acquistare una casa.");
    return;
  }
  if (!agenteAttivo) {
    alert('Devi acquistare un agente immobiliare prima di comprare una casa.');
    return;
  }
  if (casaInVendita) {
    alert("Un agente immobiliare è già impegnato nella vendita di una casa. Attendi il completamento della vendita.");
    return;
  }
  if (saldo < prezzoCasa) {
    alert('Saldo insufficiente per acquistare questa casa.');
    return;
  }
  saldo -= prezzoCasa;
  displaySaldo.textContent = saldo.toFixed(2);
  const casaAcquistata = caseDati.find(casa => casa.id === idCasa);
  if (casaAcquistata) {
    casaInVendita = casaAcquistata; // L'agente inizia a vendere questa casa
    alert(`Hai acquistato ${casaAcquistata.nome}. La vendita avverrà automaticamente tra 1 e 3 minuti.`);
    aggiornaLivello();
    // Imposta timer per vendita automatica (delay random tra 60000 e 180000 ms)
    const delay = Math.floor(Math.random() * (180000 - 60000 + 1)) + 60000;
    casaAcquistata.timeoutId = setTimeout(() => {
      autoVendiCasa(casaAcquistata);
    }, delay);
  }
}

// Vendita automatica della casa
function autoVendiCasa(casa) {
  const prezzoVenditaCasa = casa.prezzo + (casa.prezzo * venditaIncremento / 100);
  const commissione = prezzoVenditaCasa * (agenteAttivo.percentuale / 100);
  const guadagnoNetto = prezzoVenditaCasa - commissione;
  saldo += guadagnoNetto;
  displaySaldo.textContent = saldo.toFixed(2);
  alert(`La casa ${casa.nome} è stata venduta per €${prezzoVenditaCasa.toFixed(2)}.
Commissione dell'agente: €${commissione.toFixed(2)}.
Guadagno ottenuto: €${guadagnoNetto.toFixed(2)}.`);
  aggiornaLivello();
  casaInVendita = false;
}

/* —— GESTIONE DEGLI AGENTI IMMOBILIARI —— */
// Visualizza la selezione degli agenti: accesso consentito solo dal livello 2
function mostraAgenti() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione agenti immobiliari.");
    return;
  }
  
  contenitorePc.innerHTML = ''; // Pulisce lo schermo PC
  if (agenteAttivo) {
    contenitorePc.innerHTML = `<p>Hai già acquistato un agente immobiliare: ${agenteAttivo.nome}</p>`;
    return;
  }
  agentiDati.forEach(agent => {
    const elementoAgente = document.createElement('div');
    elementoAgente.classList.add('contenitore-porta');
    elementoAgente.innerHTML = `
      <p>${agent.nome}</p>
      <p>Prezzo: €${agent.prezzo}</p>
      <p>Professionalità: ${agent.professionalita}</p>
      <p>Trattativa: ${agent.trattativa}</p>
      <p>Commissione: ${agent.percentuale}%</p>
      <button class="compra-agente-btn" data-id="${agent.id}" data-prezzo="${agent.prezzo}">Compra Agente</button>
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
    agenteAttivo = agente;
    alert(`Hai acquistato l'agente immobiliare ${agente.nome}. Ora puoi acquistare case.`);
  }
}

/* —— EVENT LISTENERS —— */
bottoneMostraPorte.addEventListener('click', mostraPorte);
bottoneMostraMagazzino.addEventListener('click', mostraMagazzino);
bottoneMostraCase.addEventListener('click', mostraCase);
bottoneMostraAgenti.addEventListener('click', mostraAgenti);

bottoneApriComputer.addEventListener('click', () => {
  schermataComputer.classList.remove('nascosto');
});
pulsanteChiudi.addEventListener('click', () => {
  schermataComputer.classList.add('nascosto');
});
