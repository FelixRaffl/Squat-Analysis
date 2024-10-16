import cv2
import numpy as np

def calculate_femur_angle(corners):
    # Dummy calculation of femur angle based on marker positions
    # Replace this with real angle calculations using your ArUco marker positions
    return np.random.uniform(60, 90)  # Random angle for demonstration

def calculate_knee_angle(corners):
    # Dummy calculation of knee angle based on marker positions
    return np.random.uniform(100, 140)  # Random angle for demonstration

def aruco_detection(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    parameters = cv2.aruco.DetectorParameters()

    # Create ArUco detector
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejected = detector.detectMarkers(gray)
    centerpoints =[]
    if ids is not None:
        for i, marker_corners in enumerate(corners):
            # Calculate the center of the marker by averaging the corner points
            marker_center = np.mean(marker_corners[0], axis=0)
            center_x, center_y = int(marker_center[0]), int(marker_center[1])
            
            # Extract the ID as an integer
            marker_id = ids[i][0]
            
            # Append a new row with the marker ID, X, and Y coordinates
            centerpoints.append([marker_id, center_x, center_y])
            
            # Draw a circle at the center point of the marker
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
        centerpoints_array = np.array(centerpoints)    
    
    return frame, centerpoints_array

def stop_measurement():
    pass
