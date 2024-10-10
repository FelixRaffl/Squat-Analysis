import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
laptopcam = cv2.VideoCapture(0) #opens the default camera
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
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('Detected Markers', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
