"""Main application window."""
import os
import time
import numpy as np
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import cv2

from ui.camera_widget import CameraWidget
from ui.registration_dialog import RegistrationDialog
from ui.management_dialog import ManagementDialog
from face_recognition import FaceDetector, FaceEmbedder, FaceMatcher
from database import Database
import config


class MainWindow(QMainWindow):
    """Main application window for facial recognition."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        
        # Initialize components
        self.db = Database()
        self.detector = FaceDetector()
        self.embedder = FaceEmbedder()
        self.matcher = FaceMatcher()
        
        # State variables
        self.last_detection_time = 0
        self.detection_cooldown = 3.0  # seconds
        self.pending_registration = None
        
        # Load known users
        self.known_embeddings = []
        self.known_user_ids = []
        self._load_known_users()
        
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        self._init_ui()
        
        # Start face detection timer
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self._process_face_detection)
        self.detection_timer.start(100)  # Process every 100ms
    
    def _init_ui(self):
        """Initialize UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        # Left panel - Camera
        left_panel = self._create_camera_panel()
        
        # Center panel - Recognition info
        center_panel = self._create_info_panel()
        
        # Right panel - Controls
        right_panel = self._create_control_panel()
        
        main_layout.addWidget(left_panel, stretch=2)
        main_layout.addWidget(center_panel, stretch=1)
        main_layout.addWidget(right_panel, stretch=1)
        
        central_widget.setLayout(main_layout)
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
        """)
    
    def _create_camera_panel(self):
        """Create camera preview panel.
        
        Returns:
            QWidget containing camera preview
        """
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 10px;")
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Anteprima Camera")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Camera widget
        self.camera_widget = CameraWidget()
        self.camera_widget.start()
        layout.addWidget(self.camera_widget)
        
        panel.setLayout(layout)
        return panel
    
    def _create_info_panel(self):
        """Create recognition info panel.
        
        Returns:
            QWidget containing recognition information
        """
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Stato Riconoscimento")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Status label
        self.status_label = QLabel("In attesa...")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("padding: 20px; background-color: #e3f2fd; border-radius: 5px;")
        layout.addWidget(self.status_label)
        
        # Detected person info
        self.person_info_label = QLabel("")
        self.person_info_label.setFont(QFont("Arial", 11))
        self.person_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.person_info_label.setWordWrap(True)
        self.person_info_label.setStyleSheet("padding: 15px; margin-top: 10px;")
        layout.addWidget(self.person_info_label)
        
        # Statistics
        self.stats_label = QLabel("")
        self.stats_label.setFont(QFont("Arial", 10))
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def _create_control_panel(self):
        """Create control buttons panel.
        
        Returns:
            QWidget containing control buttons
        """
        panel = QWidget()
        panel.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Controlli")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Gestione button
        gestione_btn = QPushButton("👥 Gestione")
        gestione_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        gestione_btn.clicked.connect(self._open_management)
        layout.addWidget(gestione_btn)
        
        # Settings button (placeholder)
        settings_btn = QPushButton("⚙️ Impostazioni")
        settings_btn.setStyleSheet("background-color: #2196F3; color: white;")
        settings_btn.clicked.connect(self._show_settings)
        layout.addWidget(settings_btn)
        
        layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("❌ Esci")
        exit_btn.setStyleSheet("background-color: #f44336; color: white;")
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
        
        panel.setLayout(layout)
        return panel
    
    def _load_known_users(self):
        """Load all known users and their embeddings."""
        self.known_embeddings = []
        self.known_user_ids = []
        
        users = self.db.get_all_users()
        for user in users:
            user_id, nome, cognome, foto_path, embedding_path, _ = user
            
            if embedding_path and os.path.exists(embedding_path):
                try:
                    embedding = self.embedder.load_embedding(embedding_path)
                    self.known_embeddings.append(embedding)
                    self.known_user_ids.append(user_id)
                except Exception as e:
                    print(f"Error loading embedding for user {user_id}: {e}")
        
        self._update_stats()
    
    def _update_stats(self):
        """Update statistics display."""
        stats_text = f"Utenti registrati: {len(self.known_user_ids)}"
        self.stats_label.setText(stats_text)
    
    def _process_face_detection(self):
        """Process face detection on current frame."""
        frame = self.camera_widget.get_current_frame()
        if frame is None:
            return
        
        # Detect faces
        faces = self.detector.detect_faces(frame)
        
        if not faces:
            self.camera_widget.set_detected_faces([])
            self.status_label.setText("Nessun volto rilevato")
            self.person_info_label.setText("")
            return
        
        # Process first detected face
        face_bbox = faces[0]
        face_img = self.detector.extract_face(frame, face_bbox)
        
        if face_img is None:
            return
        
        # Generate embedding
        try:
            embedding = self.embedder.generate_embedding(face_img)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return
        
        # Match against known faces
        if self.known_embeddings:
            user_id, similarity = self.matcher.find_match(
                embedding, self.known_embeddings, self.known_user_ids
            )
            
            if user_id:
                # Recognized user
                user = self.db.get_user(user_id)
                if user:
                    nome, cognome = user[1], user[2]
                    label = f"{nome} {cognome}"
                    self.status_label.setText("✅ Utente Riconosciuto")
                    self.status_label.setStyleSheet(
                        "padding: 20px; background-color: #c8e6c9; border-radius: 5px; color: #2e7d32;"
                    )
                    self.person_info_label.setText(
                        f"<b>Nome:</b> {nome} {cognome}<br>"
                        f"<b>Similarità:</b> {similarity:.2%}"
                    )
                    self.camera_widget.set_detected_faces([face_bbox], [label])
            else:
                # Unknown face
                self._handle_unknown_face(face_img, face_bbox, embedding)
        else:
            # No known users - prompt registration
            self._handle_unknown_face(face_img, face_bbox, embedding)
    
    def _handle_unknown_face(self, face_img, face_bbox, embedding):
        """Handle detection of unknown face.
        
        Args:
            face_img: Face image
            face_bbox: Face bounding box
            embedding: Face embedding
        """
        current_time = time.time()
        
        # Check cooldown to avoid spamming registration dialogs
        if current_time - self.last_detection_time < self.detection_cooldown:
            self.status_label.setText("⚠️ Volto Sconosciuto")
            self.status_label.setStyleSheet(
                "padding: 20px; background-color: #fff9c4; border-radius: 5px; color: #f57f17;"
            )
            self.person_info_label.setText("Volto non riconosciuto nel database")
            self.camera_widget.set_detected_faces([face_bbox], ["Sconosciuto"])
            return
        
        self.last_detection_time = current_time
        
        # Prompt for registration
        self._prompt_registration(face_img, embedding)
    
    def _prompt_registration(self, face_img, embedding):
        """Prompt user to register new face.
        
        Args:
            face_img: Face image
            embedding: Face embedding
        """
        dialog = RegistrationDialog(face_frame=face_img, parent=self)
        if dialog.exec() == RegistrationDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()
            if user_data:
                self._register_new_user(user_data, face_img, embedding)
    
    def _register_new_user(self, user_data, face_img, embedding):
        """Register a new user.
        
        Args:
            user_data: User registration data
            face_img: Face image
            embedding: Face embedding
        """
        nome = user_data['nome']
        cognome = user_data['cognome']
        photo = user_data.get('photo')
        
        # Check for duplicates
        if self.db.user_exists(nome, cognome):
            QMessageBox.warning(
                self,
                "Utente Duplicato",
                f"Un utente con nome '{nome} {cognome}' esiste già!"
            )
            return
        
        # Save photo
        foto_path = None
        if photo is not None:
            filename = f"user_{int(time.time())}_{nome}_{cognome}.jpg"
            foto_path = os.path.join(config.USERS_DIR, filename)
            
            if isinstance(photo, np.ndarray):
                cv2.imwrite(foto_path, photo)
            elif isinstance(photo, str) and os.path.exists(photo):
                import shutil
                shutil.copy(photo, foto_path)
        
        # Save embedding
        embedding_filename = f"embedding_{int(time.time())}_{nome}_{cognome}.npy"
        embedding_path = os.path.join(config.EMBEDDINGS_DIR, embedding_filename)
        self.embedder.save_embedding(embedding, embedding_path)
        
        # Add to database
        user_id = self.db.add_user(nome, cognome, foto_path, embedding_path)
        
        if user_id:
            QMessageBox.information(
                self,
                "Successo",
                f"Utente '{nome} {cognome}' registrato con successo!"
            )
            # Reload known users
            self._load_known_users()
        else:
            QMessageBox.critical(
                self,
                "Errore",
                "Errore durante la registrazione dell'utente."
            )
    
    def _open_management(self):
        """Open user management dialog."""
        dialog = ManagementDialog(parent=self)
        dialog.users_modified.connect(self._load_known_users)
        dialog.exec()
    
    def _show_settings(self):
        """Show settings dialog (placeholder)."""
        QMessageBox.information(
            self,
            "Impostazioni",
            "Le impostazioni non sono ancora implementate."
        )
    
    def closeEvent(self, event):
        """Handle window close event.
        
        Args:
            event: Close event
        """
        self.detection_timer.stop()
        self.camera_widget.stop()
        event.accept()
