let livello = 1;
let saldo = 5000;
let magazzino = []; // Variabile per contenere le porte acquistate
let venditaIncremento = 20; // Percentuale di incremento del prezzo di vendita (default 20%)

const bottoneApriComputer = document.getElementById('apri-computer');
const schermataComputer = document.getElementById('schermata-computer');
const pulsanteChiudi = document.getElementById('pulsante-chiudi');
const displayLivello = document.getElementById('livello');
const displaySaldo = document.getElementById('saldo');
const bottoneMostraPorte = document.getElementById('mostra-porte');
const bottoneMostraMagazzino = document.getElementById('mostra-magazzino');
const contenitorePc = document.getElementById('schermo-pc');

const portaDati = [
  { id: 1, prezzo: 1000, immagine: '/immage/porta_inglese.png', nome: 'Porta 1' },
  { id: 2, prezzo: 3000, immagine: '/immage/porta_italiano.png', nome: 'Porta 2' },
  { id: 3, prezzo: 5000, immagine: '/immage/porta_moderna.png', nome: 'Porta 3' },
  { id: 4, prezzo: 7000, immagine: '/immage/porta_orientale.png', nome: 'Porta 4' },
  { id: 5, prezzo: 9000, immagine: '/immage/porta_gotica.png', nome: 'Porta 5' },
  { id: 6, prezzo: 12000, immagine: '/immage/porta_blindata.png', nome: 'Porta 6' }
];

// Aggiorna il livello in base al saldo
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

// Funzione per mostrare le porte disponibili
function mostraPorte() {
    contenitorePc.innerHTML = ''; // Pulisce il contenuto della schermata PC

    portaDati.forEach((porta) => {
        const elementoPorta = document.createElement('div');
        elementoPorta.classList.add('contenitore-porta');
        elementoPorta.innerHTML = `
            <img src="${porta.immagine}" alt="Porta ${porta.id}">
            <p>${porta.nome}</p>
            <p>Prezzo: €${porta.prezzo}</p>
            <button class="compra-btn" data-id="${porta.id}" data-prezzo="${porta.prezzo}">Compra</button>
        `;
        contenitorePc.appendChild(elementoPorta);
    });

    // Aggiungo gli event listener per ciascun pulsante "Compra"
    const compraBtns = document.querySelectorAll('.compra-btn');
    compraBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const idPorta = parseInt(btn.getAttribute('data-id'));
            const prezzoPorta = parseFloat(btn.getAttribute('data-prezzo'));
            compraPorta(idPorta, prezzoPorta);
        });
    });
}

// Funzione per acquistare una porta
function compraPorta(idPorta, prezzoPorta) {
    if (magazzino.length >= 10) {
        alert('Il magazzino è pieno! Capienza massima: 10 porte.');
        return;
    }
    if (saldo >= prezzoPorta) {
        saldo -= prezzoPorta;
        magazzino.push(portaDati.find((porta) => porta.id === idPorta));
        displaySaldo.textContent = saldo.toFixed(2);
        aggiornaLivello();
        alert(`Hai acquistato ${portaDati.find((porta) => porta.id === idPorta).nome}.`);
    } else {
        alert('Saldo insufficiente per acquistare questa porta.');
    }
}

// Funzione per mostrare il contenuto del magazzino
function mostraMagazzino() {
    contenitorePc.innerHTML = ''; // Pulisce il contenuto della schermata PC

    if (magazzino.length === 0) {
        contenitorePc.innerHTML = '<p>Il magazzino è vuoto.</p>';
    } else {
        magazzino.forEach((oggetto, indice) => {
            const prezzoVendita = oggetto.prezzo + (oggetto.prezzo * venditaIncremento / 100);
            const elementoOggetto = document.createElement('div');
            elementoOggetto.classList.add('contenitore-porta');
            elementoOggetto.innerHTML = `
                <img src="${oggetto.immagine}" alt="${oggetto.nome}">
                <p>${oggetto.nome}</p>
                <p>Prezzo originale: €${oggetto.prezzo}</p>
                <p>Prezzo di vendita: €${prezzoVendita.toFixed(2)}</p>
                <button class="vendi-btn" data-indice="${indice}" data-vendita="${prezzoVendita}">Vendi</button>
            `;
            contenitorePc.appendChild(elementoOggetto);
        });

        // Aggiungo gli event listener per ciascun pulsante "Vendi"
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

// Funzione per vendere una porta
function vendiPorta(indice, prezzoVendita) {
    if (indice < magazzino.length) {
        saldo += prezzoVendita;
        magazzino.splice(indice, 1); // Rimuove la porta venduta dal magazzino
        displaySaldo.textContent = saldo.toFixed(2);
        aggiornaLivello();
        alert(`Hai venduto la porta per €${prezzoVendita.toFixed(2)}.`);
        mostraMagazzino(); // Aggiorna la schermata del magazzino
    }
}

// Event listener per mostrare la schermata delle Porte
bottoneMostraPorte.addEventListener('click', mostraPorte);

// Event listener per mostrare la schermata del Magazzino
bottoneMostraMagazzino.addEventListener('click', mostraMagazzino);

// Event listener per aprire e chiudere la scheda Computer
bottoneApriComputer.addEventListener('click', () => {
    schermataComputer.classList.remove('nascosto');
});

pulsanteChiudi.addEventListener('click', () => {
    schermataComputer.classList.add('nascosto');
});
