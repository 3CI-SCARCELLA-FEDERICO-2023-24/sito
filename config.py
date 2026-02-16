"""Configuration settings for the facial recognition application."""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_DIR = os.path.join(DATA_DIR, 'users')
EMBEDDINGS_DIR = os.path.join(DATA_DIR, 'embeddings')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATABASE_PATH = os.path.join(DATA_DIR, 'users.db')

# Create directories if they don't exist
for directory in [DATA_DIR, USERS_DIR, EMBEDDINGS_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Face detection settings (MediaPipe)
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5

# Face recognition settings
SIMILARITY_THRESHOLD = 0.6  # Lower = more strict matching
EMBEDDING_SIZE = 512

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Sistema di Riconoscimento Facciale"

# Default values
DEFAULT_USER_NAME = "Sconosciuto"
DEFAULT_USER_SURNAME = ""

# FaceNet model URL (will be downloaded if not present)
FACENET_MODEL_URL = "https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5"
FACENET_MODEL_PATH = os.path.join(MODELS_DIR, "facenet_weights.h5")
