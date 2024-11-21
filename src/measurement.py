from PIL import Image, ImageDraw, ImageTk
import cv2
import numpy as np
import winsound

# Define the flag as a global variable outside the function
flag = False


def calculate_knee_angle(frame, marker1, marker12, marker123):
    # Validate inputs
    if not (isinstance(marker1, (list, tuple)) and len(marker1) == 2):
        return frame, None
    if not (isinstance(marker12, (list, tuple)) and len(marker12) == 2):
        return frame, None
    if not (isinstance(marker123, (list, tuple)) and len(marker123) == 2):
        return frame, None
    #coordinates of the markes -> variables
    x1, y1 = marker1
    x12, y12 = marker12
    x123, y123 = marker123


    #This code calculates the angle between two vectors (vector1 and vector2) originating from a common point. 
    # It uses the dot product formula to find the cosine of the angle, converts it from radians to degrees, and ensures 
    # no division by zero by checking the vector magnitudes.
    # Create vectors from the center points
    vector1 = np.array([x1 - x12, y1 - y12])
    vector2 = np.array([x123 - x12, y123 - y12])

    # Calculate the angle between the vectors using the dot product
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    # Prevent division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        print("Error: One or both vectors have zero magnitude.")
        return frame, None

    angle_radians = np.arccos(dot_product / (magnitude1 * magnitude2))
    angle_degrees = np.degrees(angle_radians)

    # Draw lines between the center points to visualize the vectors
    cv2.line(frame, (x1, y1), (x12, y12), (255, 0, 0), 2)  # Line from 1 to 2
    cv2.line(frame, (x123, y123), (x12, y12), (255, 0, 0), 2)  # Line from 3 to 2

    # Display the calculated angle on the image
    angle_text = f"{int(angle_degrees)} degrees"
    cv2.putText(frame, angle_text, (x12, y12 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame, angle_degrees

def measure_handlebar_height(frame, marker123, marker2, corners, marker_size_cm=8):

    ankle_coords = None
    handlebar_coords = None
    pixel_to_cm_ratio = None

    # Calculate the pixel-to-cm ratio from the detected marker corners
    if corners is not None and len(corners) > 0:
        for marker_corners in corners:
            # Calculate the diagonal of the first marker's bounding box
            top_left = marker_corners[0][0]
            bottom_right = marker_corners[0][2]
            marker_pixel_size = np.linalg.norm(np.array(top_left) - np.array(bottom_right))
            pixel_to_cm_ratio = marker_size_cm / marker_pixel_size
            break  # Use the first detected marker for ratio calculation
    
    # Validate and assign coordinates
    if isinstance(marker123, (list, tuple)) and len(marker123) == 2:
        ankle_coords = marker123
    if isinstance(marker2, (list, tuple)) and len(marker2) == 2:
        handlebar_coords = marker2

    # Check if both markers were found and are valid
    if ankle_coords is None or handlebar_coords is None:
        return frame, None  # Return the frame unchanged and indicate no height

    # Project the handlebar marker onto the vertical line through the ankle marker
    x_ankle, y_ankle = ankle_coords
    x_handlebar, y_handlebar = handlebar_coords
    x_projection = x_ankle  # Vertical line through the ankle
    y_projection = y_handlebar

    # Draw orthogonal lines for visualization
    cv2.line(frame, (x_handlebar, y_handlebar), (x_projection, y_projection), (255, 0, 255), 2)  # Horizontal
    cv2.line(frame, (x_projection, y_projection), (x_ankle, y_ankle), (0, 255, 0), 2)  # Vertical

    # Calculate the vertical height in pixels
    height_pixels = abs(y_ankle - y_projection)

    # Convert pixels to centimeters
    height_cm = height_pixels * pixel_to_cm_ratio if pixel_to_cm_ratio else None

    # Round the height to the nearest integer
    height_cm = round(height_cm) if height_cm else None

    # Display the height in cm on the frame
    height_text = f"Height: {int(height_cm)} cm" if height_cm else "Height: N/A"
    cv2.putText(frame, height_text, (x_projection, y_projection - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame, height_cm



def calculate_horizontal_angle(frame, marker1, marker12):
    # Validate the inputs
    if not (isinstance(marker1, (list, tuple)) and len(marker1) == 2):
        return frame, None
    if not (isinstance(marker12, (list, tuple)) and len(marker12) == 2):
        return frame, None

    # Assign validated coordinates
    coords_1 = marker1
    coords_12 = marker12

    # Unpack coordinates
    x1, y1 = coords_1
    x12, y12 = coords_12

    # Create the vector from marker12 to marker123
    vector = np.array([x12 - x1, y12 - y1])

    # Calculate the angle with respect to the horizontal (x-axis)
    angle_radians = np.arctan2(vector[1], vector[0])
    angle_degrees = np.degrees(angle_radians)

    # Display the calculated angle on the image
    angle_text = f"Angle: {int(angle_degrees)} degrees"
    cv2.putText(frame, angle_text, (x12, y12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame, angle_degrees


def create_measurement_frame(frame):
    if frame is None:
        return None
    marker1 = 0
    marker12= 0
    marker123= 0
    marker2= 0
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_1000)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejected = detector.detectMarkers(gray)

    if ids is not None:
        for i, marker_corners in enumerate(corners):
            marker_center = np.mean(marker_corners[0], axis=0)
            center_x, center_y = int(marker_center[0]), int(marker_center[1])
            marker_id = ids[i][0]
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            if(marker_id == 1):
                marker1 = center_x,center_y
            elif(marker_id == 12):
                marker12 = center_x,center_y
            elif(marker_id == 123):
                marker123 = center_x,center_y
            elif(marker_id == 2):
                marker2 = center_x,center_y


    # Measure handlebar height
    frame, handlebar_height = measure_handlebar_height(frame, marker123,marker2, corners)
    # Calculate angles (optional, from your existing functions)
    frame, knee_angle = calculate_knee_angle(frame, marker1,marker12,marker123)
    frame, femur_angle = calculate_horizontal_angle(frame, marker1,marker12)

    return frame, femur_angle, knee_angle, handlebar_height


def squat_counter(squat_count, femur_angle, BOTTOM_THRESHOLD, TOP_THRESHOLD, squatsound):
    global flag
    if femur_angle is not None:
        if int(femur_angle) < BOTTOM_THRESHOLD and not flag:
            if squatsound:
                winsound.Beep(4000, 200)  # Slightly longer beep for clear feedback
            flag = True  # Set flag when bottom threshold is reached

        elif int(femur_angle) > TOP_THRESHOLD and flag:
            flag = False  # Reset flag when top threshold is reached
            squat_count += 1  # Increment squat count for each completed squat

    return squat_count
