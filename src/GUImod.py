import tkinter as tk
from camera import CameraModule
import measurement
from PIL import Image, ImageTk
import cv2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera vs Measurement")
        self.root.geometry("1600x780")  # Updated to accommodate camera frame + live plot

        self.camera_module = CameraModule()
        self.camera_mode = False
        self.measurement_mode = False
        self.squat_count = 0
        self.femur_angle = 0
        self.knee_angle = 0
        self.frame = 0

        # Tkinter label to show the camera frames
        self.label = tk.Label(self.root)
        self.label.grid(row=1, column=0, rowspan=2, padx=10)

        # Squat count label
        self.squat_count_label = tk.Label(self.root, text="Squat Count: 0", font=("Helvetica", 14))
        self.squat_count_label.grid(row=3, column=4, pady=5)

        # Handlebar height label (new)
        self.handlebar_label = tk.Label(self.root, text="Handlebar Height: N/A", font=("Helvetica", 14))
        self.handlebar_label.grid(row=2, column=4, pady=5)

        # Checkbox for enabling/disabling squat sound
        self.squatsound = tk.BooleanVar(value=True)
        self.squatsound_checkbox = tk.Checkbutton(self.root, text="Toggle Squat Sound", variable=self.squatsound)
        self.squatsound_checkbox.grid(row=4, column=4, pady=5)

        # Reset button for squat count
        self.reset_button = tk.Button(self.root, text="Reset Squat Count", command=self.reset_squat_count)
        self.reset_button.grid(row=5, column=4, pady=5)

        # Camera and measurement buttons
        self.camera_button = tk.Button(self.root, text="Toggle Camera", command=self.toggle_camera)
        self.camera_button.grid(row=3, column=0, padx=5)
        self.measurement_button = tk.Button(self.root, text="Toggle Measurement", command=self.toggle_measurement)
        self.measurement_button.grid(row=4, column=0, padx=5)

        # Matplotlib figure for live knee and femur angle plot
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Live Knee and Femur Angles (last 10 seconds)")
        self.ax.set_ylim(0, 180)  # Angle range for both angles
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Angle (°)")
        
        # Initialize lists to store time, knee, and femur angle data
        self.time_data = []
        self.knee_angle_data = []
        self.femur_angle_data = []

        # Matplotlib canvas for embedding the plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=4, rowspan=2, padx=10)

        # Update buttons and start the frame update loop
        self.update_button_colors()
        self.update_frame()

    def toggle_camera(self):
        if self.camera_mode:
            self.camera_module.stop_camera()
            self.camera_mode = False
        else:
            if self.measurement_mode:
                self.toggle_measurement()
            self.camera_module.start_camera()
            self.camera_mode = True
        self.update_button_colors()

    def toggle_measurement(self):
        if self.measurement_mode:
            self.measurement_mode = False
            self.camera_module.stop_camera()
            self.squat_count_label.grid_remove()
            self.handlebar_label.grid_remove()
            self.squatsound_checkbox.grid_remove()
            self.reset_button.grid_remove()
        else:
            if self.camera_mode:
                self.toggle_camera()
            self.measurement_mode = True
            self.camera_module.start_camera()
            self.squat_count_label.grid()
            self.handlebar_label.grid()
            self.squatsound_checkbox.grid(pady=5)
            self.reset_button.grid(pady=5)
        self.update_button_colors()

    def reset_squat_count(self):
        self.squat_count = 0
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
            self.frame = self.camera_module.get_frame()
            if self.frame is not None:
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        elif self.measurement_mode:
            self.frame, femur_angle, knee_angle, handlebar_height = measurement.create_measurement_frame(
                self.camera_module.get_frame())
            self.squat_count = measurement.squat_counter(self.squat_count, femur_angle, 0, 25, self.squatsound.get())
            self.squat_count_label.config(text=f"Squat Count: {self.squat_count}")

            if handlebar_height is not None:
                self.handlebar_label.config(text=f"Handlebar Height: {handlebar_height} cm")

            if self.frame is not None:
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(self.frame))
                self.label.config(image=frame_image)
                self.label.image = frame_image

            if knee_angle is not None and femur_angle is not None:
                # Append data for live plot
                current_time = time.time()
                self.time_data.append(current_time)
                self.knee_angle_data.append(knee_angle)
                self.femur_angle_data.append(femur_angle)

                # Remove old data beyond 10 seconds
                while self.time_data and current_time - self.time_data[0] > 10:
                    self.time_data.pop(0)
                    self.knee_angle_data.pop(0)
                    self.femur_angle_data.pop(0)

                # Update plot
                self.ax.clear()
                self.ax.set_title("Live Knee and Femur Angles (last 10 seconds)")
                self.ax.set_ylim(0, 180)
                self.ax.set_xlabel("Time (s)")
                self.ax.set_ylabel("Angle (°)")

                # Adjust time for x-axis
                times = [t - self.time_data[0] for t in self.time_data]
                self.ax.plot(times, self.knee_angle_data, label="Knee Angle", color='blue')
                self.ax.plot(times, self.femur_angle_data, label="Femur Angle", color='orange')
                self.ax.legend()

                # Draw the canvas
                self.canvas.draw()

        # Placeholder if neither mode is active
        else:
            placeholder = self.create_placeholder_frame(640, 480)
            self.label.config(image=placeholder)
            self.label.image = placeholder

        self.root.after(10, self.update_frame)

    def create_placeholder_frame(self, width, height):
        img = Image.new("RGB", (width, height), color="grey")
        return ImageTk.PhotoImage(img)
