# Developer Documentation

## Architecture Overview

### System Components

The facial recognition application follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                     Main Window (UI)                     │
│  - Camera preview                                        │
│  - Recognition display                                   │
│  - Control panel                                         │
└─────────────┬───────────────────────────────────────────┘
              │
              ├──────────────────────────────────────┐
              ↓                                      ↓
    ┌──────────────────┐                  ┌──────────────────┐
    │  Face Recognition │                  │    Database      │
    │  ----------------│                  │    --------      │
    │  • Detector      │                  │  • SQLite CRUD   │
    │  • Embedder      │                  │  • User mgmt     │
    │  • Matcher       │                  │  • File mgmt     │
    └──────────────────┘                  └──────────────────┘
              ↑
              │
    ┌──────────────────┐
    │  Camera Widget   │
    │  --------------  │
    │  • Live feed     │
    │  • Frame capture │
    └──────────────────┘
```

### Module Descriptions

#### 1. Database Module (`database/`)

**Purpose**: Handle all data persistence operations

**Key Components**:
- `Database` class: Manages SQLite operations
- User CRUD operations
- File path management
- Duplicate prevention

**Database Schema**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    foto_path TEXT,
    embedding_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(nome, cognome)
);
```

#### 2. Face Recognition Module (`face_recognition/`)

**Purpose**: Core AI/ML functionality for face detection and recognition

**Components**:

##### detector.py
- Uses MediaPipe Face Detection
- Real-time face detection
- Face extraction with margins
- Bounding box visualization

##### embedder.py
- FaceNet-based architecture
- Generates 128-dimensional embeddings
- Face preprocessing (resize, normalize)
- Embedding persistence

##### matcher.py
- Cosine similarity comparison
- Threshold-based matching
- Best match selection

#### 3. UI Module (`ui/`)

**Purpose**: User interface components

**Components**:

##### main_window.py
- Application main window
- Orchestrates all components
- Face detection loop
- User interaction handling

##### camera_widget.py
- Live camera feed display
- Frame capture
- Face overlay rendering

##### registration_dialog.py
- User registration form
- Photo upload/capture
- Input validation

##### management_dialog.py
- User list display
- Add/delete operations
- User editing

### Data Flow

#### Registration Flow

```
1. Camera detects unknown face
   ↓
2. Extract face region
   ↓
3. Generate embedding
   ↓
4. Show registration dialog
   ↓
5. User enters information
   ↓
6. Save photo to data/users/
   ↓
7. Save embedding to data/embeddings/
   ↓
8. Insert record to database
   ↓
9. Reload known embeddings
```

#### Recognition Flow

```
1. Camera captures frame
   ↓
2. Detect faces in frame
   ↓
3. Extract face region
   ↓
4. Generate embedding
   ↓
5. Compare with known embeddings
   ↓
6. Find best match (if similarity > threshold)
   ↓
7. Display user information
```

## Configuration

### config.py

Central configuration file for all settings:

```python
# Camera settings
CAMERA_INDEX = 0          # Camera device index
CAMERA_WIDTH = 640        # Frame width
CAMERA_HEIGHT = 480       # Frame height
CAMERA_FPS = 30          # Frames per second

# Detection settings
MIN_DETECTION_CONFIDENCE = 0.7  # MediaPipe confidence threshold
MIN_TRACKING_CONFIDENCE = 0.5   # Tracking threshold

# Recognition settings
SIMILARITY_THRESHOLD = 0.6      # Face matching threshold
EMBEDDING_SIZE = 128            # FaceNet embedding dimensions

# UI settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Sistema di Riconoscimento Facciale"
```

## Extending the Application

### Adding New Features

#### 1. Custom Face Recognition Model

To integrate a different model (e.g., ArcFace, VGGFace):

```python
# face_recognition/embedder.py

class FaceEmbedder:
    def _create_model(self):
        # Replace with your model architecture
        from your_model import create_model
        return create_model()
    
    def _load_weights(self):
        # Load your pre-trained weights
        self.model.load_weights('path/to/weights.h5')
```

#### 2. Additional User Attributes

Update database schema:

