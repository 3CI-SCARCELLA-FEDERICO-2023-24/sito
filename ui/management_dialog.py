"""User management dialog."""
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QListWidget, QListWidgetItem, 
                            QMessageBox, QWidget, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from database import Database
from ui.registration_dialog import RegistrationDialog
import config


class ManagementDialog(QDialog):
    """Dialog for managing registered users."""
    
    # Signal emitted when users are modified
    users_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize management dialog.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.db = Database()
        
        self.setWindowTitle("Gestione Utenti")
        self.setModal(True)
        self.setMinimumSize(700, 500)
        
        self._init_ui()
        self._load_users()
    
    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Gestione Utenti Registrati")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # User list
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        layout.addWidget(self.user_list)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Aggiungi Nuovo Utente")
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        add_btn.clicked.connect(self._add_user)
        
        delete_btn = QPushButton("Elimina Utente")
        delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        delete_btn.clicked.connect(self._delete_user)
        
        close_btn = QPushButton("Chiudi")
        close_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        close_btn.clicked.connect(self.accept)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def _load_users(self):
        """Load and display all users."""
        self.user_list.clear()
        users = self.db.get_all_users()
        
        if not users:
            item = QListWidgetItem("Nessun utente registrato")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.user_list.addItem(item)
            return
        
        for user in users:
            user_id, nome, cognome, foto_path, embedding_path, created_at = user
            
            # Create custom widget for user item
            item_widget = QWidget()
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(5, 5, 5, 5)
            
            # Photo thumbnail
            photo_label = QLabel()
            photo_label.setFixedSize(60, 60)
            photo_label.setStyleSheet("border: 1px solid #ccc;")
            
            if foto_path and os.path.exists(foto_path):
                pixmap = QPixmap(foto_path)
                pixmap = pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
                photo_label.setPixmap(pixmap)
            else:
                photo_label.setText("No\nPhoto")
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # User info
            info_label = QLabel(f"<b>{nome} {cognome}</b><br>ID: {user_id}<br>Data: {created_at[:10]}")
            
            item_layout.addWidget(photo_label)
            item_layout.addWidget(info_label)
            item_layout.addStretch()
            
            item_widget.setLayout(item_layout)
            
            # Add to list
            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setData(Qt.ItemDataRole.UserRole, user_id)
            self.user_list.addItem(item)
            self.user_list.setItemWidget(item, item_widget)
    
    def _add_user(self):
        """Add a new user manually."""
        dialog = RegistrationDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()
            if user_data:
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
                
                # Save photo if provided
                foto_path = None
                if photo is not None:
                    import cv2
                    import numpy as np
                    
                    # Generate unique filename
                    import time
                    filename = f"user_{int(time.time())}_{nome}_{cognome}.jpg"
                    foto_path = os.path.join(config.USERS_DIR, filename)
                    
                    if isinstance(photo, np.ndarray):
                        cv2.imwrite(foto_path, photo)
                    elif isinstance(photo, str) and os.path.exists(photo):
                        # Copy file
                        import shutil
                        shutil.copy(photo, foto_path)
                
                # Add to database
                user_id = self.db.add_user(nome, cognome, foto_path)
                
                if user_id:
                    QMessageBox.information(
                        self,
                        "Successo",
                        f"Utente '{nome} {cognome}' registrato con successo!"
                    )
                    self._load_users()
                    self.users_modified.emit()
                else:
                    QMessageBox.critical(
                        self,
                        "Errore",
                        "Errore durante la registrazione dell'utente."
                    )
    
    def _delete_user(self):
        """Delete selected user."""
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Errore", "Seleziona un utente da eliminare.")
            return
        
        user_id = current_item.data(Qt.ItemDataRole.UserRole)
        if not user_id:
            return
        
        # Get user info
        user = self.db.get_user(user_id)
        if not user:
            return
        
        nome, cognome = user[1], user[2]
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare l'utente '{nome} {cognome}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_user(user_id):
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Utente '{nome} {cognome}' eliminato con successo!"
                )
                self._load_users()
                self.users_modified.emit()
            else:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Errore durante l'eliminazione dell'utente."
                )
