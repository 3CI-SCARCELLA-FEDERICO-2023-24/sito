let level = 1;
let balance = 5000;
let magazzino = []; // Variabile per contenere le porte acquistate
let venditaIncremento = 20; // Percentuale di incremento del prezzo di vendita (default 20%)

const openComputerButton = document.getElementById('open-computer');
const computerScreen = document.getElementById('computer-screen');
const closeButton = document.getElementById('close-button');
const levelDisplay = document.getElementById('level');
const balanceDisplay = document.getElementById('balance');
const showDoorsButton = document.getElementById('show-doors');
const showWarehouseButton = document.getElementById('show-warehouse');
const pcContainer = document.getElementById('pc');

const doorData = [
    { id: 1, price: 1000, image: '/immage/porta_inglese.png', name: 'Porta 1' },
    { id: 2, price: 3000, image: '/immage/porta_italiano.png', name: 'Porta 2' },
    { id: 3, price: 5000, image: '/immage/porta_moderna.png', name: 'Porta 3' },
    { id: 4, price: 7000, image: '/immage/porta_orientale.png', name: 'Porta 4' },
    { id: 5, price: 9000, image: '/immage/porta_gotica.png', name: 'Porta 5' },
    { id: 6, price: 12000, image: '/immage/porta_blindata.png', name: 'Porta 6' }
];

// Funzione per aggiornare il livello in base al saldo
function updateLevel() {
    if (balance >= 100000) {
        level = 3;
    } else if (balance >= 10000) {
        level = 2;
    } else {
        level = 1;
    }
    levelDisplay.textContent = level;
}

// Mostra il saldo corrente
balanceDisplay.textContent = balance.toFixed(2);

// Funzione per mostrare le porte
function showDoors() {
    pcContainer.innerHTML = ''; // Pulisce il contenuto della schermata PC
    doorData.forEach((door) => {
        const doorElement = document.createElement('div');
        doorElement.classList.add('door-container');
        doorElement.innerHTML = `
            <img src="${door.image}" alt="Porta ${door.id}">
            <p>${door.name}</p>
            <p>Prezzo: €${door.price}</p>
            <button onclick="buyDoor(${door.id}, ${door.price})">Compra</button>
        `;
        pcContainer.appendChild(doorElement);
    });
}

// Funzione per acquistare una porta
function buyDoor(doorId, doorPrice) {
    if (magazzino.length >= 10) {
        alert('Il magazzino è pieno! Capienza massima: 10 porte.');
        return;
    }
    if (balance >= doorPrice) {
        balance -= doorPrice;
        magazzino.push(doorData.find((door) => door.id === doorId));
        balanceDisplay.textContent = balance.toFixed(2);
        updateLevel();
        alert(`Hai acquistato ${doorData.find((door) => door.id === doorId).name}.`);
    } else {
        alert('Saldo insufficiente per acquistare questa porta.');
    }
}

// Funzione per mostrare il contenuto del magazzino
function showWarehouse() {
    pcContainer.innerHTML = ''; // Pulisce il contenuto della schermata PC
    if (magazzino.length === 0) {
        pcContainer.innerHTML = '<p>Il magazzino è vuoto.</p>';
    } else {
        magazzino.forEach((item, index) => {
            const venditaPrezzo = item.price + (item.price * venditaIncremento / 100);
            const itemElement = document.createElement('div');
            itemElement.classList.add('door-container');
            itemElement.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <p>${item.name}</p>
                <p>Prezzo originale: €${item.price}</p>
                <p>Prezzo di vendita: €${venditaPrezzo.toFixed(2)}</p>
                <button onclick="sellDoor(${index}, ${venditaPrezzo})">Vendi</button>
            `;
            pcContainer.appendChild(itemElement);
        });
    }
}

// Funzione per vendere una porta
function sellDoor(index, venditaPrezzo) {
    if (index < magazzino.length) {
        balance += venditaPrezzo;
        magazzino.splice(index, 1); // Rimuove la porta venduta dal magazzino
        balanceDisplay.textContent = balance.toFixed(2);
        updateLevel();
        alert(`Hai venduto la porta per €${venditaPrezzo.toFixed(2)}.`);
        showWarehouse(); // Aggiorna la schermata del magazzino
    }
}

// Event listener per mostrare la schermata Porte
showDoorsButton.addEventListener('click', showDoors);

// Event listener per mostrare la schermata Magazzino
showWarehouseButton.addEventListener('click', showWarehouse);

// Event listener per aprire e chiudere la scheda Computer
openComputerButton.addEventListener('click', () => {
    computerScreen.classList.remove('hidden');
});

closeButton.addEventListener('click', () => {
    computerScreen.classList.add('hidden');
});
