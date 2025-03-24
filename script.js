// Stato iniziale e variabili globali
let livello = 1;
let saldo = 5000;
let magazzino = [];         // Magazzino per le porte
let venditaIncremento = 20;  // Percentuale di incremento (applicata sia a porte che a case)
let agentiAcquistati = [];   // Lista di agenti acquistati

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

/* —— GESTIONE DEGLI AGENTI IMMOBILIARI —— */
// Visualizza la selezione degli agenti e quelli già acquistati
function mostraAgenti() {
  if (livello < 2) {
    alert("Devi raggiungere il livello 2 per accedere alla sezione agenti immobiliari.");
    return;
  }

  contenitorePc.innerHTML = ''; // Pulisce lo schermo PC

  // Sezione agenti acquistati
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

      // Aggiornamento dinamico della barra di progresso
      const barraProgresso = document.getElementById(`progresso-${agente.id}`);
      aggiornaBarraProgresso(barraProgresso, agente.tempoRimanente);
    });
  }

  // Sezione agenti disponibili
  const titoloDisponibili = document.createElement('h3');
  titoloDisponibili.textContent = 'Agenti Disponibili';
  contenitorePc.appendChild(titoloDisponibili);

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
    agentiAcquistati.push({ ...agente, tempoRimanente: 0 }); // Inizializza l'agente acquistato
    alert(`Hai acquistato l'agente immobiliare ${agente.nome}. Ora puoi utilizzarlo per vendere case.`);
  }
}

// Aggiorna dinamicamente la barra di progresso
function aggiornaBarraProgresso(barraProgresso, tempoRimanente) {
  if (tempoRimanente <= 0) {
    barraProgresso.style.width = '100%';
    barraProgresso.textContent = 'Vendita completata!';
  } else {
    const percentuale = (100 - (tempoRimanente / 180000) * 100).toFixed(2); // Calcola la percentuale basata sul tempo totale
    barraProgresso.style.width = `${percentuale}%`;
    barraProgresso.textContent = `${percentuale}%`;
  }
}
