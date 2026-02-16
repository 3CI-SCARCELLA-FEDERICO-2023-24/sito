"""
Widget per l'anteprima della camera in tempo reale.
"""

import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import config


class CameraPreview(QWidget):
    """Widget per visualizzare l'anteprima della camera."""
    
    # Segnale emesso quando viene rilevato un volto sconosciuto
    unknown_face_detected = pyqtSignal(np.ndarray, np.ndarray)  # (face_image, embedding)
    
    def __init__(self, face_detector, face_encoder, face_matcher, db_manager, parent=None):
        """
        Inizializza il widget della camera.
        
        Args:
            face_detector: Istanza di FaceDetector
            face_encoder: Istanza di FaceEncoder
            face_matcher: Istanza di FaceMatcher
            db_manager: Istanza di DatabaseManager
            parent: Widget genitore
        """
        super().__init__(parent)
        
        self.face_detector = face_detector
        self.face_encoder = face_encoder
        self.face_matcher = face_matcher
        self.db_manager = db_manager
        
        self.camera = None
        self.timer = QTimer()
        self.is_running = False
        
        # Cache per gli embeddings del database
        self.database_embeddings = []
        
        # Debouncing per volti sconosciuti (evita popup multipli)
        self.unknown_faces_cooldown = {}  # {embedding_hash: timestamp}
        self.cooldown_seconds = 10  # Tempo minimo tra segnalazioni dello stesso volto
        
        self._init_ui()
        self._init_camera()
    
    def _init_ui(self):
        """Inizializza l'interfaccia utente."""
        layout = QVBoxLayout()
        
        # Label per mostrare il video
        self.video_label = QLabel()
        self.video_label.setMinimumSize(config.PREVIEW_WIDTH, config.PREVIEW_HEIGHT)
        self.video_label.setStyleSheet("border: 2px solid #333; background-color: black;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.video_label)
        
        # Pulsanti di controllo
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Avvia Camera")
        self.start_button.clicked.connect(self.start_camera)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Ferma Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
        
        # Label per le informazioni
        self.info_label = QLabel("Camera non attiva")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)
        
        self.setLayout(layout)
    
    def _init_camera(self):
        """Inizializza la camera."""
        try:
            self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
        except Exception as e:
            print(f"Errore inizializzazione camera: {e}")
            self.info_label.setText("Errore: Camera non disponibile")
    
    def start_camera(self):
        """Avvia la cattura video."""
        if self.camera is None or not self.camera.isOpened():
            self._init_camera()
        
        if self.camera and self.camera.isOpened():
            self.is_running = True
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # ~30 FPS
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.info_label.setText("Camera attiva - Riconoscimento in corso...")
            
            # Carica gli embeddings dal database
            self.refresh_database()
        else:
            self.info_label.setText("Errore: Impossibile avviare la camera")
    
    def stop_camera(self):
        """Ferma la cattura video."""
        self.is_running = False
        self.timer.stop()
        
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.info_label.setText("Camera ferma")
        
        # Pulisci il video label
        self.video_label.clear()
    
    def update_frame(self):
        """Aggiorna il frame corrente."""
        if not self.is_running or self.camera is None:
            return
        
        ret, frame = self.camera.read()
        
        if not ret:
            self.info_label.setText("Errore: Impossibile leggere dalla camera")
            return
        
        # Rileva volti
        faces = self.face_detector.detect_faces(frame)
        
        # Processa ogni volto
        labels = []
        for bbox, confidence in faces:
            # Estrai il volto
            face_img = self.face_detector.extract_face(frame, bbox)
            
            if face_img.size == 0:
                labels.append("Errore")
                continue
            
            # Genera embedding
            embedding = self.face_encoder.encode_face(face_img)
            
            if embedding is None:
                labels.append("Errore")
                continue
            
            # Cerca match nel database
            match = self.face_matcher.find_best_match(embedding, self.database_embeddings)
            
            if match:
                user_id, nome, distance = match
                confidence_score = self.face_matcher.get_confidence_score(distance)
                labels.append(f"{nome} ({confidence_score:.0f}%)")
            else:
                labels.append("Sconosciuto")
                # Emetti segnale per volto sconosciuto con debouncing
                self._emit_unknown_face_with_debounce(face_img, embedding)
        
        # Disegna i volti rilevati
        annotated_frame = self.face_detector.draw_detections(frame, faces, labels)
        
        # Converti in QPixmap e mostra
        self._display_frame(annotated_frame)
        
        # Aggiorna info
        if faces:
            self.info_label.setText(f"Rilevati {len(faces)} volti")
        else:
            self.info_label.setText("Nessun volto rilevato")
    
    def _display_frame(self, frame):
        """
        Visualizza un frame nel label.
        
        Args:
            frame: Frame da visualizzare (BGR)
        """
        # Converti BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Crea QImage
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scala l'immagine mantenendo l'aspect ratio
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.video_label.setPixmap(scaled_pixmap)
    
    def _emit_unknown_face_with_debounce(self, face_img: np.ndarray, embedding: np.ndarray):
        """
        Emette il segnale per volto sconosciuto con debouncing.
        
        Args:
            face_img: Immagine del volto
            embedding: Embedding del volto
        """
        import time
        
        # Crea un hash dell'embedding per identificare lo stesso volto
        # Usiamo una versione arrotondata per tollerare piccole variazioni
        embedding_hash = hash(tuple(np.round(embedding, 2)))
        
        current_time = time.time()
        
        # Pulisci vecchie entry dal cooldown (più vecchie di 60 secondi)
        old_keys = [k for k, v in self.unknown_faces_cooldown.items() 
                    if current_time - v > 60]
        for k in old_keys:
            del self.unknown_faces_cooldown[k]
        
        # Controlla se questo volto è in cooldown
        if embedding_hash in self.unknown_faces_cooldown:
            last_time = self.unknown_faces_cooldown[embedding_hash]
            if current_time - last_time < self.cooldown_seconds:
                # Ancora in cooldown, non emettere segnale
                return
        
        # Emetti segnale e aggiorna cooldown
        self.unknown_face_detected.emit(face_img, embedding)
        self.unknown_faces_cooldown[embedding_hash] = current_time
    
    def refresh_database(self):
        """Ricarica gli embeddings dal database."""
        self.database_embeddings = self.db_manager.get_all_embeddings()
        print(f"Database caricato: {len(self.database_embeddings)} utenti")
    
    def closeEvent(self, event):
        """Gestisce la chiusura del widget."""
        self.stop_camera()
        if self.camera:
            self.camera.release()
        event.accept()
