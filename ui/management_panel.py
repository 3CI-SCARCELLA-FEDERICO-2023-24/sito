"""
Panel di gestione utenti.
"""

import cv2
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QListWidgetItem, QLabel, QLineEdit,
                            QMessageBox, QFileDialog, QDialog, QDialogButtonBox,
                            QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import config


class UserRegistrationDialog(QDialog):
    """Dialog per la registrazione di un nuovo utente."""
    
    def __init__(self, face_image=None, parent=None):
        """
        Inizializza il dialog di registrazione.
        
        Args:
            face_image: Immagine del volto (opzionale)
            parent: Widget genitore
        """
        super().__init__(parent)
        
        self.face_image = face_image
        self.profile_photo = None
        
        self.setWindowTitle("Registra Nuovo Utente")
        self.setModal(True)
        self.resize(400, 500)
        
        self._init_ui()
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente."""
        layout = QVBoxLayout()
        
        # Form per nome e cognome
        form_layout = QFormLayout()
        
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Inserisci il nome")
        form_layout.addRow("Nome:", self.nome_input)
        
        self.cognome_input = QLineEdit()
        self.cognome_input.setPlaceholderText("Inserisci il cognome")
        form_layout.addRow("Cognome:", self.cognome_input)
        
        layout.addLayout(form_layout)
        
        # Anteprima foto
        photo_group = QGroupBox("Foto Profilo")
        photo_layout = QVBoxLayout()
        
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(200, 200)
        self.photo_label.setStyleSheet("border: 2px solid #333; background-color: #f0f0f0;")
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        if self.face_image is not None:
            self._display_image(self.face_image)
            self.photo_label.setToolTip("Foto dal rilevamento facciale")
        else:
            self.photo_label.setText("Nessuna foto")
        
        photo_layout.addWidget(self.photo_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Pulsante per caricare foto
        self.load_photo_button = QPushButton("Carica Foto...")
        self.load_photo_button.clicked.connect(self.load_photo)
        photo_layout.addWidget(self.load_photo_button)
        
        photo_group.setLayout(photo_layout)
        layout.addWidget(photo_group)
        
        # Pulsanti OK/Cancel
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def _display_image(self, image):
        """
        Visualizza un'immagine nel label.
        
        Args:
            image: Immagine numpy array (BGR)
        """
        if image is None or image.size == 0:
            return
        
        # Converti BGR a RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Crea QImage
        h, w, ch = image_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(image_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scala e mostra
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.photo_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.photo_label.setPixmap(scaled_pixmap)
    
    def load_photo(self):
        """Carica una foto profilo da file."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona Foto Profilo",
            "",
            "Immagini (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if filename:
            # Carica l'immagine
            image = cv2.imread(filename)
            if image is not None:
                self.face_image = image
                self.profile_photo = filename
                self._display_image(image)
    
    def get_user_data(self):
        """
        Ottiene i dati inseriti dall'utente.
        
        Returns:
            Dizionario con nome, cognome e foto
        """
        return {
            'nome': self.nome_input.text().strip(),
            'cognome': self.cognome_input.text().strip(),
            'foto': self.face_image
        }


