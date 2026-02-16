"""
Script di test per verificare l'installazione e le dipendenze.
"""

import sys


def test_python_version():
    """Verifica versione Python."""
    print("=" * 50)
    print("Test Versione Python")
    print("=" * 50)
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Versione Python compatibile")
        return True
    else:
        print("❌ Richiesto Python 3.10 o superiore")
        return False


def test_dependencies():
    """Verifica dipendenze principali."""
    print("\n" + "=" * 50)
    print("Test Dipendenze")
    print("=" * 50)
    
    all_ok = True
    
    # Test OpenCV
    try:
        import cv2
        print(f"✅ OpenCV installato - versione {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV non trovato")
        all_ok = False
    
    # Test MediaPipe
    try:
        import mediapipe
        print(f"✅ MediaPipe installato - versione {mediapipe.__version__}")
    except ImportError:
        print("❌ MediaPipe non trovato")
        all_ok = False
    
    # Test PyTorch
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        cuda_info = f" (CUDA: {torch.cuda.get_device_name(0)})" if cuda_available else " (CPU only)"
        print(f"✅ PyTorch installato - versione {torch.__version__}{cuda_info}")
    except ImportError:
        print("❌ PyTorch non trovato")
        all_ok = False
    
    # Test PyQt6
    try:
        from PyQt6 import QtCore
        print(f"✅ PyQt6 installato - versione {QtCore.PYQT_VERSION_STR}")
    except ImportError:
        print("❌ PyQt6 non trovato")
        all_ok = False
    
    # Test NumPy
    try:
        import numpy as np
        print(f"✅ NumPy installato - versione {np.__version__}")
    except ImportError:
        print("❌ NumPy non trovato")
        all_ok = False
    
    # Test Pillow
    try:
        import PIL
        print(f"✅ Pillow installato - versione {PIL.__version__}")
    except ImportError:
        print("❌ Pillow non trovato")
        all_ok = False
    
    return all_ok


def test_modules():
    """Verifica moduli dell'applicazione."""
    print("\n" + "=" * 50)
    print("Test Moduli Applicazione")
    print("=" * 50)
    
    all_ok = True
    
    # Test config
    try:
        import config
        print("✅ config.py caricato correttamente")
    except ImportError as e:
        print(f"❌ Errore caricamento config: {e}")
        all_ok = False
    
    # Test database
    try:
        from database.db_manager import DatabaseManager
        print("✅ database.db_manager importato correttamente")
    except ImportError as e:
        print(f"❌ Errore import database: {e}")
        all_ok = False
    
    # Test face_recognition
    try:
        from face_recognition.face_detector import FaceDetector
        from face_recognition.face_encoder import FaceEncoder
        from face_recognition.face_matcher import FaceMatcher
        print("✅ face_recognition modules importati correttamente")
    except ImportError as e:
        print(f"❌ Errore import face_recognition: {e}")
        all_ok = False
    
    # Test ui
    try:
        from ui.camera_preview import CameraPreview
        from ui.management_panel import ManagementPanel
        from ui.main_window import MainWindow
        print("✅ ui modules importati correttamente")
    except ImportError as e:
        print(f"❌ Errore import ui: {e}")
        all_ok = False
    
    return all_ok


def test_camera():
    """Verifica disponibilità camera."""
    print("\n" + "=" * 50)
    print("Test Camera")
    print("=" * 50)
    
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        
        if camera.isOpened():
            ret, frame = camera.read()
            if ret and frame is not None:
                print(f"✅ Camera funzionante - risoluzione: {frame.shape}")
                camera.release()
                return True
            else:
                print("❌ Camera aperta ma impossibile leggere frame")
                camera.release()
                return False
        else:
            print("❌ Impossibile aprire la camera")
            return False
    except Exception as e:
        print(f"❌ Errore test camera: {e}")
        return False


def test_database():
    """Verifica funzionamento database."""
    print("\n" + "=" * 50)
    print("Test Database")
    print("=" * 50)
    
    try:
        from database.db_manager import DatabaseManager
        import numpy as np
        
        # Crea database di test
        db = DatabaseManager()
        print("✅ Database inizializzato")
        
        # Test operazioni base
        users = db.get_all_users()
        print(f"✅ Utenti nel database: {len(users)}")
        
        db.close()
        print("✅ Database chiuso correttamente")
        
        return True
    except Exception as e:
        print(f"❌ Errore test database: {e}")
        return False


def main():
    """Funzione principale."""
    print("\n" + "=" * 50)
    print("TEST SISTEMA DI RICONOSCIMENTO FACCIALE")
    print("=" * 50 + "\n")
    
    results = []
    
    # Test versione Python
    results.append(("Python Version", test_python_version()))
    
    # Test dipendenze
    results.append(("Dependencies", test_dependencies()))
    
    # Test moduli
    results.append(("Application Modules", test_modules()))
    
    # Test camera (opzionale)
    print("\n⚠️  Test camera opzionale (premi Ctrl+C per saltare)")
    try:
        results.append(("Camera", test_camera()))
    except KeyboardInterrupt:
        print("\n⏭️  Test camera saltato")
        results.append(("Camera", None))
    
    # Test database
    results.append(("Database", test_database()))
    
    # Riepilogo
    print("\n" + "=" * 50)
    print("RIEPILOGO TEST")
    print("=" * 50)
    
    for name, result in results:
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⏭️  SKIP"
        
        print(f"{name:.<30} {status}")
    
    # Conclusione
    print("\n" + "=" * 50)
    
    failed = sum(1 for _, result in results if result is False)
    passed = sum(1 for _, result in results if result is True)
    
    if failed == 0:
        print("✅ TUTTI I TEST SUPERATI!")
        print("=" * 50)
        print("\nPuoi avviare l'applicazione con:")
        print("  python main.py")
        return 0
    else:
        print(f"❌ {failed} TEST FALLITI, {passed} SUPERATI")
        print("=" * 50)
        print("\nSegui le istruzioni in SETUP.md per risolvere i problemi.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
