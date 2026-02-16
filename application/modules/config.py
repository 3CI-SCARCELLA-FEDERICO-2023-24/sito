"""
Configuration module for facial recognition application
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FACES_DIR = os.path.join(DATA_DIR, "faces")
DB_PATH = os.path.join(DATA_DIR, "faces.db")

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)

# Camera settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Face detection settings (MediaPipe)
DETECTION_CONFIDENCE = 0.7
MIN_DETECTION_CONFIDENCE = 0.5

# Face recognition settings (DeepFace)
RECOGNITION_MODEL = "Facenet512"  # Options: VGG-Face, Facenet, Facenet512, OpenFace, DeepFace, DeepID, ArcFace, Dlib, SFace
RECOGNITION_BACKEND = "opencv"  # Options: opencv, ssd, dlib, mtcnn, retinaface, mediapipe
DISTANCE_METRIC = "cosine"  # Options: cosine, euclidean, euclidean_l2
RECOGNITION_THRESHOLD = 0.4  # Lower is stricter, higher is more permissive (0.0-1.0)

# Performance settings
ENABLE_GPU = True  # Set to False if no GPU available
PROCESS_EVERY_N_FRAMES = 2  # Process every Nth frame for better performance
MAX_FRAME_BUFFER = 10

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
VIDEO_DISPLAY_WIDTH = 640
VIDEO_DISPLAY_HEIGHT = 480

# Database settings
DEFAULT_UNKNOWN_NAME = "Sconosciuto"
DEFAULT_UNKNOWN_SURNAME = ""

# Face image settings
FACE_IMAGE_SIZE = (160, 160)
FACE_IMAGE_FORMAT = "jpg"
FACE_IMAGE_QUALITY = 95
