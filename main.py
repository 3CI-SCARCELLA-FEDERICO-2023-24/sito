"""Main application entry point for facial recognition system."""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Initialize and run the application."""
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Sistema di Riconoscimento Facciale")
    app.setOrganizationName("3CI-SCARCELLA-FEDERICO")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
