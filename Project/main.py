import cv2
import numpy as np

laptopcam = cv2.VideoCapture(0)  # opens the default camera
if not laptopcam.isOpened():
    print("Cannot open camera")
else:
    print("A camera was opened")

ret, frame = laptopcam.read()
cv2.imshow('Detected Markers', frame)
cv2.waitKey(0)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()

# Create the ArUco detector
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
# Detect the markers
corners, ids, rejected = detector.detectMarkers(gray)
# Print the detected markers
print("Detected markers:", ids)

if ids is not None:
    # Draw the detected markers
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)

    # Calculate the midpoint of each marker and draw it on the frame
    for i in range(len(corners)):
        # Get the four corner points of the current marker
        marker_corners = corners[i][0]
        print(f"Marker ID {ids[i][0]} corner points: {marker_corners}")

        # Calculate the midpoint (center) of the marker
        center_x = int(np.mean(marker_corners[:, 0]))  # average x-coordinates
        center_y = int(np.mean(marker_corners[:, 1]))  # average y-coordinates
        center_point = (center_x, center_y)
        print(f"Marker ID {ids[i][0]} center point (x, y): {center_point}")

        # Draw a circle at the center point
        cv2.circle(frame, center_point, radius=5, color=(0, 0, 255), thickness=-1)

    # Show the frame with the detected markers and center points
    cv2.imshow('Detected Markers with Centers', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    