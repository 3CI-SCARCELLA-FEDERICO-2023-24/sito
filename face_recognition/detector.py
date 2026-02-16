"""Face detection using MediaPipe."""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
import config


class FaceDetector:
    """Handles face detection using MediaPipe Face Detection."""
    
    def __init__(self):
        """Initialize MediaPipe Face Detection."""
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            model_selection=1  # 1 for faces within 5 meters
        )
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in a frame.
        
        Args:
            frame: Input image as numpy array (BGR format)
            
        Returns:
            List of bounding boxes as (x, y, width, height)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            h, w, _ = frame.shape
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Ensure coordinates are within frame bounds
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                faces.append((x, y, width, height))
        
        return faces
    
    def extract_face(self, frame: np.ndarray, bbox: Tuple[int, int, int, int],
                    margin: float = 0.2) -> Optional[np.ndarray]:
        """Extract face region from frame with margin.
        
        Args:
            frame: Input image
            bbox: Bounding box as (x, y, width, height)
            margin: Margin to add around face (as fraction of bbox size)
            
        Returns:
            Cropped face image or None if extraction fails
        """
        x, y, w, h = bbox
        
        # Add margin
        margin_w = int(w * margin)
        margin_h = int(h * margin)
        
        x1 = max(0, x - margin_w)
        y1 = max(0, y - margin_h)
        x2 = min(frame.shape[1], x + w + margin_w)
        y2 = min(frame.shape[0], y + h + margin_h)
        
        if x2 <= x1 or y2 <= y1:
            return None
        
        face = frame[y1:y2, x1:x2]
        return face
    
    def draw_faces(self, frame: np.ndarray, faces: List[Tuple[int, int, int, int]],
                  labels: List[str] = None, color: Tuple[int, int, int] = (0, 255, 0)):
        """Draw bounding boxes around detected faces.
        
        Args:
            frame: Input image to draw on
            faces: List of bounding boxes
            labels: Optional labels for each face
            color: Color for bounding box (BGR)
        """
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            if labels and i < len(labels):
                label = labels[i]
                # Draw label background
                label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (x, y - label_size[1] - 10), 
                            (x + label_size[0], y), color, -1)
                # Draw label text
                cv2.putText(frame, label, (x, y - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def __del__(self):
        """Cleanup MediaPipe resources."""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
