"""
Finestra principale dell'applicazione di riconoscimento facciale.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QSplitter, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
import config

from ui.camera_preview import CameraPreview
from ui.management_panel import ManagementPanel
from face_recognition.face_detector import FaceDetector
from face_recognition.face_encoder import FaceEncoder
from face_recognition.face_matcher import FaceMatcher
from database.db_manager import DatabaseManager


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione."""
    
    def __init__(self):
        """Inizializza la finestra principale."""
        super().__init__()
        
        # Inizializza i componenti
        self.db_manager = DatabaseManager()
        self.face_detector = FaceDetector()
        self.face_encoder = FaceEncoder()
        self.face_matcher = FaceMatcher()
        
        self._init_ui()
        self._init_menu()
        
        # Connetti segnali
        self._connect_signals()
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente."""
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale
        main_layout = QVBoxLayout()
        
        # Titolo
        title_label = QLabel("Sistema di Riconoscimento Facciale")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            background-color: #2c3e50;
            color: white;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Splitter per dividere preview e gestione
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Camera preview (sinistra)
        self.camera_preview = CameraPreview(
            self.face_detector,
            self.face_encoder,
            self.face_matcher,
            self.db_manager
        )
        splitter.addWidget(self.camera_preview)
        
        # Management panel (destra)
        self.management_panel = ManagementPanel(
            self.db_manager,
            self.face_encoder
        )
        splitter.addWidget(self.management_panel)
        
        # Imposta le proporzioni iniziali (60% camera, 40% gestione)
        splitter.setSizes([int(config.WINDOW_WIDTH * 0.6), int(config.WINDOW_WIDTH * 0.4)])
        
        main_layout.addWidget(splitter)
        
        # Barra di stato
        self.statusBar().showMessage("Pronto")
        
        central_widget.setLayout(main_layout)
    
    def _init_menu(self):
        """Inizializza il menu."""
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Esci", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Visualizza
        view_menu = menubar.addMenu("Visualizza")
        
        refresh_action = QAction("Aggiorna Database", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_database)
        view_menu.addAction(refresh_action)
        
        # Menu Impostazioni
        settings_menu = menubar.addMenu("Impostazioni")
        
        threshold_action = QAction("Imposta Soglia Riconoscimento", self)
        threshold_action.triggered.connect(self.show_threshold_dialog)
        settings_menu.addAction(threshold_action)
        
        # Menu Aiuto
        help_menu = menubar.addMenu("Aiuto")
        
        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def _connect_signals(self):
        """Connette i segnali tra i componenti."""
        # Quando viene rilevato un volto sconosciuto
        self.camera_preview.unknown_face_detected.connect(
            self.management_panel.handle_unknown_face
        )
        
        # Quando il database viene aggiornato
        self.management_panel.database_updated.connect(
            self.camera_preview.refresh_database
        )
    
    def refresh_database(self):
        """Aggiorna il database."""
        self.camera_preview.refresh_database()
        self.management_panel.refresh_user_list()
        self.statusBar().showMessage("Database aggiornato", 3000)
    
    def show_threshold_dialog(self):
        """Mostra dialog per impostare la soglia di riconoscimento."""
        from PyQt6.QtWidgets import QInputDialog
        
        current_threshold = self.face_matcher.threshold
        
        value, ok = QInputDialog.getDouble(
            self,
            "Imposta Soglia",
            "Soglia di riconoscimento (0.0 - 1.0):",
            current_threshold,
            0.0,
            1.0,
            2
        )
        
        if ok:
            self.face_matcher.set_threshold(value)
            self.statusBar().showMessage(f"Soglia impostata a {value:.2f}", 3000)
    
    def show_about(self):
        """Mostra informazioni sull'applicazione."""
        QMessageBox.about(
            self,
            "Informazioni",
            """
            <h2>Sistema di Riconoscimento Facciale</h2>
            <p><b>Versione:</b> 1.0.0</p>
            <p><b>Tecnologie utilizzate:</b></p>
            <ul>
                <li>PyQt6 - Interfaccia grafica</li>
                <li>OpenCV - Elaborazione immagini</li>
                <li>MediaPipe - Rilevamento volti</li>
                <li>FaceNet - Generazione embeddings</li>
                <li>SQLite - Database</li>
            </ul>
            <p><b>Caratteristiche:</b></p>
            <ul>
                <li>Riconoscimento facciale in tempo reale</li>
                <li>Gestione utenti registrati</li>
                <li>Registrazione automatica volti sconosciuti</li>
                <li>Database locale con embeddings</li>
            </ul>
            """
        )
    
    def closeEvent(self, event):
        """Gestisce la chiusura dell'applicazione."""
        reply = QMessageBox.question(
            self,
            "Conferma Uscita",
            "Sei sicuro di voler uscire?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Ferma la camera
            self.camera_preview.stop_camera()
            
            # Chiudi i componenti
            self.face_detector.close()
            self.db_manager.close()
            
            event.accept()
        else:
            event.ignore()
