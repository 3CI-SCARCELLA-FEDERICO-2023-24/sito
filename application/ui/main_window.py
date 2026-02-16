"""
Main window for facial recognition application
"""
import os
import cv2
import numpy as np
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QStatusBar, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from modules.database import FaceDatabase
from modules.camera import Camera
from modules.face_detector import FaceDetector
from modules.face_recognizer import FaceRecognizer
from modules import config
from ui.management_panel import ManagementPanel
import datetime


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize main window"""
        super().__init__()
        
        # Initialize components
        self.database = FaceDatabase()
        self.camera = Camera()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()
        
        # State variables
        self.camera_thread = None
        self.current_frame = None
        self.is_processing = False
        self.frame_counter = 0
        self.current_recognized_person = None
        self.last_unknown_time = None
        
        # UI setup
        self.setWindowTitle("Sistema di Riconoscimento Facciale")
        self.setGeometry(100, 100, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        self.init_ui()
        self.load_stylesheet()
        
        # Start camera
        self.start_camera()
    
    def init_ui(self):
        """Initialize user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left panel - Video feed
        left_panel = self._create_video_panel()
        main_layout.addWidget(left_panel, 2)
        
        # Right panel - Controls and info
        right_panel = self._create_control_panel()
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
        # FPS label in status bar
        self.fps_label = QLabel("FPS: 0")
        self.fps_label.setObjectName("status")
        self.status_bar.addPermanentWidget(self.fps_label)
    
    def _create_video_panel(self) -> QGroupBox:
        """Create video feed panel"""
        group = QGroupBox("Anteprima Video")
        layout = QVBoxLayout()
        
        # Video display label
        self.video_label = QLabel()
        self.video_label.setObjectName("video")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumSize(config.VIDEO_DISPLAY_WIDTH, config.VIDEO_DISPLAY_HEIGHT)
        self.video_label.setScaledContents(False)
        self.video_label.setText("Avvio webcam...")
        layout.addWidget(self.video_label)
        
        # Recognized name label
        self.recognized_label = QLabel("In attesa di rilevamento...")
        self.recognized_label.setObjectName("recognized_name")
        self.recognized_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recognized_label.setMinimumHeight(50)
        layout.addWidget(self.recognized_label)
        
        group.setLayout(layout)
        return group
    
    def _create_control_panel(self) -> QGroupBox:
        """Create control panel"""
        group = QGroupBox("Controlli")
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Sistema di Riconoscimento Facciale")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Management button
        self.management_btn = QPushButton("Gestione Persone")
        self.management_btn.clicked.connect(self.open_management)
        self.management_btn.setMinimumHeight(50)
        layout.addWidget(self.management_btn)
        
        # Statistics group
        stats_group = QGroupBox("Statistiche")
        stats_layout = QVBoxLayout()
        
        self.total_persons_label = QLabel("Persone registrate: 0")
        stats_layout.addWidget(self.total_persons_label)
        
        self.unknown_count_label = QLabel("Sconosciuti: 0")
        stats_layout.addWidget(self.unknown_count_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Info group
        info_group = QGroupBox("Informazioni")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "• Il sistema rileva automaticamente i volti\n"
            "• I volti sconosciuti vengono registrati automaticamente\n"
            "• Usa 'Gestione' per modificare le informazioni\n"
            "• I volti riconosciuti vengono evidenziati in verde"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Add stretch
        layout.addStretch()
        
        # Exit button
        self.exit_btn = QPushButton("Esci")
        self.exit_btn.setObjectName("danger")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)
        
        group.setLayout(layout)
        return group
    
    def load_stylesheet(self):
        """Load QSS stylesheet"""
        stylesheet_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
    
    def start_camera(self):
        """Start camera capture"""
        try:
            self.camera_thread = self.camera.start()
            self.camera_thread.frame_ready.connect(self.on_frame_ready)
            self.camera_thread.error_occurred.connect(self.on_camera_error)
            self.camera_thread.fps_updated.connect(self.on_fps_updated)
            
            self.status_bar.showMessage("Webcam avviata")
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile avviare la webcam: {e}")
    
    def stop_camera(self):
        """Stop camera capture"""
        if self.camera:
            self.camera.stop()
            self.status_bar.showMessage("Webcam fermata")
    
    @pyqtSlot(np.ndarray)
    def on_frame_ready(self, frame: np.ndarray):
        """
        Handle new frame from camera
        
        Args:
            frame: Captured frame
        """
        self.current_frame = frame.copy()
        
        # Process frame for face detection and recognition
        if not self.is_processing and self.frame_counter % config.PROCESS_EVERY_N_FRAMES == 0:
            self.process_frame(frame)
        
        self.frame_counter += 1
        
        # Display frame
        self.display_frame(frame)
    
    def process_frame(self, frame: np.ndarray):
        """
        Process frame for face detection and recognition
        
        Args:
            frame: Frame to process
        """
        self.is_processing = True
        
        try:
            # Detect faces
            faces = self.face_detector.detect_faces(frame)
            
            if faces:
                # Process the largest face
                largest_face = self.face_detector.get_largest_face(faces)
                if largest_face:
                    x, y, w, h, confidence = largest_face
                    
                    # Extract face region
                    face_region = self.face_detector.extract_face_region(frame, x, y, w, h)
                    
                    if face_region is not None:
                        # Preprocess face
                        preprocessed_face = self.face_detector.preprocess_face_for_recognition(face_region)
                        
                        # Get face embedding
                        embedding = self.face_recognizer.get_embedding(preprocessed_face)
                        
                        if embedding:
                            # Try to match with database
                            match = self.recognize_face(embedding)
                            
                            if match:
                                person_id, distance = match
                                person = self.database.get_person(person_id)
                                
                                if person:
                                    # Update recognized person
                                    full_name = f"{person['name']} {person['surname']}".strip()
                                    self.current_recognized_person = full_name
                                    
                                    # Record detection
                                    self.database.add_detection(person_id, 1.0 - distance)
                                    
                                    # Draw green box for recognized person
                                    self.face_detector.draw_faces(
                                        frame, [largest_face], 
                                        [full_name], 
                                        color=(0, 255, 0)
                                    )
                            else:
                                # Unknown person - register automatically
                                self.register_unknown_face(face_region, embedding)
                                
                                # Draw yellow box for unknown person
                                self.face_detector.draw_faces(
                                    frame, [largest_face], 
                                    [config.DEFAULT_UNKNOWN_NAME], 
                                    color=(0, 255, 255)
                                )
                    
                    self.update_statistics()
            else:
                # No faces detected
                self.current_recognized_person = None
                self.recognized_label.setText("Nessun volto rilevato")
        
        except Exception as e:
            print(f"Error processing frame: {e}")
        
        finally:
            self.is_processing = False
    
    def recognize_face(self, embedding: list) -> tuple:
        """
        Recognize face from embedding
        
        Args:
            embedding: Face embedding vector
            
        Returns:
            Tuple of (person_id, distance) or None if no match
        """
        # Get all persons with embeddings
        persons = self.database.get_all_persons(include_unknown=True)
        
        database_embeddings = []
        for person in persons:
            if person['face_embedding']:
                database_embeddings.append((person['id'], person['face_embedding']))
        
        # Find best match
        match = self.face_recognizer.find_best_match(embedding, database_embeddings)
        
        return match
    
    def register_unknown_face(self, face_image: np.ndarray, embedding: list):
        """
        Register an unknown face automatically
        
        Args:
            face_image: Face image
            embedding: Face embedding
        """
        # Check if we should register (avoid too frequent registrations)
        now = datetime.datetime.now()
        if self.last_unknown_time:
            time_diff = (now - self.last_unknown_time).total_seconds()
            if time_diff < 5:  # Don't register more than once every 5 seconds
                return
        
        self.last_unknown_time = now
        
        # Generate unique filename
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"unknown_{timestamp}.{config.FACE_IMAGE_FORMAT}"
        photo_path = os.path.join(config.FACES_DIR, filename)
        
        # Save face image
        success = self.camera.save_frame_as_image(
            face_image, 
            photo_path, 
            resize=config.FACE_IMAGE_SIZE
        )
        
        if success:
            # Add to database
            person_id = self.database.add_person(
                name=config.DEFAULT_UNKNOWN_NAME,
                surname=config.DEFAULT_UNKNOWN_SURNAME,
                photo_path=photo_path,
                face_embedding=embedding,
                is_unknown=True
            )
            
            print(f"Registered unknown person with ID: {person_id}")
            self.update_statistics()
    
    def display_frame(self, frame: np.ndarray):
        """
        Display frame in video label
        
        Args:
            frame: Frame to display
        """
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to QImage
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scale to fit label
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.video_label.setPixmap(scaled_pixmap)
        
        # Update recognized label
        if self.current_recognized_person:
            self.recognized_label.setText(f"Riconosciuto: {self.current_recognized_person}")
        elif not self.is_processing:
            self.recognized_label.setText("In attesa di rilevamento...")
    
    @pyqtSlot(str)
    def on_camera_error(self, error: str):
        """
        Handle camera error
        
        Args:
            error: Error message
        """
        self.status_bar.showMessage(f"Errore: {error}")
        QMessageBox.warning(self, "Errore Webcam", error)
    
    @pyqtSlot(float)
    def on_fps_updated(self, fps: float):
        """
        Handle FPS update
        
        Args:
            fps: Current FPS
        """
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    def update_statistics(self):
        """Update statistics display"""
        persons = self.database.get_all_persons(include_unknown=True)
        
        total = len(persons)
        unknown = len([p for p in persons if p['is_unknown']])
        
        self.total_persons_label.setText(f"Persone registrate: {total}")
        self.unknown_count_label.setText(f"Sconosciuti: {unknown}")
    
    def open_management(self):
        """Open management panel"""
        management_panel = ManagementPanel(self.database, self)
        management_panel.person_updated.connect(self.on_person_updated)
        management_panel.exec()
    
    def on_person_updated(self):
        """Handle person update from management panel"""
        self.update_statistics()
        # Clear embedding cache in recognizer
        self.face_recognizer.clear_cache()
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop camera
        self.stop_camera()
        
        # Close database
        self.database.close()
        
        # Close face detector
        self.face_detector.close()
        
        event.accept()
