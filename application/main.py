#!/usr/bin/env python3
"""
Main entry point for facial recognition application

Facial Recognition Application
============================

This application provides real-time face detection and recognition using:
- MediaPipe for face detection
- DeepFace for face recognition
- PyQt6 for the user interface
- SQLite for database storage

Features:
- Real-time video capture and face detection
- Automatic registration of unknown faces
- Manual person management (edit names, photos)
- Face recognition with configurable threshold
- Cross-platform support (Windows, Linux, macOS)

Usage:
    python main.py

Requirements:
    See requirements.txt for dependencies
"""

import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from modules.camera import Camera


def check_camera():
    """Check if camera is available"""
    if not Camera.is_camera_available():
        return False
    return True


def main():
    """Main function"""
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Facial Recognition System")
    app.setOrganizationName("FaceRecognition")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Check camera availability
    if not check_camera():
        QMessageBox.critical(
            None,
            "Errore",
            "Nessuna webcam disponibile!\n\n"
            "Assicurati che una webcam sia collegata e funzionante."
        )
        return 1
    
    # Create and show main window
    try:
        window = MainWindow()
        window.show()
        
        # Run application
        return app.exec()
    
    except Exception as e:
        QMessageBox.critical(
            None,
            "Errore Critico",
            f"Si è verificato un errore durante l'avvio:\n\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
