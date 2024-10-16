import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
from camera import Camera
import marker_detection

class SquatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Squat Analysis")
        self.root.geometry("800x600")  # Set main window size
        
        self.video_label = ttk.Label(self.root)
        self.video_label.grid(row=2, column=0, padx=10, pady=10)  # Camera feed in the top left corner
        self.show_placeholder()

        self.toggle_cam_button = ttk.Button(self.root, text="Toggle Camera", command=self.toggle_camera)
        self.toggle_cam_button.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        self.start_measurement = ttk.Button(self.root, text="Start measurement", command=self.start_measurement)
        self.start_measurement.grid(row=0, column=1, padx=0, pady=0, sticky="w")

        self.Camera_On = False
        self.camera = Camera()

    def show_placeholder(self):
        """Displays a gray placeholder in the video label area before the camera starts."""
        gray_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # 640x480 gray image
        gray_frame[:] = (169, 169, 169)  # Fill with a gray color (RGB 169, 169, 169)
        img = Image.fromarray(gray_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def toggle_camera(self):
        if self.Camera_On == False:
            self.camera.startcam()
            self.Camera_On = True
        else:
            self.camera.releasecam()
            self.Camera_On = False
            self.show_placeholder()  # Reset to gray box when measurement stops

        self.update_cam()  # Start updating the measurements

    def update_cam(self):
        if self.Camera_On:
            frame = self.camera.get_frame()
            if frame is not None:  # Ensure a frame was captured
                # Convert the frame to an image suitable for Tkinter
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv_image)
                imgtk = ImageTk.PhotoImage(image=img)

                # Update the label with the new frame
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

            # Schedule the next frame update (in milliseconds)
            self.root.after(10, self.update_cam)

    def start_measurement(self):
        self.camera.startcam()
        frame = self.camera.get_frame()
        newframe,centerpoints = marker_detection.aruco_detection(frame)
        print(centerpoints)
        cv2.imshow("frame",newframe)
        self.camera.releasecam()
        
    def run(self):
        self.root.mainloop()

