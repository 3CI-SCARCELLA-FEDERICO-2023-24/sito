"""
Camera module for webcam capture and video processing
"""
import cv2
import numpy as np
from typing import Optional, Tuple
from PyQt6.QtCore import QThread, pyqtSignal, QMutex
from modules import config


class CameraThread(QThread):
    """Thread for capturing video from webcam"""
    
    # Signals
    frame_ready = pyqtSignal(np.ndarray)  # Emits captured frame
    error_occurred = pyqtSignal(str)  # Emits error message
    fps_updated = pyqtSignal(float)  # Emits current FPS
    
    def __init__(self, camera_index: int = config.CAMERA_INDEX):
        """
        Initialize camera thread
        
        Args:
            camera_index: Index of the camera to use
        """
        super().__init__()
        self.camera_index = camera_index
        self.capture = None
        self.running = False
        self.mutex = QMutex()
        self.frame_count = 0
        self.process_frame_number = 0
    
    def run(self):
        """Main thread loop for capturing frames"""
        self.running = True
        
        # Initialize camera
        self.capture = cv2.VideoCapture(self.camera_index)
        
        if not self.capture.isOpened():
            self.error_occurred.emit("Failed to open camera")
            return
        
        # Set camera properties
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
        
        # FPS calculation variables
        fps_counter = 0
        fps_timer = cv2.getTickCount()
        
        while self.running:
            ret, frame = self.capture.read()
            
            if not ret:
                self.error_occurred.emit("Failed to read frame from camera")
                break
            
            self.mutex.lock()
            self.frame_count += 1
            current_frame = self.frame_count
            self.mutex.unlock()
            
            # Emit frame for processing
            self.frame_ready.emit(frame.copy())
            
            # Calculate FPS
            fps_counter += 1
            if fps_counter >= 30:
                current_time = cv2.getTickCount()
                time_elapsed = (current_time - fps_timer) / cv2.getTickFrequency()
                fps = fps_counter / time_elapsed
                self.fps_updated.emit(fps)
                fps_counter = 0
                fps_timer = current_time
        
        # Cleanup
        if self.capture:
            self.capture.release()
    
    def stop(self):
        """Stop the camera thread"""
        self.running = False
        self.wait()
    
    def should_process_frame(self) -> bool:
        """
        Check if current frame should be processed
        Used for performance optimization
        
        Returns:
            True if frame should be processed
        """
        self.mutex.lock()
        should_process = (self.frame_count % config.PROCESS_EVERY_N_FRAMES == 0)
        self.mutex.unlock()
        return should_process
    
    def get_frame_count(self) -> int:
        """Get current frame count"""
        self.mutex.lock()
        count = self.frame_count
        self.mutex.unlock()
        return count


class Camera:
    """Wrapper class for camera operations"""
    
    def __init__(self, camera_index: int = config.CAMERA_INDEX):
        """
        Initialize camera
        
        Args:
            camera_index: Index of the camera to use
        """
        self.camera_index = camera_index
        self.thread = None
    
    def start(self) -> CameraThread:
        """
        Start camera capture
        
        Returns:
            CameraThread instance
        """
        if self.thread and self.thread.isRunning():
            self.stop()
        
        self.thread = CameraThread(self.camera_index)
        self.thread.start()
        return self.thread
    
    def stop(self):
        """Stop camera capture"""
        if self.thread:
            self.thread.stop()
            self.thread = None
    
    @staticmethod
    def is_camera_available(camera_index: int = config.CAMERA_INDEX) -> bool:
        """
        Check if camera is available
        
        Args:
            camera_index: Index of the camera to check
            
        Returns:
            True if camera is available
        """
        cap = cv2.VideoCapture(camera_index)
        available = cap.isOpened()
        cap.release()
        return available
    
    @staticmethod
    def save_frame_as_image(frame: np.ndarray, output_path: str, 
                          resize: Optional[Tuple[int, int]] = None) -> bool:
        """
        Save a frame as an image file
        
        Args:
            frame: Frame to save
            output_path: Path to save the image
            resize: Optional tuple (width, height) to resize the image
            
        Returns:
            True if save successful
        """
        try:
            if resize:
                frame = cv2.resize(frame, resize)
            
            # Convert BGR to RGB for saving
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            success = cv2.imwrite(output_path, frame_rgb, 
                                [cv2.IMWRITE_JPEG_QUALITY, config.FACE_IMAGE_QUALITY])
            return success
        except Exception as e:
            print(f"Error saving frame: {e}")
            return False
    
    @staticmethod
    def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Resize frame to specified dimensions
        
        Args:
            frame: Frame to resize
            width: Target width
            height: Target height
            
        Returns:
            Resized frame
        """
        return cv2.resize(frame, (width, height))
    
    @staticmethod
    def draw_rectangle(frame: np.ndarray, x: int, y: int, w: int, h: int, 
                      color: Tuple[int, int, int] = (0, 255, 0), 
                      thickness: int = 2) -> np.ndarray:
        """
        Draw rectangle on frame
        
        Args:
            frame: Frame to draw on
            x, y: Top-left corner coordinates
            w, h: Width and height
            color: BGR color tuple
            thickness: Line thickness
            
        Returns:
            Frame with rectangle drawn
        """
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        return frame
    
    @staticmethod
    def draw_text(frame: np.ndarray, text: str, x: int, y: int, 
                 color: Tuple[int, int, int] = (0, 255, 0),
                 font_scale: float = 0.7, thickness: int = 2) -> np.ndarray:
        """
        Draw text on frame
        
        Args:
            frame: Frame to draw on
            text: Text to draw
            x, y: Bottom-left corner coordinates
            color: BGR color tuple
            font_scale: Font scale
            thickness: Text thickness
            
        Returns:
            Frame with text drawn
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Draw background rectangle for better readability
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        cv2.rectangle(frame, (x - 5, y - text_size[1] - 5), 
                     (x + text_size[0] + 5, y + 5), (0, 0, 0), -1)
        
        # Draw text
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        return frame
