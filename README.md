<<<<<<< HEAD
Driver Drowsiness Detection System

Project Overview

Driver fatigue is one of the major causes of road accidents worldwide. This project presents a real-time Driver Drowsiness Detection System that monitors a driver's facial features through a webcam and detects signs of fatigue such as prolonged eye closure and yawning.

The system uses computer vision techniques and facial landmark detection to identify drowsiness and alert the driver using an audible alarm.

What the Project Does

The system performs the following tasks in real time:

* Captures live video from a webcam.
* Detects facial landmarks using MediaPipe Face Mesh.
* Calculates the Eye Aspect Ratio (EAR) to determine whether the driver's eyes are closed.
* Calculates the Mouth Aspect Ratio (MAR) to detect yawning.
* Displays the driver's head position (Left, Right, Down, or Center).
* Generates visual alerts when drowsiness or yawning is detected.
* Plays an alarm sound when fatigue-related behavior is detected.

Main Features

* Real-time face monitoring
* Eye closure detection
* Yawning detection
* Head position monitoring
* Alarm notification system
* Live webcam visualization


Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* Pygame


Project Workflow

1. Webcam captures live video frames.
2. MediaPipe Face Mesh detects facial landmarks.
3. Eye landmarks are used to calculate EAR.
4. Mouth landmarks are used to calculate MAR.
5. The system determines whether the driver is:

   * Awake
   * Yawning
   * Drowsy
6. An alarm is triggered when fatigue indicators are detected.


How to Run the Project

Step 1: Clone the Repository

git clone <repository-link>
cd driver-drowsiness-detection

Step 2: Create a Virtual Environment

python -m venv venv

Step 3: Activate the Virtual Environment

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

Step 5: Run the Application

venv\Scripts\python.exe main.py

Step 6: Exit the Program

Press: q

to close the application.

Required Libraries

opencv-python
mediapipe==0.10.14
numpy
pygame

Results Achieved

The developed system successfully performs real-time monitoring of the driver's facial behavior.

Observed Results

* Successfully detected eye closure using Eye Aspect Ratio (EAR).
* Successfully detected yawning using Mouth Aspect Ratio (MAR).
* Displayed driver's head orientation in real time.
* Generated on-screen alerts for fatigue-related events.
* Played an alarm sound when drowsiness conditions were detected.
* Achieved stable real-time performance using a standard webcam.

Example Outputs

Normal State

Status: AWAKE


Yawning State

Status: YAWNING
YAWNING DETECTED!

Drowsiness State

Status: DROWSY
DROWSINESS ALERT!

Challenges Faced

* Tuning EAR and MAR thresholds for different users.
* Handling variations in lighting conditions.
* Preventing false detections during normal facial movements.
* Improving yawning detection consistency.

Future Improvements

* Use a deep learning model for improved accuracy.
* Add mobile notifications or SMS alerts.
* Support night-time driving conditions.
* Deploy as a desktop or web application.
* Integrate multiple fatigue indicators for better reliability.

Conclusion

This project demonstrates the practical application of Artificial Intelligence and Computer Vision for road safety. By monitoring eye closure, yawning, and head position, the system can provide early warnings of driver fatigue and help reduce the risk of accidents.
=======
# driver-drowsiness-detection
Driver fatigue is one of the major causes of road accidents worldwide. This project presents a real-time Driver Drowsiness Detection System that monitors a driver's facial features through a webcam and detects signs of fatigue such as prolonged eye closure and yawning.
>>>>>>> a6b8add8cce0858659702701e15a835cb4330690
