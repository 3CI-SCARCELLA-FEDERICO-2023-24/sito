"""Face recognition module initialization."""
from .detector import FaceDetector
from .embedder import FaceEmbedder
from .matcher import FaceMatcher

__all__ = ['FaceDetector', 'FaceEmbedder', 'FaceMatcher']
