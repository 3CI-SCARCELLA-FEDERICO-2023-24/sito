#!/usr/bin/env python
"""
Installation verification script for the Facial Recognition Application.

This script checks if all required dependencies are installed and properly configured.
Run this script after installing requirements.txt to verify your setup.
"""

import sys
import importlib.util


def check_module(module_name, package_name=None):
    """Check if a Python module can be imported.
    
    Args:
        module_name: Name of the module to import
        package_name: Package name (if different from module)
    
    Returns:
        True if module is available, False otherwise
    """
    spec = importlib.util.find_spec(module_name)
    display_name = package_name or module_name
    
    if spec is not None:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name:20} version {version}")
            return True
        except ImportError as e:
            print(f"✗ {display_name:20} import error: {e}")
            return False
    else:
        print(f"✗ {display_name:20} not found")
        return False


def main():
    """Run installation verification."""
    print("="*60)
    print("Facial Recognition Application - Installation Verification")
    print("="*60)
    print()
    
    print(f"Python version: {sys.version}")
    print()
    
    print("Checking required dependencies...")
    print("-"*60)
    
    dependencies = [
        ('PyQt6', 'PyQt6'),
        ('cv2', 'opencv-python'),
        ('mediapipe', 'mediapipe'),
        ('tensorflow', 'tensorflow'),
        ('PIL', 'Pillow'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
    ]
    
    all_installed = True
    for module, package in dependencies:
        if not check_module(module, package):
            all_installed = False
    
    print("-"*60)
    print()
    
    if all_installed:
        print("✓ All dependencies installed successfully!")
        print()
        print("Testing application modules...")
        print("-"*60)
        
        try:
            import config
            print("✓ config module loaded")
            
            from database import Database
            print("✓ Database module loaded")
            
            from face_recognition import FaceDetector, FaceEmbedder, FaceMatcher
            print("✓ Face recognition modules loaded")
            
            print("-"*60)
            print()
            print("✓ Installation verified successfully!")
            print()
            print("You can now run the application with:")
            print("    python main.py")
            
        except Exception as e:
            print(f"✗ Error loading application modules: {e}")
            return 1
    else:
        print("✗ Some dependencies are missing!")
        print()
        print("Please install missing dependencies with:")
        print("    pip install -r requirements.txt")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
