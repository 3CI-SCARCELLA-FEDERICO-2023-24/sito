"""
Generazione di embeddings facciali usando FaceNet.
"""

import cv2
import numpy as np
from typing import Optional
import config

try:
    from facenet_pytorch import InceptionResnetV1
    import torch
    FACENET_AVAILABLE = True
except ImportError:
    FACENET_AVAILABLE = False
    print("Warning: facenet-pytorch non disponibile. Usando embedding semplificato.")


class FaceEncoder:
    """Genera embeddings facciali usando FaceNet."""
    
    def __init__(self):
        """Inizializza l'encoder facciale."""
        self.model = None
        self.device = None
        
        if FACENET_AVAILABLE:
            self._initialize_facenet()
        else:
            print("Usando encoder semplificato basato su feature estratte.")
    
    def _initialize_facenet(self):
        """Inizializza il modello FaceNet."""
        try:
            # Usa CUDA se disponibile, altrimenti CPU
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            
            # Carica il modello pre-addestrato
            # 'vggface2' è un dataset popolare per il riconoscimento facciale
            self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
            
            print(f"FaceNet inizializzato su {self.device}")
        except Exception as e:
            print(f"Errore inizializzazione FaceNet: {e}")
            self.model = None
    
    def encode_face(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Genera un embedding per un'immagine di un volto.
        
        Args:
            face_image: Immagine del volto (BGR)
            
        Returns:
            Embedding del volto (numpy array) o None
        """
        if face_image is None or face_image.size == 0:
            return None
        
        if self.model is not None and FACENET_AVAILABLE:
            return self._encode_with_facenet(face_image)
        else:
            return self._encode_simple(face_image)
    
    def _encode_with_facenet(self, face_image: np.ndarray) -> Optional[np.ndarray]:
        """
        Genera embedding usando FaceNet.
        
        Args:
            face_image: Immagine del volto
            
        Returns:
            Embedding del volto
        """
        try:
            # Pre-processing
            # 1. Ridimensiona a 160x160 (input FaceNet)
            face_resized = cv2.resize(face_image, (160, 160))
            
            # 2. Converti BGR a RGB
            face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
            
            # 3. Normalizza pixel values a [-1, 1]
            face_normalized = (face_rgb.astype(np.float32) - 127.5) / 128.0
            
            # 4. Converti a tensor PyTorch
            # Shape: (1, 3, 160, 160) - batch, canali, altezza, larghezza
            face_tensor = torch.from_numpy(face_normalized).permute(2, 0, 1).unsqueeze(0)
            face_tensor = face_tensor.to(self.device)
            
            # 5. Genera embedding
            with torch.no_grad():
                embedding = self.model(face_tensor)
            
            # 6. Converti a numpy
            embedding_np = embedding.cpu().numpy().flatten()
            
            # 7. Normalizza l'embedding
            embedding_normalized = embedding_np / np.linalg.norm(embedding_np)
            
            return embedding_normalized
            
        except Exception as e:
            print(f"Errore nella generazione dell'embedding: {e}")
            return self._encode_simple(face_image)
    
    def _encode_simple(self, face_image: np.ndarray) -> np.ndarray:
        """
        Genera un embedding semplificato basato su feature estratte.
        Questo è un fallback quando FaceNet non è disponibile.
        
        Args:
            face_image: Immagine del volto
            
        Returns:
            Embedding semplificato
        """
        try:
            # Ridimensiona a dimensione fissa
            face_resized = cv2.resize(face_image, config.FACENET_INPUT_SIZE)
            
            # Converti in grayscale
            face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            
            # Estrai feature usando istogramma e statistiche
            hist = cv2.calcHist([face_gray], [0], None, [32], [0, 256])
            hist = hist.flatten()
            hist = hist / (hist.sum() + 1e-7)  # Normalizza
            
            # Calcola statistiche
            mean = np.mean(face_gray)
            std = np.std(face_gray)
            
            # Estrai bordi
            edges = cv2.Canny(face_gray, 50, 150)
            edge_density = np.mean(edges) / 255.0
            
            # Ridimensiona ulteriormente per feature spaziali
            face_small = cv2.resize(face_gray, (16, 16))
            spatial_features = face_small.flatten() / 255.0
            
            # Combina tutte le feature
            features = np.concatenate([
                hist,  # 32 valori
                [mean / 255.0, std / 255.0, edge_density],  # 3 valori
                spatial_features  # 256 valori
            ])
            
            # Normalizza
            features = features / (np.linalg.norm(features) + 1e-7)
            
            # Padding o troncamento a dimensione fissa
            if len(features) < config.EMBEDDING_SIZE:
                features = np.pad(features, (0, config.EMBEDDING_SIZE - len(features)))
            else:
                features = features[:config.EMBEDDING_SIZE]
            
            return features
            
        except Exception as e:
            print(f"Errore nella generazione dell'embedding semplificato: {e}")
            # Ritorna embedding casuale come ultima risorsa
            return np.random.randn(config.EMBEDDING_SIZE)
    
    def batch_encode(self, face_images: list) -> list:
        """
        Genera embeddings per una lista di volti.
        
        Args:
            face_images: Lista di immagini di volti
            
        Returns:
            Lista di embeddings
        """
        embeddings = []
        for face_img in face_images:
            embedding = self.encode_face(face_img)
            if embedding is not None:
                embeddings.append(embedding)
        
        return embeddings
