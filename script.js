// Variabili globali
let livello = 1, saldo = 50000, livelloMassimo = 1;
let magazzino = [], agentiAcquistati = [], registroVendite = [];
const venditaIncremento = 20;

// Elementi del DOM
const bottoneApriComputer = document.getElementById('apri-computer');
const schermataComputer = document.getElementById('schermata-computer');
const pulsanteChiudi = document.getElementById('pulsante-chiudi');
const displayLivello = document.getElementById('livello');
const displaySaldo = document.getElementById('saldo');
const contenitorePc = document.getElementById('schermo-pc');

// Dati degli oggetti
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
  { id: 1, nome: 'Agente Alpha', prezzo: 2000, percentuale: 10 },
  { id: 2, nome: 'Agente Beta', prezzo: 3000, percentuale: 15 },
  { id: 3, nome: 'Agente Gamma', prezzo: 2500, percentuale: 12 }
];

// Funzioni di utilità
function aggiornaLivello() {
  livello = saldo >= 100000 ? 3 : saldo >= 10000 ? 2 : 1;
  if (livello > livelloMassimo) livelloMassimo = livello;
  livello = livelloMassimo;
  displayLivello.textContent = livello;
}

function aggiornaSaldo() {
  displaySaldo.textContent = saldo.toFixed(2);
}

// Funzione generica per mostrare oggetti
function mostraOggetti(dati, tipo, callback) {
  contenitorePc.innerHTML = '';
  dati.forEach(oggetto => {
    const elemento = document.createElement('div');
    elemento.classList.add('contenitore-porta');
    elemento.innerHTML = `
      <img src="${oggetto.immagine}" alt="${oggetto.nome}">
      <p>${oggetto.nome}</p>
      <p>Prezzo: €${oggetto.prezzo}</p>
      <button class="compra-btn" data-id="${oggetto.id}" data-prezzo="${oggetto.prezzo}">Compra</button>
    `;
    contenitorePc.appendChild(elemento);
  });
  document.querySelectorAll('.compra-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = parseInt(btn.getAttribute('data-id'));
      const prezzo = parseFloat(btn.getAttribute('data-prezzo'));
      callback(id, prezzo);
    });
  });
}

// Funzioni per acquistare porte e case
function compraPorta(id, prezzo) {
  if (magazzino.length >= 10 || saldo < prezzo) return alert('Acquisto non possibile.');
  saldo -= prezzo;
  magazzino.push(portaDati.find(p => p.id === id));
  registroVendite.push(`Acquistata porta: €${prezzo}.`);
  aggiornaSaldo();
  aggiornaLivello();
}

function compraCasa(id, prezzo) {
  if (livello < 2 || saldo < prezzo || agentiAcquistati.length === 0) return alert('Acquisto non possibile.');
  saldo -= prezzo;
  registroVendite.push(`Acquistata casa: €${prezzo}.`);
  aggiornaSaldo();
  aggiornaLivello();
  iniziaVenditaCasa(agentiAcquistati[0], caseDati.find(c => c.id === id));
}

// Funzione per vendere una casa
function iniziaVenditaCasa(agente, casa) {
  const tempo = Math.random() * (180000 - 60000) + 60000;
  const prezzoVendita = casa.prezzo * (1 + venditaIncremento / 100);
  const guadagnoNetto = prezzoVendita * (1 - agente.percentuale / 100);
  
  registroVendite.push(`Vendita iniziata: ${casa.nome}. Prezzo: €${prezzoVendita.toFixed(2)}`);
  setTimeout(() => {
    saldo += guadagnoNetto;
    registroVendite.push(`Vendita completata: ${casa.nome}. Guadagno: €${guadagnoNetto.toFixed(2)}`);
    aggiornaSaldo();
    aggiornaLivello();
  }, tempo);
}

// Eventi interfaccia
bottoneApriComputer.addEventListener('click', () => schermataComputer.classList.remove('nascosto'));
pulsanteChiudi.addEventListener('click', () => schermataComputer.classList.add('nascosto'));
document.getElementById('mostra-porte').addEventListener('click', () => mostraOggetti(portaDati, 'porte', compraPorta));
document.getElementById('mostra-case').addEventListener('click', () => livello >= 2 ? mostraOggetti(caseDati, 'case', compraCasa) : alert('Raggiungi livello 2.'));
document.getElementById('registro-vendite').addEventListener('click', () => {
  contenitorePc.innerHTML = registroVendite.map(v => `<p>${v}</p>`).join('');
});

// Inizializzazione
aggiornaSaldo();
