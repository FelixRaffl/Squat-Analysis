cha

This is the minimal software structure we would expect. 

The optional requirements are given as:

Integration of a valid squat counter incl. visualization (6 %)
Create a sound every time a valid squat was done & include a check Box for the feature in your visualization (6%)
Integration of a knee angle graph in the visualisation (always visualize the last X seconds) (11%)
Integration of handle tracking incl. visualization of squat hight (6%)
Integration of handle tracking incl. visualization of squat hight (6%)
Integration of a handle position graph in the visualisation (always visualize the last Y seconds) (11%)


Each of the given optional requirements would have an impact on the software structure. A possible structure could look like:



Initializing state:
+ Initialize data storage
+ Initialize GUI
+ Initialize timing

Idle state:
+ Waiting for a GUI Callback

GUI Callbacks
+ Start Button (Triggers a state change to Measurement state)
+ Stop Button  (Triggers a state change to Idle state)
+ Sound Checkbox (A change of the checkbox triggers a variable change)
+ Counter Reset Button (Triggers an update of the counter value to 0)

Measurement state
+ Get the current frame from the camera with a time stap
+ Find the marker (ArUco Codes) within the current frame
+ Calculate the current knee and femur angle and the handle position from the marker (ArUco Codes) position
+ Store the time stamp, current knee and femur angle and hnadle position in a respective ditionary/structure
+ Check whether a valid squat has happened and act accordingly (sound + count + squat hight)
+ Update the GUI (both graphs, squat count label, squat hight label)

