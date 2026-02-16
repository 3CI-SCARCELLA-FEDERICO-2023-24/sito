"""
Configurazione globale per l'applicazione di riconoscimento facciale.
"""

import os

# Percorsi di base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
FACES_DIR = os.path.join(DATA_DIR, "faces")

# Database
DATABASE_PATH = os.path.join(DATABASE_DIR, "face_recognition.db")

# Impostazioni Camera
CAMERA_INDEX = 0  # Default camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Impostazioni Riconoscimento Facciale
FACE_DETECTION_CONFIDENCE = 0.5  # MediaPipe detection confidence
FACE_RECOGNITION_THRESHOLD = 0.6  # Soglia per il riconoscimento (distanza euclidea)
MIN_FACE_SIZE = 20  # Dimensione minima del volto in pixel

# Impostazioni FaceNet
FACENET_MODEL_PATH = os.path.join(MODELS_DIR, "facenet", "facenet_keras.h5")
FACENET_INPUT_SIZE = (160, 160)  # Dimensione input per FaceNet
EMBEDDING_SIZE = 128  # Dimensione degli embeddings

# Impostazioni MediaPipe
MEDIAPIPE_MAX_FACES = 5  # Numero massimo di volti da rilevare
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = 0.5

# Impostazioni UI
WINDOW_TITLE = "Sistema di Riconoscimento Facciale"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 480

# Colori per l'UI (RGB)
COLOR_RECOGNIZED = (0, 255, 0)  # Verde per volti riconosciuti
COLOR_UNKNOWN = (255, 0, 0)     # Rosso per volti sconosciuti
COLOR_BOX = (255, 255, 0)       # Giallo per il riquadro

# Impostazioni Database
MAX_DUPLICATE_DISTANCE = 0.4  # Soglia per considerare un volto come duplicato

# Creazione delle directory se non esistono
for directory in [DATABASE_DIR, MODELS_DIR, DATA_DIR, FACES_DIR]:
    os.makedirs(directory, exist_ok=True)
