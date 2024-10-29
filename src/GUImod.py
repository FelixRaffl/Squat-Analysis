import tkinter as tk
from camera import CameraModule
from measurement import MeasurementModule
from PIL import Image, ImageTk
import cv2

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera vs Measurement")
        self.root.geometry("640x520")

        self.camera_module = CameraModule()
        self.measurement_module = MeasurementModule()

        self.camera_mode = False
        self.measurement_mode = False

        # Tkinter label to show the frames
        self.label = tk.Label(self.root)
        self.label.pack()

        # Buttons
        self.camera_button = tk.Button(self.root, text="Toggle Camera", command=self.toggle_camera)
        self.camera_button.pack(side=tk.LEFT, padx=10)

        self.measurement_button = tk.Button(self.root, text="Toggle Measurement", command=self.toggle_measurement)
        self.measurement_button.pack(side=tk.LEFT, padx=10)

        # Set initial button colors
        self.update_button_colors()

        # Continuously update the frame display
        self.update_frame()

    def toggle_camera(self):
        if self.camera_mode:
            self.camera_module.stop_camera()
            self.camera_mode = False
        else:
            # If measurement mode is active, stop it
            if self.measurement_mode:
                self.toggle_measurement()  # This will stop the measurement and turn off the camera

            self.camera_module.start_camera()
            self.camera_mode = True
        
        # Update button colors
        self.update_button_colors()

    def toggle_measurement(self):
        if self.measurement_mode:
            self.measurement_mode = False
            self.camera_module.stop_camera()  # Stop the camera when measurement mode is turned off
        else:
            # If camera mode is active, stop it
            if self.camera_mode:
                self.toggle_camera()  # This will stop the camera and turn off measurement

            self.measurement_mode = True
            self.camera_module.start_camera()  # Start the camera if it's not already running

        # Update button colors
        self.update_button_colors()

    def update_button_colors(self):
        if self.camera_mode:
            self.camera_button.config(bg='red')
            self.measurement_button.config(bg='grey')
        elif self.measurement_mode:
            self.camera_button.config(bg='grey')
            self.measurement_button.config(bg='red')
        else:
            self.camera_button.config(bg='grey')
            self.measurement_button.config(bg='grey')

    def update_frame(self):
        if self.camera_mode:
            frame = self.camera_module.get_frame()
            if frame is not None:
                # Convert the BGR frame to RGB for display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert NumPy array to ImageTk.PhotoImage for Tkinter
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        elif self.measurement_mode:
            frame,femurangle,kneeangle = self.measurement_module.create_measurement_frame(self.camera_module.get_frame())
            squat_count = self.measurement_module.squat_counter(femurangle,0,50)
            print(squat_count)
            if frame is not None:
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        else:
            # Grey placeholder when neither mode is active
            placeholder = self.create_placeholder_frame(640, 480)
            self.label.config(image=placeholder)
            self.label.image = placeholder

        # Continue updating
        self.root.after(10, self.update_frame)

    def create_placeholder_frame(self, width, height):
        # Create a grey image to use as a placeholder
        img = Image.new("RGB", (width, height), color="grey")
        return ImageTk.PhotoImage(img)