class ManagementPanel(QWidget):
    """Panel per la gestione degli utenti registrati."""
    
    # Segnale emesso quando il database viene aggiornato
    database_updated = pyqtSignal()
    
    def __init__(self, db_manager, face_encoder, parent=None):
        """
        Inizializza il panel di gestione.
        
        Args:
            db_manager: Istanza di DatabaseManager
            face_encoder: Istanza di FaceEncoder
            parent: Widget genitore
        """
        super().__init__(parent)
        
        self.db_manager = db_manager
        self.face_encoder = face_encoder
        
        self._init_ui()
        self.refresh_user_list()
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente."""
        layout = QVBoxLayout()
        
        # Titolo
        title_label = QLabel("Gestione Utenti")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Lista utenti
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        layout.addWidget(self.user_list)
        
        # Info utente selezionato
        self.info_label = QLabel("Seleziona un utente per vedere i dettagli")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("padding: 10px; border: 1px solid #ccc; background-color: #f9f9f9;")
        layout.addWidget(self.info_label)
        
        # Pulsanti di azione
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Aggiungi Utente")
        self.add_button.clicked.connect(self.add_user)
        button_layout.addWidget(self.add_button)
        
        self.delete_button = QPushButton("Elimina Utente")
        self.delete_button.clicked.connect(self.delete_user)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("Aggiorna Lista")
        self.refresh_button.clicked.connect(self.refresh_user_list)
        button_layout.addWidget(self.refresh_button)
        
        layout.addLayout(button_layout)
        
        # Statistiche
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)
        
        self.setLayout(layout)
    
    def refresh_user_list(self):
        """Aggiorna la lista degli utenti dal database."""
        self.user_list.clear()
        
        users = self.db_manager.get_all_users()
        
        for user in users:
            item_text = f"{user['cognome']}, {user['nome']} (ID: {user['id']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, user['id'])
            self.user_list.addItem(item)
        
        # Aggiorna statistiche
        self.stats_label.setText(f"Totale utenti registrati: {len(users)}")
        
        # Emetti segnale
        self.database_updated.emit()
    
    def on_user_selected(self):
        """Gestisce la selezione di un utente."""
        selected_items = self.user_list.selectedItems()
        
        if not selected_items:
            self.delete_button.setEnabled(False)
            self.info_label.setText("Seleziona un utente per vedere i dettagli")
            return
        
        self.delete_button.setEnabled(True)
        
        # Ottieni dati utente
        user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        user = self.db_manager.get_user(user_id)
        
        if user:
            info_text = f"<b>Nome:</b> {user['nome']}<br>"
            info_text += f"<b>Cognome:</b> {user['cognome']}<br>"
            info_text += f"<b>ID:</b> {user['id']}<br>"
            info_text += f"<b>Data Registrazione:</b> {user['data_registrazione']}"
            
            self.info_label.setText(info_text)
    
    def add_user(self):
        """Aggiunge un nuovo utente."""
        dialog = UserRegistrationDialog(parent=self)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            user_data = dialog.get_user_data()
            
            nome = user_data['nome']
            cognome = user_data['cognome']
            foto = user_data['foto']
            
            # Validazione
            if not nome or not cognome:
                QMessageBox.warning(
                    self,
                    "Errore",
                    "Nome e cognome sono obbligatori!"
                )
                return
            
            if foto is None:
                QMessageBox.warning(
                    self,
                    "Errore",
                    "È necessaria una foto per generare l'embedding facciale!"
                )
                return
            
            # Genera embedding
            embedding = self.face_encoder.encode_face(foto)
            
            if embedding is None:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Impossibile generare l'embedding facciale!"
                )
                return
            
            # Controlla duplicati
            duplicate_id = self.db_manager.check_duplicate(embedding)
            if duplicate_id:
                duplicate_user = self.db_manager.get_user(duplicate_id)
                result = QMessageBox.question(
                    self,
                    "Possibile Duplicato",
                    f"Esiste già un utente simile: {duplicate_user['nome']} {duplicate_user['cognome']}.\n"
                    f"Vuoi continuare comunque?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if result == QMessageBox.StandardButton.No:
                    return
            
            # Converti foto in bytes
            foto_bytes = None
            if foto is not None:
                _, buffer = cv2.imencode('.jpg', foto)
                foto_bytes = buffer.tobytes()
            
            # Aggiungi al database
            user_id = self.db_manager.add_user(nome, cognome, embedding, foto_bytes)
            
            if user_id > 0:
                QMessageBox.information(
                    self,
                    "Successo",
                    f"Utente {nome} {cognome} registrato con successo!"
                )
                self.refresh_user_list()
            else:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Utente già esistente o errore durante la registrazione!"
                )
    
    def delete_user(self):
        """Elimina l'utente selezionato."""
        selected_items = self.user_list.selectedItems()
        
        if not selected_items:
            return
        
        user_id = selected_items[0].data(Qt.ItemDataRole.UserRole)
        user = self.db_manager.get_user(user_id)
        
        if not user:
            return
        
        # Conferma eliminazione
        result = QMessageBox.question(
            self,
            "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare {user['nome']} {user['cognome']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_user(user_id):
                QMessageBox.information(
                    self,
                    "Successo",
                    "Utente eliminato con successo!"
                )
                self.refresh_user_list()
            else:
                QMessageBox.critical(
                    self,
                    "Errore",
                    "Errore durante l'eliminazione dell'utente!"
                )
    
    def handle_unknown_face(self, face_image, embedding):
        """
        Gestisce il rilevamento di un volto sconosciuto.
        
        Args:
            face_image: Immagine del volto
            embedding: Embedding del volto
        """
        # Mostra dialog per registrazione
        result = QMessageBox.question(
            self,
            "Volto Sconosciuto",
            "Rilevato un volto sconosciuto. Vuoi registrare questo utente?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            dialog = UserRegistrationDialog(face_image=face_image, parent=self)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                user_data = dialog.get_user_data()
                
                nome = user_data['nome'] or "Sconosciuto"
                cognome = user_data['cognome'] or ""
                
                # Converti foto in bytes
                foto_bytes = None
                if face_image is not None:
                    _, buffer = cv2.imencode('.jpg', face_image)
                    foto_bytes = buffer.tobytes()
                
                # Aggiungi al database
                user_id = self.db_manager.add_user(nome, cognome, embedding, foto_bytes)
                
                if user_id > 0:
                    QMessageBox.information(
                        self,
                        "Successo",
                        f"Utente {nome} {cognome} registrato con successo!"
                    )
                    self.refresh_user_list()
