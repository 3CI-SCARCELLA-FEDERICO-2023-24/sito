"""Camera widget for displaying live video feed."""
import cv2
import numpy as np
import logging
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
import config

logger = logging.getLogger(__name__)


class CameraWidget(QWidget):
    """Widget for displaying camera feed and detected faces."""
    
    # Signal emitted when a face is detected
    face_detected = pyqtSignal(np.ndarray, tuple)  # frame, bbox
    
    def __init__(self, parent=None):
        """Initialize camera widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.camera = None
        self.current_frame = None
        self.detected_faces = []
        self.face_labels = []
        
        # Initialize face detector once
        from face_recognition import FaceDetector
        self.face_detector = FaceDetector()
        
        self._init_ui()
        self._init_camera()
    
    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        
        # Video label
        self.video_label = QLabel()
        self.video_label.setMinimumSize(config.CAMERA_WIDTH, config.CAMERA_HEIGHT)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #ccc;")
        
        layout.addWidget(self.video_label)
        self.setLayout(layout)
        
        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
    
    def _init_camera(self):
        """Initialize camera capture."""
        self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
    
    def start(self):
        """Start camera feed."""
        if self.camera and self.camera.isOpened():
            self.timer.start(33)  # ~30 FPS
    
    def stop(self):
        """Stop camera feed."""
        self.timer.stop()
    
    def _update_frame(self):
        """Update camera frame."""
        if not self.camera or not self.camera.isOpened():
            return
        
        ret, frame = self.camera.read()
        if ret:
            self.current_frame = frame.copy()
            self._display_frame(frame)
    
    def _display_frame(self, frame):
        """Display frame on label.
        
        Args:
            frame: Frame to display
        """
        # Draw faces if any
        if self.detected_faces:
            self.face_detector.draw_faces(frame, self.detected_faces, self.face_labels)
        
        # Convert to QImage
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Display
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)
    
    def set_detected_faces(self, faces, labels=None):
        """Set detected faces to display.
        
        Args:
            faces: List of face bounding boxes
            labels: Optional list of labels for each face
        """
        self.detected_faces = faces
        self.face_labels = labels or []
    
    def get_current_frame(self):
        """Get current camera frame.
        
        Returns:
            Current frame as numpy array
        """
        return self.current_frame.copy() if self.current_frame is not None else None
    
    def capture_frame(self):
        """Capture and return current frame.
        
        Returns:
            Captured frame
        """
        return self.get_current_frame()
    
    def closeEvent(self, event):
        """Handle widget close event.
        
        Args:
            event: Close event
        """
        self.stop()
        if self.camera:
            self.camera.release()
        event.accept()
