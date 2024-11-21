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
        self.root.title("Squat Analyzing Tool")
        self.root.geometry("1600x780")
        self.camera_module = CameraModule()
        self.camera_mode = False # is camera mode on or not
        self.measurement_mode = False #is measurement mode on or not
        self.squat_count = 0
        self.frame = 0

        # Tkinter label to show the camera frames
        self.label = tk.Label(self.root)
        self.label.grid(row=0, column=0, rowspan=2, padx=10)

        # Squat count and handlebar height labels
        self.squat_count_label = tk.Label(self.root, text="Squat Count: 0", font=("Helvetica", 14))
        self.squat_count_label.grid(row=3, column=4, pady=5)
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
        self.camera_button.grid(row=2, column=0, padx=5)
        self.measurement_button = tk.Button(self.root, text="Toggle Measurement", command=self.toggle_measurement)
        self.measurement_button.grid(row=3, column=0, padx=5)

        # Matplotlib figure for live knee and femur angle plot
        self.fig_angles = Figure(figsize=(5, 2.5), dpi=100)
        self.ax_angles = self.fig_angles.add_subplot(111)
        self.ax_angles.set_title("Live Knee and Femur Angles (last 10 seconds)")
        self.ax_angles.set_ylim(0, 180)
        self.ax_angles.set_xticks(range(0, 11, 1))
        self.ax_angles.set_xlabel("Time (s)")
        self.ax_angles.set_ylabel("Angle (°)")

        # Matplotlib figure for live handlebar height plot
        self.fig_handlebar = Figure(figsize=(5, 2.5), dpi=100)
        self.ax_handlebar = self.fig_handlebar.add_subplot(111)
        self.ax_handlebar.set_title("Live Handlebar Height (last 10 seconds)")
        self.ax_handlebar.set_ylim(0, 100)  # Adjust based on expected height range
        self.ax_handlebar.set_xticks(range(0, 11, 1))
        self.ax_handlebar.set_xlabel("Time (s)")
        self.ax_handlebar.set_ylabel("Height (cm)")

        # Initialize lists to store time, knee, femur, and handlebar height data
        self.time_data = []
        self.knee_angle_data = []
        self.femur_angle_data = []
        self.handlebar_height_data = []

        # Matplotlib canvases for embedding the plots in Tkinter
        self.canvas_angles = FigureCanvasTkAgg(self.fig_angles, master=self.root)
        self.canvas_angles.get_tk_widget().grid(row=0, column=4, padx=10)
        self.canvas_handlebar = FigureCanvasTkAgg(self.fig_handlebar, master=self.root)
        self.canvas_handlebar.get_tk_widget().grid(row=1, column=4, padx=10)

        # Update buttons and start the frame update loop
        self.update_button_colors()
        self.update_frame()
    #camera on or of, if camera is on and button is pressed camera gets turned off, 
    #if camera is off and measurement mode is on and button is pressed measurement mode gets turned off and camera on
    #if camera is off and button is pressed 
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
    #same as for the camera toggling, only one is on
    def toggle_measurement(self):
        if self.measurement_mode:
            self.measurement_mode = False
            self.camera_module.stop_camera()
        else:
            if self.camera_mode:
                self.toggle_camera()
            self.measurement_mode = True
            self.camera_module.start_camera()
        self.update_button_colors()

    #resets the variable squatcount
    def reset_squat_count(self):
        self.squat_count = 0
        self.squat_count_label.config(text=f"Squat Count: {self.squat_count}")

    #makes the buttons change color so that you know if camera mode or measurement mode is active, the active one gets red
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
    #when in camera mode ,gets frame from camera if there is no frame then a grey spaceholder is drawn
    def update_frame(self):
        if self.camera_mode:
            self.frame = self.camera_module.get_frame()
            if self.frame is not None:
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.config(image=frame_image)
                self.label.image = frame_image
        elif self.measurement_mode:
            #when in measurement mode frame is given to the method thats does the measurement basically
            #calculates femur angle knee angle handbar height and the angles are drawn into the frame then it is returned and displayed
            self.frame, femur_angle, knee_angle, handlebar_height = measurement.create_measurement_frame(self.camera_module.get_frame())
            #counts the squat, the current value is given as a parameter and the current femur angle then the threshhold angles for what
            #we count as a correct squat and then the status of the squatsound checkbox is controlled and given to the function 
            self.squat_count = measurement.squat_counter(self.squat_count, femur_angle, 0, 25, self.squatsound.get())
            self.squat_count_label.config(text=f"Squat Count: {self.squat_count}")

            if handlebar_height is not None:
                self.handlebar_label.config(text=f"Handlebar Height: {handlebar_height:.2f} cm")
            #displays the created frame
            if self.frame is not None:
                frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                frame_image = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
                self.label.config(image=frame_image)
                self.label.image = frame_image

            # Append data for live plot
            if knee_angle is not None and femur_angle is not None and handlebar_height is not None:
                current_time = time.time()
                self.time_data.append(current_time)
                self.knee_angle_data.append(knee_angle)
                self.femur_angle_data.append(femur_angle)
                self.handlebar_height_data.append(handlebar_height)

                # Remove old data beyond 10 seconds
                while self.time_data and current_time - self.time_data[0] > 10:
                    self.time_data.pop(0)
                    self.knee_angle_data.pop(0)
                    self.femur_angle_data.pop(0)
                    self.handlebar_height_data.pop(0)

                # Update knee and femur angle plot
                self.ax_angles.clear()
                self.ax_angles.set_title("Live Knee and Femur Angles (last 10 seconds)")
                self.ax_angles.set_ylim(0, 180)
                self.ax_angles.set_xlabel("Time (s)")
                self.ax_angles.set_ylabel("Angle (°)")
                times = [t - self.time_data[0] for t in self.time_data]
                self.ax_angles.plot(times, self.knee_angle_data, label="Knee Angle", color='blue')
                self.ax_angles.plot(times, self.femur_angle_data, label="Femur Angle", color='orange')
                self.ax_angles.legend()
                self.canvas_angles.draw()

                # Update handlebar height plot
                self.ax_handlebar.clear()
                self.ax_handlebar.set_title("Live Handlebar Height (last 10 seconds)")
                self.ax_handlebar.set_ylim(0, 100)
                self.ax_handlebar.set_xlabel("Time (s)")
                self.ax_handlebar.set_ylabel("Height (cm)")
                self.ax_handlebar.plot(times, self.handlebar_height_data, label="Handlebar Height", color='green')
                self.ax_handlebar.legend()
                self.canvas_handlebar.draw()
        else:
            placeholder = self.create_placeholder_frame(640, 480)
            self.label.config(image=placeholder)
            self.label.image = placeholder

        self.root.after(10, self.update_frame)

    def create_placeholder_frame(self, width, height):
        img = Image.new("RGB", (width, height), color="grey")
        return ImageTk.PhotoImage(img)
