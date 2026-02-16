"""
Rilevamento volti usando MediaPipe.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple
import config


class FaceDetector:
    """Rileva volti usando MediaPipe Face Detection."""
    
    def __init__(self):
        """Inizializza il rilevatore di volti MediaPipe."""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=config.MEDIAPIPE_MIN_DETECTION_CONFIDENCE,
            model_selection=1  # 1 per modello a lungo raggio (migliore per volti distanti)
        )
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[Tuple[int, int, int, int], float]]:
        """
        Rileva volti nell'immagine.
        
        Args:
            image: Immagine in formato BGR (OpenCV)
            
        Returns:
            Lista di tuple ((x, y, w, h), confidence) per ogni volto rilevato
        """
        # Converti BGR a RGB per MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Processa l'immagine
        results = self.face_detection.process(image_rgb)
        
        faces = []
        
        if results.detections:
            h, w, _ = image.shape
            
            for detection in results.detections:
                # Ottieni il bounding box
                bbox = detection.location_data.relative_bounding_box
                
                # Converti coordinate relative in pixel
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Assicurati che le coordinate siano dentro l'immagine
                x = max(0, x)
                y = max(0, y)
                width = min(width, w - x)
                height = min(height, h - y)
                
                # Filtra volti troppo piccoli
                if width >= config.MIN_FACE_SIZE and height >= config.MIN_FACE_SIZE:
                    confidence = detection.score[0]
                    faces.append(((x, y, width, height), confidence))
        
        return faces
    
    def extract_face(self, image: np.ndarray, bbox: Tuple[int, int, int, int],
                    margin: float = 0.2) -> np.ndarray:
        """
        Estrae una regione del volto dall'immagine.
        
        Args:
            image: Immagine sorgente
            bbox: Bounding box (x, y, w, h)
            margin: Margine aggiuntivo intorno al volto (frazione)
            
        Returns:
            Immagine del volto estratto
        """
        x, y, w, h = bbox
        
        # Aggiungi margine
        margin_x = int(w * margin)
        margin_y = int(h * margin)
        
        x1 = max(0, x - margin_x)
        y1 = max(0, y - margin_y)
        x2 = min(image.shape[1], x + w + margin_x)
        y2 = min(image.shape[0], y + h + margin_y)
        
        face_img = image[y1:y2, x1:x2]
        
        return face_img
    
    def draw_detections(self, image: np.ndarray, 
                       faces: List[Tuple[Tuple[int, int, int, int], float]],
                       labels: List[str] = None,
                       color: Tuple[int, int, int] = None) -> np.ndarray:
        """
        Disegna i bounding box dei volti rilevati.
        
        Args:
            image: Immagine su cui disegnare
            faces: Lista di volti rilevati
            labels: Lista di etichette per ogni volto (opzionale)
            color: Colore del bounding box (opzionale)
            
        Returns:
            Immagine con le annotazioni
        """
        output = image.copy()
        
        if color is None:
            color = config.COLOR_BOX
        
        for i, (bbox, confidence) in enumerate(faces):
            x, y, w, h = bbox
            
            # Disegna il rettangolo
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
            
            # Prepara il testo
            if labels and i < len(labels):
                text = f"{labels[i]} ({confidence:.2f})"
            else:
                text = f"Face ({confidence:.2f})"
            
            # Disegna il testo
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            
            # Calcola dimensioni del testo per lo sfondo
            (text_width, text_height), baseline = cv2.getTextSize(
                text, font, font_scale, thickness
            )
            
            # Disegna sfondo per il testo
            cv2.rectangle(
                output,
                (x, y - text_height - 10),
                (x + text_width, y),
                color,
                -1
            )
            
            # Disegna il testo
            cv2.putText(
                output,
                text,
                (x, y - 5),
                font,
                font_scale,
                (0, 0, 0),
                thickness
            )
        
        return output
    
    def close(self):
        """Chiude il rilevatore."""
        if self.face_detection:
            self.face_detection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
