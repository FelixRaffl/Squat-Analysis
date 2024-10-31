from PIL import Image, ImageDraw, ImageTk
import cv2,numpy as np
import winsound


class MeasurementModule:
    def __init__(self):
        self.flag = False
        self.squat_count=0
    def calculate_knee_angle(self,frame, centerpoints):
        if len(centerpoints) < 3:
            return frame, None  # Return the frame unchanged and indicate no angle
        
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

        return frame,angle_degrees

    def calculate_horizontal_angle(self, frame, centerpoints):
        # Initialize variables to hold coordinates
        coords_1 = None
        coords_12 = None

        # Find the coordinates of markers with ID 1 and 12
        for marker in centerpoints:
            marker_id = marker[0]
            if marker_id == 1:
                coords_1 = (marker[1], marker[2])  # (x, y) for marker 1
            elif marker_id == 12:
                coords_12 = (marker[1], marker[2])  # (x, y) for marker 12

        # Check if both markers were found
        if coords_1 is None or coords_12 is None:
            return frame, None  # Return the frame unchanged and indicate no angle
        
        x1, y1 = coords_1
        x12, y12 = coords_12
        
        # Create the vector from marker 1 to marker 12
        vector = np.array([x12 - x1, y12 - y1])
        
        # Calculate the angle with respect to the horizontal (x-axis)
        angle_radians = np.arctan2(vector[1], vector[0])
        angle_degrees = np.degrees(angle_radians)
            
        # Display the calculated angle on the image
        angle_text = f"Angle: {int(angle_degrees)} degrees"
        cv2.putText(frame, angle_text, (x12, y12 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame, angle_degrees

    def create_measurement_frame(self,frame):
        if frame is None:
            # Handle case where frame is None
            return None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
        centerpoints =[]
        if ids is not None:
            for i, marker_corners in enumerate(corners):
                marker_center = np.mean(marker_corners[0], axis=0)
                center_x, center_y = int(marker_center[0]), int(marker_center[1])
                marker_id = ids[i][0]
                centerpoints.append([marker_id, center_x, center_y])
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
            centerpoints.sort(key=lambda x: x[0])
        centerpoints_array = np.array(centerpoints)
        frame ,kneeangle= self.calculate_knee_angle(frame,centerpoints_array)
        frame ,femurangle = self.calculate_horizontal_angle(frame,centerpoints_array)
        return frame,femurangle,kneeangle
    def squat_counter(self,femur_angle,BOTTOM_THRESHOLD,TOP_THRESHOLD,squatsound):
        if femur_angle is not None:
            if int(femur_angle) < int(BOTTOM_THRESHOLD)and not self.flag:
                if(squatsound):
                    winsound.Beep(4000, 10)
                self.flag = True

            elif int(femur_angle) > int(TOP_THRESHOLD)and self.flag:
                self.flag = False
                self.squat_count += 1  
        return self.squat_count