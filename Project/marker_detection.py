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

            # Append the center point to the list
            centerpoints.append((center_x, center_y))

            # Draw a circle at the center point of the marker
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

            # Put the marker ID near the center point
            marker_id = str(ids[i][0])
            cv2.putText(frame, f"ID: {marker_id}", (center_x - 10, center_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Optionally, draw the marker borders as well
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Return the modified frame with the center points and IDs
    return frame, centerpoints

def stop_measurement():
    # Placeholder for stopping the measurement process if needed
    pass
