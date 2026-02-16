"""Face matching and comparison logic."""
import numpy as np
from typing import List, Tuple, Optional
from scipy.spatial.distance import cosine
import config


class FaceMatcher:
    """Handles face comparison and matching."""
    
    def __init__(self, threshold: float = None):
        """Initialize face matcher.
        
        Args:
            threshold: Similarity threshold for face matching
        """
        self.threshold = threshold or config.SIMILARITY_THRESHOLD
    
    def compare_embeddings(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compare two face embeddings using cosine similarity.
        
        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
            
        Returns:
            Similarity score (1 - cosine distance), higher is more similar
        """
        # Calculate cosine similarity (1 - cosine distance)
        similarity = 1 - cosine(embedding1, embedding2)
        return similarity
    
    def find_match(self, query_embedding: np.ndarray, 
                   known_embeddings: List[np.ndarray],
                   user_ids: List[int] = None) -> Tuple[Optional[int], float]:
        """Find the best matching face from known embeddings.
        
        Args:
            query_embedding: Embedding to match
            known_embeddings: List of known face embeddings
            user_ids: List of user IDs corresponding to embeddings
            
        Returns:
            Tuple of (user_id or index, similarity_score) or (None, 0) if no match
        """
        if not known_embeddings:
            return None, 0.0
        
        best_match_idx = None
        best_similarity = 0.0
        
        for idx, known_embedding in enumerate(known_embeddings):
            similarity = self.compare_embeddings(query_embedding, known_embedding)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match_idx = idx
        
        # Check if best match exceeds threshold
        if best_similarity >= self.threshold:
            if user_ids:
                return user_ids[best_match_idx], best_similarity
            return best_match_idx, best_similarity
        
        return None, best_similarity
    
    def is_match(self, embedding1: np.ndarray, embedding2: np.ndarray) -> bool:
        """Check if two embeddings match.
        
        Args:
            embedding1: First face embedding
            embedding2: Second face embedding
            
        Returns:
            True if embeddings match, False otherwise
        """
        similarity = self.compare_embeddings(embedding1, embedding2)
        return similarity >= self.threshold
    
    def get_all_similarities(self, query_embedding: np.ndarray,
                           known_embeddings: List[np.ndarray]) -> List[float]:
        """Get similarity scores for all known embeddings.
        
        Args:
            query_embedding: Embedding to compare
            known_embeddings: List of known face embeddings
            
        Returns:
            List of similarity scores
        """
        similarities = []
        for known_embedding in known_embeddings:
            similarity = self.compare_embeddings(query_embedding, known_embedding)
            similarities.append(similarity)
        
        return similarities
