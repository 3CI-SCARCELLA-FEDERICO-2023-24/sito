"""User registration dialog."""
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import cv2
import numpy as np
from PIL import Image
import config


class RegistrationDialog(QDialog):
    """Dialog for registering new users."""
    
    def __init__(self, face_frame=None, parent=None):
        """Initialize registration dialog.
        
        Args:
            face_frame: Optional face image captured from camera
            parent: Parent widget
        """
        super().__init__(parent)
        self.face_frame = face_frame
        self.selected_photo_path = None
        self.user_data = None
        
        self.setWindowTitle("Registrazione Nuovo Utente")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self._init_ui()
    
    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Registra Nuovo Utente")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Nome field
        nome_layout = QHBoxLayout()
        nome_label = QLabel("Nome:")
        nome_label.setMinimumWidth(100)
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Inserisci il nome")
        nome_layout.addWidget(nome_label)
        nome_layout.addWidget(self.nome_input)
        layout.addLayout(nome_layout)
        
        # Cognome field
        cognome_layout = QHBoxLayout()
        cognome_label = QLabel("Cognome:")
        cognome_label.setMinimumWidth(100)
        self.cognome_input = QLineEdit()
        self.cognome_input.setPlaceholderText("Inserisci il cognome")
        cognome_layout.addWidget(cognome_label)
        cognome_layout.addWidget(self.cognome_input)
        layout.addLayout(cognome_layout)
        
        # Photo preview
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setStyleSheet("border: 2px solid #ccc; background-color: #f0f0f0;")
        
        if self.face_frame is not None:
            self._display_photo(self.face_frame)
            self.photo_label.setToolTip("Foto catturata dalla webcam")
        else:
            self.photo_label.setText("Nessuna foto")
        
        layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Upload photo button
        upload_btn = QPushButton("Carica Foto Profilo (Opzionale)")
        upload_btn.clicked.connect(self._upload_photo)
        layout.addWidget(upload_btn)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Salva")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        save_btn.clicked.connect(self._save)
        
        skip_btn = QPushButton("Salta (Sconosciuto)")
        skip_btn.setStyleSheet("background-color: #ff9800; color: white; padding: 8px;")
        skip_btn.clicked.connect(self._skip)
        
        cancel_btn = QPushButton("Annulla")
        cancel_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(skip_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def _display_photo(self, img):
        """Display photo in preview label.
        
        Args:
            img: Image to display (numpy array or path)
        """
        if isinstance(img, np.ndarray):
            # Convert BGR to RGB
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Resize to fit label
            h, w = rgb_img.shape[:2]
            aspect = w / h
            new_h = 200
            new_w = int(new_h * aspect)
            if new_w > 200:
                new_w = 200
                new_h = int(new_w / aspect)
            
            rgb_img = cv2.resize(rgb_img, (new_w, new_h))
            
            # Convert to QPixmap
            from PyQt6.QtGui import QImage
            h, w, ch = rgb_img.shape
            bytes_per_line = ch * w
            qt_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
        else:
            # Load from file path
            pixmap = QPixmap(img)
            pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        
        self.photo_label.setPixmap(pixmap)
    
    def _upload_photo(self):
        """Handle photo upload."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Foto Profilo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.selected_photo_path = file_path
            self._display_photo(file_path)
    
    def _save(self):
        """Save user data."""
        nome = self.nome_input.text().strip()
        cognome = self.cognome_input.text().strip()
        
        if not nome or not cognome:
            QMessageBox.warning(self, "Errore", "Nome e Cognome sono obbligatori!")
            return
        
        # Prepare photo
        photo_data = None
        if self.selected_photo_path:
            photo_data = self.selected_photo_path
        elif self.face_frame is not None:
            photo_data = self.face_frame
        
        self.user_data = {
            'nome': nome,
            'cognome': cognome,
            'photo': photo_data
        }
        
        self.accept()
    
    def _skip(self):
        """Skip registration and use default."""
        self.user_data = {
            'nome': config.DEFAULT_USER_NAME,
            'cognome': config.DEFAULT_USER_SURNAME,
            'photo': self.face_frame
        }
        self.accept()
    
    def get_user_data(self):
        """Get registered user data.
        
        Returns:
            Dictionary with user data or None
        """
        return self.user_data
