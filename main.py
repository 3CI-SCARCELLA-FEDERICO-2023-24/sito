"""Main application entry point for facial recognition system."""
import sys
import logging
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('face_recognition.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Initialize and run the application."""
    # Setup logging
    setup_logging()
    
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
