import cv2
import numpy as np
from PIL import Image, ImageTk

class CameraModule:
    def __init__(self):
        self.cap = None

    def start_camera(self):
        if not self.cap:
            self.cap = cv2.VideoCapture(0)  # Open the default camera

    def get_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Return the raw NumPy array (BGR format as OpenCV captures)
                return frame  # Directly return NumPy array
            else:
                print("Warning: Failed to capture frame")
        return None

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