```python
# database/database.py

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT,              # New field
        department TEXT,         # New field
        foto_path TEXT,
        embedding_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(nome, cognome)
    )
''')
```

#### 3. Multi-Face Support

Modify detection loop to process multiple faces:

```python
# ui/main_window.py

def _process_face_detection(self):
    faces = self.detector.detect_faces(frame)
    
    for face_bbox in faces:
        face_img = self.detector.extract_face(frame, face_bbox)
        embedding = self.embedder.generate_embedding(face_img)
        
        # Match and display each face
        user_id, similarity = self.matcher.find_match(...)
        # Handle result
```

### Performance Optimization

#### 1. Embedding Cache

Cache embeddings in memory to reduce file I/O:

```python
class EmbeddingCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, user_id):
        if user_id not in self.cache:
            self.cache[user_id] = load_from_disk(user_id)
        return self.cache[user_id]
```

#### 2. Async Face Detection

Use threading for face detection:

```python
from threading import Thread
from queue import Queue

class AsyncDetector:
    def __init__(self, detector):
        self.detector = detector
        self.queue = Queue(maxsize=2)
        self.thread = Thread(target=self._process)
        self.running = True
        self.thread.start()
    
    def _process(self):
        while self.running:
            frame = self.queue.get()
            faces = self.detector.detect_faces(frame)
            # Emit results
```

## Testing

### Unit Tests

Create test files for each module:

```python
# tests/test_database.py

import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
    
    def test_add_user(self):
        user_id = self.db.add_user('John', 'Doe')
        self.assertIsNotNone(user_id)
    
    def test_duplicate_prevention(self):
        self.db.add_user('John', 'Doe')
        duplicate_id = self.db.add_user('John', 'Doe')
        self.assertIsNone(duplicate_id)
```

### Integration Tests

Test component interactions:

```python
# tests/test_recognition.py

def test_face_recognition_pipeline():
    # Setup
    detector = FaceDetector()
    embedder = FaceEmbedder()
    matcher = FaceMatcher()
    
    # Load test image
    frame = cv2.imread('test_face.jpg')
    
    # Detect
    faces = detector.detect_faces(frame)
    assert len(faces) > 0
    
    # Extract and embed
    face_img = detector.extract_face(frame, faces[0])
    embedding = embedder.generate_embedding(face_img)
    assert embedding.shape == (128,)
```

## Security Considerations

### 1. Input Validation

Always validate user inputs:

```python
def validate_name(name):
    if not name or len(name) > 100:
        raise ValueError("Invalid name")
    
    # Allow only letters, spaces, hyphens
    if not re.match(r'^[a-zA-Z\s-]+$', name):
        raise ValueError("Name contains invalid characters")
```

### 2. File Path Safety

Prevent path traversal attacks:

```python
import os

def safe_file_path(filename):
    # Remove any path components
    filename = os.path.basename(filename)
    
    # Sanitize filename
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Ensure it's within allowed directory
    full_path = os.path.join(USERS_DIR, filename)
    return full_path
```

### 3. Database Queries

Use parameterized queries to prevent SQL injection:

```python
# Good - parameterized
cursor.execute('SELECT * FROM users WHERE nome = ?', (nome,))

# Bad - string interpolation
cursor.execute(f'SELECT * FROM users WHERE nome = {nome}')  # Never do this!
```

## Troubleshooting

### Common Issues

#### 1. MediaPipe Initialization Errors

**Problem**: `RuntimeError: Failed to initialize MediaPipe`

**Solution**: 
- Update graphics drivers
- Try different MediaPipe model selection
- Reduce detection confidence threshold

#### 2. Memory Leaks

**Problem**: Application memory usage increases over time

**Solution**:
- Ensure proper cleanup in camera widget
- Release OpenCV resources
- Clear embedding cache periodically

#### 3. Slow Performance

**Problem**: Low FPS or laggy interface

**Solution**:
- Reduce camera resolution
- Increase detection interval
- Use threading for face detection
- Optimize embedding generation

## Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings to all public methods
- Keep functions focused and small

### Pull Request Process

1. Create a feature branch
2. Implement changes with tests
3. Update documentation
4. Submit PR with clear description
5. Address review feedback

## License

Educational project - see LICENSE file for details.
