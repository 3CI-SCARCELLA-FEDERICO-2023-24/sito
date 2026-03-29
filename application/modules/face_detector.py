"""
Face detector module using MediaPipe for face detection
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional
from modules import config


class FaceDetector:
    """Face detector using MediaPipe Face Detection"""
    
    def __init__(self, min_detection_confidence: float = config.MIN_DETECTION_CONFIDENCE):
        """
        Initialize face detector
        
        Args:
            min_detection_confidence: Minimum confidence for detection
        """
        self.min_detection_confidence = min_detection_confidence
        
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,  # 1 for full range, 0 for short range (< 2 meters)
            min_detection_confidence=min_detection_confidence
        )
    
    def detect_faces(self, frame: np.ndarray) -> List[Tuple[int, int, int, int, float]]:
        """
        Detect faces in a frame
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            List of tuples (x, y, width, height, confidence)
        """
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        results = self.face_detection.process(rgb_frame)
        
        faces = []
        if results.detections:
            h, w, _ = frame.shape
            
            for detection in results.detections:
                # Get bounding box
                bboxC = detection.location_data.relative_bounding_box
                
                # Convert relative coordinates to absolute
                x = int(bboxC.xmin * w)
                y = int(bboxC.ymin * h)
                width = int(bboxC.width * w)
                height = int(bboxC.height * h)
                
                # Get confidence
                confidence = detection.score[0]
                
                # Ensure coordinates are within frame bounds
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                faces.append((x, y, width, height, confidence))
        
        return faces
    
    def extract_face_region(self, frame: np.ndarray, x: int, y: int, 
                           w: int, h: int, padding: float = 0.2) -> Optional[np.ndarray]:
        """
        Extract face region from frame with optional padding
        
        Args:
            frame: Input frame
            x, y: Top-left corner of face bounding box
            w, h: Width and height of face bounding box
            padding: Padding factor (0.2 = 20% padding on each side)
            
        Returns:
            Extracted face region or None if invalid
        """
        if w <= 0 or h <= 0:
            return None
        
        frame_h, frame_w = frame.shape[:2]
        
        # Calculate padding
        pad_w = int(w * padding)
        pad_h = int(h * padding)
        
        # Calculate padded coordinates
        x1 = max(0, x - pad_w)
        y1 = max(0, y - pad_h)
        x2 = min(frame_w, x + w + pad_w)
        y2 = min(frame_h, y + h + pad_h)
        
        # Extract face region
        face_region = frame[y1:y2, x1:x2]
        
        return face_region if face_region.size > 0 else None
    
    def draw_faces(self, frame: np.ndarray, 
                   faces: List[Tuple[int, int, int, int, float]],
                   labels: List[str] = None,
                   color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        Draw bounding boxes and labels on detected faces
        
        Args:
            frame: Frame to draw on
            faces: List of detected faces (x, y, w, h, confidence)
            labels: Optional list of labels for each face
            color: BGR color for bounding boxes
            
        Returns:
            Frame with drawn faces
        """
        for i, (x, y, w, h, confidence) in enumerate(faces):
            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Prepare label
            if labels and i < len(labels):
                label = labels[i]
            else:
                label = f"Face {i+1}"
            
            # Add confidence to label
            label_with_conf = f"{label} ({confidence:.2f})"
            
            # Draw label background
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            text_size = cv2.getTextSize(label_with_conf, font, font_scale, thickness)[0]
            
            # Position label above the bounding box
            label_y = y - 10 if y - 10 > 10 else y + h + 20
            
            cv2.rectangle(frame, 
                         (x, label_y - text_size[1] - 5),
                         (x + text_size[0] + 5, label_y + 5),
                         (0, 0, 0), -1)
            
            # Draw label text
            cv2.putText(frame, label_with_conf, (x, label_y), 
                       font, font_scale, color, thickness)
        
        return frame
    
    def get_largest_face(self, faces: List[Tuple[int, int, int, int, float]]) -> Optional[Tuple[int, int, int, int, float]]:
        """
        Get the largest face from a list of detected faces
        
        Args:
            faces: List of detected faces
            
        Returns:
            Largest face tuple or None if no faces
        """
        if not faces:
            return None
        
        # Find face with largest area
        largest_face = max(faces, key=lambda f: f[2] * f[3])
        return largest_face
    
    def preprocess_face_for_recognition(self, face_image: np.ndarray, 
                                       target_size: Tuple[int, int] = config.FACE_IMAGE_SIZE) -> np.ndarray:
        """
        Preprocess face image for recognition
        
        Args:
            face_image: Input face image
            target_size: Target size (width, height)
            
        Returns:
            Preprocessed face image
        """
        # Resize to target size
        resized = cv2.resize(face_image, target_size)
        
        # Convert to RGB
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        return rgb
    
    def close(self):
        """Close face detection resources"""
        if hasattr(self, 'face_detection'):
            self.face_detection.close()
    
    def __del__(self):
        """Cleanup on deletion"""
        self.close()
