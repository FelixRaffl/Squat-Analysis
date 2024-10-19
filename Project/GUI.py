import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
from camera import Camera
import marker_detection

# Create the root window
root = tk.Tk()
root.title("Squat Analysis")
root.geometry("800x600")  # Set main window size

# Placeholder video label
video_label = ttk.Label(root)
video_label.grid(row=2, column=0, padx=10, pady=10)  # Camera feed in the top left corner

Camera_On = False
camera = Camera()

live_frame = 0
def live_window():
    if Camera_On == False:
        gray_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # 640x480 gray image
        gray_frame[:] = (169, 169, 169)  # Fill with a gray color (RGB 169, 169, 169)
        img = Image.fromarray(gray_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    else: 
        cv_image = cv2.cvtColor(live_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
live_window()


def toggle_camera():
    if not Camera_On:
        camera.startcam()
        Camera_On = True
    else:
        camera.releasecam()
        Camera_On = False

def start_measurement():
    camera.startcam()
    frame = camera.get_frame()
    if frame is not None:
        newframe, centerpoints = marker_detection.aruco_detection(frame)
        newframe2 = marker_detection.calculate_knee_angle(newframe, centerpoints)
        newframe3 = marker_detection.calculate_femur_angle(newframe2, centerpoints)
        cv2.imshow("frame", newframe3)
    camera.releasecam()

# Buttons for toggling the camera and starting measurement
toggle_cam_button = ttk.Button(root, text="Toggle Camera", command=toggle_camera)
toggle_cam_button.grid(row=0, column=0, padx=0, pady=0, sticky="w")

start_measurement_button = ttk.Button(root, text="Start measurement", command=start_measurement)
start_measurement_button.grid(row=0, column=1, padx=0, pady=0, sticky="w")

# Run the main loop
root.mainloop()
