"""
Management panel for managing registered persons
"""
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QLabel, QLineEdit, QFileDialog, 
                             QMessageBox, QGroupBox, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from modules.database import FaceDatabase
from modules import config


class ManagementPanel(QDialog):
    """Dialog for managing registered persons"""
    
    # Signal emitted when a person is updated or deleted
    person_updated = pyqtSignal()
    
    def __init__(self, database: FaceDatabase, parent=None):
        """
        Initialize management panel
        
        Args:
            database: FaceDatabase instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.current_person_id = None
        self.current_photo_path = None
        
        self.setWindowTitle("Gestione Persone")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """Initialize user interface"""
        layout = QHBoxLayout()
        
        # Left side - Person list
        left_panel = self._create_list_panel()
        layout.addWidget(left_panel, 1)
        
        # Right side - Person details and edit
        right_panel = self._create_details_panel()
        layout.addWidget(right_panel, 1)
        
        self.setLayout(layout)
    
    def _create_list_panel(self) -> QGroupBox:
        """Create person list panel"""
        group = QGroupBox("Persone Registrate")
        layout = QVBoxLayout()
        
        # List widget
        self.person_list = QListWidget()
        self.person_list.itemClicked.connect(self.on_person_selected)
        layout.addWidget(self.person_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Aggiorna Lista")
        self.refresh_btn.clicked.connect(self.load_persons)
        button_layout.addWidget(self.refresh_btn)
        
        self.delete_btn = QPushButton("Elimina")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.clicked.connect(self.delete_person)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_details_panel(self) -> QGroupBox:
        """Create person details panel"""
        group = QGroupBox("Dettagli Persona")
        layout = QVBoxLayout()
        
        # Photo display
        self.photo_label = QLabel()
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 2px solid #4a9eff; background-color: #1a1a1a;")
        self.photo_label.setText("Nessuna foto")
        layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Photo button
        self.upload_photo_btn = QPushButton("Carica Foto")
        self.upload_photo_btn.clicked.connect(self.upload_photo)
        self.upload_photo_btn.setEnabled(False)
        layout.addWidget(self.upload_photo_btn)
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nome:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Inserisci nome")
        self.name_input.setEnabled(False)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Surname input
        surname_layout = QHBoxLayout()
        surname_layout.addWidget(QLabel("Cognome:"))
        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Inserisci cognome")
        self.surname_input.setEnabled(False)
        surname_layout.addWidget(self.surname_input)
        layout.addLayout(surname_layout)
        
        # Person ID label
        self.person_id_label = QLabel("ID: -")
        self.person_id_label.setObjectName("status")
        layout.addWidget(self.person_id_label)
        
        # Detection count label
        self.detection_count_label = QLabel("Rilevamenti: -")
        self.detection_count_label.setObjectName("status")
        layout.addWidget(self.detection_count_label)
        
        # Save button
        self.save_btn = QPushButton("Salva Modifiche")
        self.save_btn.setObjectName("success")
        self.save_btn.clicked.connect(self.save_person)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        # Add stretch
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def load_persons(self):
        """Load all persons from database"""
        self.person_list.clear()
        
        persons = self.database.get_all_persons(include_unknown=True)
        
        for person in persons:
            full_name = f"{person['name']} {person['surname']}".strip()
            if person['is_unknown']:
                full_name += " (Sconosciuto)"
            
            item = QListWidgetItem(full_name)
            item.setData(Qt.ItemDataRole.UserRole, person['id'])
            self.person_list.addItem(item)
    
    def on_person_selected(self, item: QListWidgetItem):
        """
        Handle person selection
        
        Args:
            item: Selected list item
        """
        person_id = item.data(Qt.ItemDataRole.UserRole)
        self.current_person_id = person_id
        
        # Enable edit controls
        self.name_input.setEnabled(True)
        self.surname_input.setEnabled(True)
        self.upload_photo_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)
        
        # Load person details
        person = self.database.get_person(person_id)
        if person:
            self.name_input.setText(person['name'])
            self.surname_input.setText(person['surname'])
            self.person_id_label.setText(f"ID: {person['id']}")
            
            # Load detection count
            detection_count = self.database.get_detection_count(person_id)
            self.detection_count_label.setText(f"Rilevamenti: {detection_count}")
            
            # Load photo
            if person['photo_path'] and os.path.exists(person['photo_path']):
                self.current_photo_path = person['photo_path']
                pixmap = QPixmap(person['photo_path'])
                scaled_pixmap = pixmap.scaled(200, 200, 
                                             Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
                self.photo_label.setPixmap(scaled_pixmap)
            else:
                self.photo_label.clear()
                self.photo_label.setText("Nessuna foto")
                self.current_photo_path = None
    
    def upload_photo(self):
        """Handle photo upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Foto",
            "",
            "Immagini (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            # Display photo
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(200, 200, 
                                         Qt.AspectRatioMode.KeepAspectRatio,
                                         Qt.TransformationMode.SmoothTransformation)
            self.photo_label.setPixmap(scaled_pixmap)
            
            # Copy photo to faces directory
            person_name = self.name_input.text().strip() or "unknown"
            filename = f"{person_name}_{self.current_person_id}.{config.FACE_IMAGE_FORMAT}"
            dest_path = os.path.join(config.FACES_DIR, filename)
            
            # Copy file
            import shutil
            shutil.copy2(file_path, dest_path)
            
            self.current_photo_path = dest_path
    
    def save_person(self):
        """Save person updates"""
        if not self.current_person_id:
            return
        
        name = self.name_input.text().strip()
        surname = self.surname_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Errore", "Il nome è obbligatorio!")
            return
        
        # Check for duplicates (excluding current person)
        existing = self.database.search_person_by_name(name, surname)
        if existing and existing['id'] != self.current_person_id:
            QMessageBox.warning(
                self, 
                "Errore", 
                "Una persona con questo nome e cognome esiste già!"
            )
            return
        
        # Update person
        success = self.database.update_person(
            self.current_person_id,
            name=name,
            surname=surname,
            photo_path=self.current_photo_path
        )
        
        if success:
            QMessageBox.information(self, "Successo", "Persona aggiornata con successo!")
            self.load_persons()
            self.person_updated.emit()
        else:
            QMessageBox.warning(self, "Errore", "Errore durante l'aggiornamento!")
    
    def delete_person(self):
        """Delete selected person"""
        if not self.current_person_id:
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            "Sei sicuro di voler eliminare questa persona?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.database.delete_person(self.current_person_id)
            
            if success:
                QMessageBox.information(self, "Successo", "Persona eliminata con successo!")
                
                # Clear form
                self.current_person_id = None
                self.name_input.clear()
                self.surname_input.clear()
                self.photo_label.clear()
                self.photo_label.setText("Nessuna foto")
                self.person_id_label.setText("ID: -")
                self.detection_count_label.setText("Rilevamenti: -")
                
                # Disable controls
                self.name_input.setEnabled(False)
                self.surname_input.setEnabled(False)
                self.upload_photo_btn.setEnabled(False)
                self.save_btn.setEnabled(False)
                self.delete_btn.setEnabled(False)
                
                self.load_persons()
                self.person_updated.emit()
            else:
                QMessageBox.warning(self, "Errore", "Errore durante l'eliminazione!")
