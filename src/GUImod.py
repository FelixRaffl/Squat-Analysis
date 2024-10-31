import tkinter as tk
from camera import CameraModule
from measurement import MeasurementModule
from PIL import Image, ImageTk
import cv2

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera vs Measurement")
        self.root.geometry("640x620")  # Adjusted to make space for elements in measurement mode

        self.camera_module = CameraModule()
        self.measurement_module = MeasurementModule()

        self.camera_mode = False
        self.measurement_mode = False
        self.squat_count = 0  # Initialize squat count

        # Tkinter label to show the frames
        self.label = tk.Label(self.root)
        self.label.pack()

        # Squat count label (initially hidden)
        self.squat_count_label = tk.Label(self.root, text="Squat Count: 0", font=("Helvetica", 14))
        self.squat_count_label.pack_forget()  # Hide initially

        # Checkbox for enabling/disabling squat sound (initially hidden)
        self.squatsound = tk.BooleanVar(value=True)  # Initialize with True for sound on by default
        self.squatsound_checkbox = tk.Checkbutton(self.root, text="Toggle Squat Sound", variable=self.squatsound)
        self.squatsound_checkbox.pack_forget()  # Hide initially

        # Reset button (initially hidden)
        self.reset_button = tk.Button(self.root, text="Reset Squat Count", command=self.reset_squat_count)
        self.reset_button.pack_forget()  # Hide initially

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
            if self.measurement_mode:
                self.toggle_measurement()  # Stop measurement if active
            self.camera_module.start_camera()
            self.camera_mode = True

        self.update_button_colors()

    def toggle_measurement(self):
        if self.measurement_mode:
            self.measurement_mode = False
            self.camera_module.stop_camera()  # Stop the camera when measurement mode is turned off
            self.squat_count_label.pack_forget()  # Hide squat count label
            self.squatsound_checkbox.pack_forget()  # Hide sound checkbox
            self.reset_button.pack_forget()  # Hide reset button
        else:
            if self.camera_mode:
                self.toggle_camera()  # Stop camera if active
            self.measurement_mode = True
            self.camera_module.start_camera()  # Start the camera if not already running
            self.squat_count_label.pack()  # Show squat count label
            self.squatsound_checkbox.pack(pady=5)  # Show sound checkbox
            self.reset_button.pack(pady=5)  # Show reset button

        self.update_button_colors()

    def reset_squat_count(self):
        self.measurement_module.squat_count=0
        self.squat_count_label.config(text=f"Squat Count: {self.squat_count}")

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
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        elif self.measurement_mode:
            frame, femur_angle, knee_angle = self.measurement_module.create_measurement_frame(self.camera_module.get_frame())
            self.squat_count = self.measurement_module.squat_counter(femur_angle, 0, 25, self.squatsound.get())
            self.squat_count_label.config(text=f"Squat Count: {self.squat_count}")  # Update squat count label

            if frame is not None:
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        else:
            placeholder = self.create_placeholder_frame(640, 480)
            self.label.config(image=placeholder)
            self.label.image = placeholder

        self.root.after(10, self.update_frame)

    def create_placeholder_frame(self, width, height):
        img = Image.new("RGB", (width, height), color="grey")
        return ImageTk.PhotoImage(img)
