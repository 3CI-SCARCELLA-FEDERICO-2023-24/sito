"""Face embedding generation using FaceNet."""
import cv2
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, ZeroPadding2D, Activation, concatenate
from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D, Lambda, Flatten, Dense
from tensorflow.keras import backend as K
import os
import config


class FaceEmbedder:
    """Generates face embeddings using FaceNet architecture."""
    
    def __init__(self):
        """Initialize FaceNet model."""
        self.model = self._create_model()
        self._load_weights()
    
    def _create_model(self):
        """Create FaceNet model architecture.
        
        Returns:
            Keras model for face embedding
        """
        def inception_block_1a(X):
            X_3x3 = Conv2D(96, (1, 1), strides=(1, 1), padding='valid')(X)
            X_3x3 = Activation('relu')(X_3x3)
            X_3x3 = ZeroPadding2D(padding=(1, 1))(X_3x3)
            X_3x3 = Conv2D(128, (3, 3), strides=(1, 1), padding='valid')(X_3x3)
            X_3x3 = Activation('relu')(X_3x3)
            
            X_5x5 = Conv2D(16, (1, 1), strides=(1, 1), padding='valid')(X)
            X_5x5 = Activation('relu')(X_5x5)
            X_5x5 = ZeroPadding2D(padding=(2, 2))(X_5x5)
            X_5x5 = Conv2D(32, (5, 5), strides=(1, 1), padding='valid')(X_5x5)
            X_5x5 = Activation('relu')(X_5x5)
            
            X_pool = MaxPooling2D(pool_size=3, strides=2, padding='same')(X)
            X_pool = Conv2D(32, (1, 1), strides=(1, 1), padding='valid')(X_pool)
            X_pool = Activation('relu')(X_pool)
            
            X_1x1 = Conv2D(256, (1, 1), strides=(1, 1), padding='valid')(X)
            X_1x1 = Activation('relu')(X_1x1)
            
            inception = concatenate([X_3x3, X_5x5, X_pool, X_1x1], axis=3)
            
            return inception
        
        # Simplified FaceNet-like architecture
        inp = Input(shape=(160, 160, 3))
        
        # Initial layers
        X = ZeroPadding2D(padding=(3, 3))(inp)
        X = Conv2D(64, (7, 7), strides=(2, 2), padding='valid')(X)
        X = Activation('relu')(X)
        X = ZeroPadding2D(padding=(1, 1))(X)
        X = MaxPooling2D(pool_size=(3, 3), strides=2)(X)
        
        # Normalization
        X = Lambda(lambda x: K.l2_normalize(x, axis=3))(X)
        
        # Conv layers
        X = Conv2D(64, (1, 1), strides=(1, 1), padding='valid')(X)
        X = Activation('relu')(X)
        X = ZeroPadding2D(padding=(1, 1))(X)
        X = Conv2D(192, (3, 3), strides=(1, 1), padding='valid')(X)
        X = Activation('relu')(X)
        
        # Normalization
        X = Lambda(lambda x: K.l2_normalize(x, axis=3))(X)
        X = ZeroPadding2D(padding=(1, 1))(X)
        X = MaxPooling2D(pool_size=3, strides=2)(X)
        
        # Inception blocks
        X = inception_block_1a(X)
        
        # Average pooling
        X = AveragePooling2D(pool_size=(3, 3), strides=(1, 1))(X)
        X = Flatten()(X)
        
        # Fully connected
        X = Dense(128)(X)
        X = Lambda(lambda x: K.l2_normalize(x, axis=1))(X)
        
        model = Model(inputs=inp, outputs=X)
        
        return model
    
    def _load_weights(self):
        """Load pre-trained weights if available.
        
        WARNING: This implementation uses random weights for demonstration.
        Face recognition will NOT work accurately without pre-trained weights.
        See models/README.md for instructions on downloading proper weights.
        """
        import warnings
        warnings.warn(
            "FaceNet model is using random weights. "
            "Face recognition accuracy will be poor. "
            "Download pre-trained weights for production use.",
            UserWarning
        )
    
    def preprocess_face(self, face_img: np.ndarray) -> np.ndarray:
        """Preprocess face image for embedding generation.
        
        Args:
            face_img: Face image
            
        Returns:
            Preprocessed image ready for model input
        """
        # Resize to 160x160 (FaceNet input size)
        face = cv2.resize(face_img, (160, 160))
        
        # Normalize pixel values to [-1, 1]
        face = face.astype('float32')
        mean, std = face.mean(), face.std()
        face = (face - mean) / std
        
        # Expand dimensions for batch
        face = np.expand_dims(face, axis=0)
        
        return face
    
    def generate_embedding(self, face_img: np.ndarray) -> np.ndarray:
        """Generate face embedding.
        
        Args:
            face_img: Face image (BGR format)
            
        Returns:
            Face embedding as numpy array
        """
        # Preprocess
        processed = self.preprocess_face(face_img)
        
        # Generate embedding
        embedding = self.model.predict(processed, verbose=0)
        
        return embedding[0]
    
    def save_embedding(self, embedding: np.ndarray, filepath: str):
        """Save embedding to file.
        
        Args:
            embedding: Face embedding
            filepath: Path to save the embedding
        """
        np.save(filepath, embedding)
    
    def load_embedding(self, filepath: str) -> np.ndarray:
        """Load embedding from file.
        
        Args:
            filepath: Path to embedding file
            
        Returns:
            Face embedding
        """
        return np.load(filepath)
