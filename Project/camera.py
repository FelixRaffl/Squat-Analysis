import cv2

class Camera:
    def __init__(self):
        self.cap = None

    def startcam(self):
        self.cap = cv2.VideoCapture(0)  # Initialize the camera (0 is usually the default camera)

    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def releasecam(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
