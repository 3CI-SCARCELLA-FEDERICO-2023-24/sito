"""
Face recognizer module using DeepFace for face recognition and embedding
"""
import os
import cv2
import numpy as np
from typing import Optional, Tuple, List
from deepface import DeepFace
from modules import config
import tempfile


class FaceRecognizer:
    """Face recognizer using DeepFace"""
    
    def __init__(self):
        """Initialize face recognizer"""
        self.model_name = config.RECOGNITION_MODEL
        self.distance_metric = config.DISTANCE_METRIC
        self.threshold = config.RECOGNITION_THRESHOLD
        
        # Cache for embeddings
        self.embedding_cache = {}
        
        # Pre-build model to avoid delays on first use
        try:
            self._initialize_model()
        except Exception as e:
            print(f"Warning: Could not pre-initialize model: {e}")
    
    def _initialize_model(self):
        """Pre-initialize the face recognition model"""
        # Create a dummy image to force model loading
        dummy_img = np.zeros((160, 160, 3), dtype=np.uint8)
        temp_path = os.path.join(tempfile.gettempdir(), "dummy_face.jpg")
        
        try:
            cv2.imwrite(temp_path, dummy_img)
            # This will download and cache the model
            DeepFace.represent(img_path=temp_path, 
                             model_name=self.model_name,
                             enforce_detection=False)
        except Exception as e:
            print(f"Model initialization note: {e}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def get_embedding(self, face_image: np.ndarray) -> Optional[List[float]]:
        """
        Get face embedding vector
        
        Args:
            face_image: Face image (RGB format)
            
        Returns:
            Embedding vector or None if failed
        """
        try:
            # DeepFace expects RGB image
            if face_image.shape[2] == 3 and len(face_image.shape) == 3:
                # Get embedding
                embedding_objs = DeepFace.represent(
                    img_path=face_image,
                    model_name=self.model_name,
                    enforce_detection=False,
                    detector_backend='skip'  # We already detected the face
                )
                
                if embedding_objs and len(embedding_objs) > 0:
                    embedding = embedding_objs[0]["embedding"]
                    return embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
        
        return None
    
    def get_embedding_from_path(self, image_path: str) -> Optional[List[float]]:
        """
        Get face embedding from image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Embedding vector or None if failed
        """
        # Check cache first
        if image_path in self.embedding_cache:
            return self.embedding_cache[image_path]
        
        try:
            embedding_objs = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                enforce_detection=False
            )
            
            if embedding_objs and len(embedding_objs) > 0:
                embedding = embedding_objs[0]["embedding"]
                # Cache the result
                self.embedding_cache[image_path] = embedding
                return embedding
        except Exception as e:
            print(f"Error getting embedding from path: {e}")
        
        return None
    
    def compare_embeddings(self, embedding1: List[float], 
                          embedding2: List[float]) -> Tuple[float, bool]:
        """
        Compare two face embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Tuple of (distance, is_match)
        """
        if not embedding1 or not embedding2:
            return (float('inf'), False)
        
        try:
            # Convert to numpy arrays
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Calculate distance based on metric
            if self.distance_metric == "cosine":
                distance = self._cosine_distance(emb1, emb2)
            elif self.distance_metric == "euclidean":
                distance = self._euclidean_distance(emb1, emb2)
            elif self.distance_metric == "euclidean_l2":
                distance = self._euclidean_l2_distance(emb1, emb2)
            else:
                distance = self._cosine_distance(emb1, emb2)
            
            # Check if match based on threshold
            is_match = distance <= self.threshold
            
            return (distance, is_match)
        except Exception as e:
            print(f"Error comparing embeddings: {e}")
            return (float('inf'), False)
    
    def find_best_match(self, query_embedding: List[float], 
                       database_embeddings: List[Tuple[int, List[float]]]) -> Optional[Tuple[int, float]]:
        """
        Find best matching face from database
        
        Args:
            query_embedding: Query face embedding
            database_embeddings: List of (person_id, embedding) tuples
            
        Returns:
            Tuple of (person_id, distance) for best match, or None if no match
        """
        if not query_embedding or not database_embeddings:
            return None
        
        best_match = None
        best_distance = float('inf')
        
        for person_id, db_embedding in database_embeddings:
            if db_embedding:
                distance, is_match = self.compare_embeddings(query_embedding, db_embedding)
                
                if is_match and distance < best_distance:
                    best_distance = distance
                    best_match = (person_id, distance)
        
        return best_match
    
    def verify_face(self, face_image1: np.ndarray, face_image2: np.ndarray) -> Tuple[bool, float]:
        """
        Verify if two face images are of the same person
        
        Args:
            face_image1: First face image
            face_image2: Second face image
            
        Returns:
            Tuple of (is_same_person, confidence)
        """
        try:
            result = DeepFace.verify(
                img1_path=face_image1,
                img2_path=face_image2,
                model_name=self.model_name,
                distance_metric=self.distance_metric,
                enforce_detection=False,
                detector_backend='skip'
            )
            
            is_verified = result['verified']
            distance = result['distance']
            
            return (is_verified, 1.0 - distance)
        except Exception as e:
            print(f"Error verifying faces: {e}")
            return (False, 0.0)
    
    @staticmethod
    def _cosine_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate cosine distance between embeddings"""
        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)
        
        if norm1 == 0 or norm2 == 0:
            return 1.0
        
        cosine_similarity = dot_product / (norm1 * norm2)
        cosine_distance = 1.0 - cosine_similarity
        
        return cosine_distance
    
    @staticmethod
    def _euclidean_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate Euclidean distance between embeddings"""
        return np.linalg.norm(emb1 - emb2)
    
    @staticmethod
    def _euclidean_l2_distance(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate L2 normalized Euclidean distance between embeddings"""
        # Normalize embeddings
        emb1_normalized = emb1 / np.linalg.norm(emb1)
        emb2_normalized = emb2 / np.linalg.norm(emb2)
        
        return np.linalg.norm(emb1_normalized - emb2_normalized)
    
    def clear_cache(self):
        """Clear embedding cache"""
        self.embedding_cache.clear()
    
    def set_threshold(self, threshold: float):
        """
        Set recognition threshold
        
        Args:
            threshold: New threshold value (0.0-1.0)
        """
        self.threshold = max(0.0, min(1.0, threshold))
