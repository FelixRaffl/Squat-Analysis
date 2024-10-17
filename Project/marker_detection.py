import cv2
import numpy as np

def calculate_femur_angle(corners):
    # Dummy calculation of femur angle based on marker positions
    # Replace this with real angle calculations using your ArUco marker positions
    return np.random.uniform(60, 90)  # Random angle for demonstration

def calculate_and_draw_angle(frame, centerpoints):
        x1, y1 = centerpoints[0][1], centerpoints[0][2]
        x2, y2 = centerpoints[1][1], centerpoints[1][2]
        x3, y3 = centerpoints[2][1], centerpoints[2][2]
        
        # Create vectors from the centerpoints
        vector1 = np.array([x1 - x2, y1 - y2])
        vector2 = np.array([x3 - x2, y3 - y2])

        # Calculate the angle between the vectors using the dot product
        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)
        angle_radians = np.arccos(dot_product / (magnitude1 * magnitude2))
        angle_degrees = np.degrees(angle_radians)

        # Draw lines between the centerpoints to visualize the vectors
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Line from 1 to 2
        cv2.line(frame, (x3, y3), (x2, y2), (255, 0, 0), 2)  # Line from 3 to 2

        # Display the calculated angle on the image
        angle_text = f"{int(angle_degrees)} degrees"
        cv2.putText(frame, angle_text, (x2, y2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame

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
        centerpoints.sort(key=lambda x: x[0])
    centerpoints_array = np.array(centerpoints)
    return frame, centerpoints_array

def stop_measurement():
    pass
