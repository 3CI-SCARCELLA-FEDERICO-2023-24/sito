# Quick Start Guide

## Prerequisites

- Windows 10 or later
- Python 3.10 or later
- Webcam
- 4GB RAM minimum

## Installation Steps

### 1. Install Python

Download and install Python from [python.org](https://www.python.org/downloads/)

Make sure to check "Add Python to PATH" during installation.

### 2. Create Virtual Environment

Open Command Prompt or PowerShell and navigate to the project directory:

```bash
cd path\to\sito
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
# On Windows Command Prompt
venv\Scripts\activate.bat

# On Windows PowerShell
venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt6 (GUI framework)
- opencv-python (Camera handling)
- mediapipe (Face detection)
- tensorflow (Face recognition AI)
- Pillow (Image processing)
- numpy (Numerical operations)
- scipy (Scientific computing)

### 4. Verify Installation

Run the verification script:

```bash
python verify_installation.py
```

This will check if all dependencies are properly installed.

### 5. Run the Application

```bash
python main.py
```

## First Run

1. The application will open with three panels
2. Allow camera access if prompted by Windows
3. Position yourself in front of the camera
4. When your face is detected, a registration dialog will appear
5. Enter your name and surname
6. Click "Salva" to register

## Using the Application

### Registering Users

**Automatic Registration:**
- Stand in front of the camera
- When an unknown face is detected, a dialog appears
- Fill in Name and Surname (required)
- Optionally upload a profile photo
- Click "Salva" to save

**Manual Registration:**
- Click "Gestione" button
- Click "Aggiungi Nuovo Utente"
- Fill in the form
- Upload a photo
- Click "Salva"

### Managing Users

Click the "Gestione" button to:
- View all registered users
- Add new users manually
- Delete existing users

### Recognition

Once users are registered:
- The system automatically recognizes faces
- User name appears above detected face
- Recognition info shows in the center panel

## Troubleshooting

### Camera Not Working

1. Check if camera is connected
2. Close other applications using the camera
3. Try changing `CAMERA_INDEX` in `config.py`:
   ```python
   CAMERA_INDEX = 1  # Try 0, 1, 2
   ```

### Poor Recognition Accuracy

The default implementation uses a simplified model. For better accuracy:

1. Download pre-trained FaceNet weights (see `models/README.md`)
2. Update `embedder.py` to load the weights
3. Adjust `SIMILARITY_THRESHOLD` in `config.py`:
   ```python
   SIMILARITY_THRESHOLD = 0.7  # Higher = more strict
   ```

### Slow Performance

1. Reduce camera resolution in `config.py`:
   ```python
   CAMERA_WIDTH = 320
   CAMERA_HEIGHT = 240
   ```

2. Increase detection cooldown in `main_window.py`:
   ```python
   self.detection_cooldown = 5.0  # seconds
   ```

### Application Won't Start

1. Make sure virtual environment is activated
2. Reinstall dependencies:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
3. Check Python version:
   ```bash
   python --version  # Should be 3.10+
   ```

## Configuration

Edit `config.py` to customize:

- Camera settings (resolution, FPS)
- Detection confidence threshold
- Recognition similarity threshold
- Window size
- Default user names

## Data Storage

All data is stored locally in the `data/` directory:
- `data/users/` - User profile photos
- `data/embeddings/` - Face embeddings
- `data/users.db` - SQLite database

## Privacy

- All data is stored locally
- No internet connection required (after installation)
- Data can be deleted through the management panel

## Support

For issues or questions:
1. Check this guide
2. Review `README.md`
3. Open an issue on GitHub
