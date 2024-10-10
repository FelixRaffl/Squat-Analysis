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

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
parameters = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

corners, ids, rejected = detector.detectMarkers(gray)
