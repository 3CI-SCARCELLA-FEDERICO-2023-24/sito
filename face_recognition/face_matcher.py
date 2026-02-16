"""
Confronto e matching di embeddings facciali.
"""

import numpy as np
from typing import List, Tuple, Optional
import config


class FaceMatcher:
    """Confronta embeddings facciali per il riconoscimento."""
    
    def __init__(self, threshold: float = None):
        """
        Inizializza il matcher.
        
        Args:
            threshold: Soglia di distanza per il riconoscimento
        """
        self.threshold = threshold or config.FACE_RECOGNITION_THRESHOLD
    
    def compare_embeddings(self, embedding1: np.ndarray, 
                          embedding2: np.ndarray) -> float:
        """
        Calcola la distanza tra due embeddings.
        
        Args:
            embedding1: Primo embedding
            embedding2: Secondo embedding
            
        Returns:
            Distanza euclidea tra gli embeddings
        """
        # Distanza euclidea
        distance = np.linalg.norm(embedding1 - embedding2)
        return distance
    
    def cosine_similarity(self, embedding1: np.ndarray, 
                         embedding2: np.ndarray) -> float:
        """
        Calcola la similarità coseno tra due embeddings.
        
        Args:
            embedding1: Primo embedding
            embedding2: Secondo embedding
            
        Returns:
            Similarità coseno (0-1, più alto = più simile)
        """
        # Normalizza gli embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Calcola similarità coseno
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        
        # Converti da [-1, 1] a [0, 1]
        similarity = (similarity + 1) / 2
        
        return similarity
    
    def find_best_match(self, query_embedding: np.ndarray,
                       database_embeddings: List[Tuple[int, str, np.ndarray]]) -> Optional[Tuple[int, str, float]]:
        """
        Trova il miglior match per un embedding nel database.
        
        Args:
            query_embedding: Embedding da confrontare
            database_embeddings: Lista di (id, nome, embedding) dal database
            
        Returns:
            Tuple (id, nome, distanza) del miglior match o None
        """
        if not database_embeddings:
            return None
        
        best_match = None
        min_distance = float('inf')
        
        for user_id, nome, stored_embedding in database_embeddings:
            distance = self.compare_embeddings(query_embedding, stored_embedding)
            
            if distance < min_distance:
                min_distance = distance
                best_match = (user_id, nome, distance)
        
        # Verifica se il miglior match è sotto la soglia
        if best_match and best_match[2] < self.threshold:
            return best_match
        
        return None
    
    def find_all_matches(self, query_embedding: np.ndarray,
                        database_embeddings: List[Tuple[int, str, np.ndarray]],
                        top_k: int = 5) -> List[Tuple[int, str, float]]:
        """
        Trova i migliori K matches per un embedding.
        
        Args:
            query_embedding: Embedding da confrontare
            database_embeddings: Lista di (id, nome, embedding) dal database
            top_k: Numero di match da restituire
            
        Returns:
            Lista di tuple (id, nome, distanza) ordinate per distanza
        """
        if not database_embeddings:
            return []
        
        matches = []
        
        for user_id, nome, stored_embedding in database_embeddings:
            distance = self.compare_embeddings(query_embedding, stored_embedding)
            matches.append((user_id, nome, distance))
        
        # Ordina per distanza (più basso = migliore)
        matches.sort(key=lambda x: x[2])
        
        # Restituisci i primi K
        return matches[:top_k]
    
    def is_match(self, embedding1: np.ndarray, embedding2: np.ndarray) -> bool:
        """
        Verifica se due embeddings corrispondono.
        
        Args:
            embedding1: Primo embedding
            embedding2: Secondo embedding
            
        Returns:
            True se è un match, False altrimenti
        """
        distance = self.compare_embeddings(embedding1, embedding2)
        return distance < self.threshold
    
    def get_confidence_score(self, distance: float) -> float:
        """
        Converte una distanza in un punteggio di confidenza (0-100).
        
        Args:
            distance: Distanza euclidea
            
        Returns:
            Punteggio di confidenza (0-100)
        """
        # Converti distanza in confidenza
        # Distanza 0 = 100% confidenza
        # Distanza >= threshold = 0% confidenza
        
        if distance >= self.threshold:
            return 0.0
        
        confidence = (1 - (distance / self.threshold)) * 100
        confidence = max(0, min(100, confidence))
        
        return confidence
    
    def set_threshold(self, threshold: float):
        """
        Imposta una nuova soglia di riconoscimento.
        
        Args:
            threshold: Nuova soglia
        """
        self.threshold = threshold
