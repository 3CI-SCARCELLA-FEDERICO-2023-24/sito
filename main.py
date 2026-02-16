"""
Entry point dell'applicazione di riconoscimento facciale.
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Funzione principale."""
    # Crea l'applicazione
    app = QApplication(sys.argv)
    
    # Imposta lo stile
    app.setStyle('Fusion')
    
    # Crea e mostra la finestra principale
    window = MainWindow()
    window.show()
    
    # Esegui l'applicazione
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
