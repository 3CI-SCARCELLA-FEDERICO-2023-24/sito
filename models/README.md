# Models Directory

This directory stores pre-trained models for face recognition.

## FaceNet Model

The application uses a FaceNet-based model for generating face embeddings. 

### Model Download

Due to file size constraints, the model weights are not included in the repository. The application will function with a simplified architecture initialized with random weights for demonstration purposes.

For production use, you should:

1. Download pre-trained FaceNet weights from:
   - https://github.com/serengil/deepface_models/releases/download/v1.0/facenet_weights.h5

2. Place the downloaded file in this directory as `facenet_weights.h5`

3. Update the `embedder.py` to load these weights in the `_load_weights()` method

## Alternative Models

You can also use other face recognition models such as:
- VGGFace
- ArcFace
- DeepFace

Modify the `FaceEmbedder` class to integrate alternative models as needed.
