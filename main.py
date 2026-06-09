import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import cv2
import mediapipe as mp
import numpy as np
import time
import pygame


# -----------------------------
# Alarm Setup
# -----------------------------
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALARM_PATH = os.path.join(BASE_DIR, "alarm.wav")

try:
    pygame.mixer.music.load(ALARM_PATH)
    alarm_file_available = True
    print("Alarm file loaded successfully.")
except:
    print("alarm.wav not found. Alarm sound will not play.")
    alarm_file_available = False

last_alarm_time = 0


def play_alarm():
    global last_alarm_time

    if not alarm_file_available:
        return

    if pygame.mixer.music.get_busy():
        return

    current_time = time.time()

    if current_time - last_alarm_time < 3:
        return

    pygame.mixer.music.play()
    last_alarm_time = current_time


def stop_alarm():
    if alarm_file_available:
        pygame.mixer.music.stop()


# -----------------------------
# EAR Calculation
# -----------------------------
def calculate_ear(eye_points):
    v1 = np.linalg.norm(eye_points[1] - eye_points[5])
    v2 = np.linalg.norm(eye_points[2] - eye_points[4])
    h = np.linalg.norm(eye_points[0] - eye_points[3])

    if h == 0:
        return 0

    return (v1 + v2) / (2.0 * h)


# -----------------------------
# MAR Calculation
# -----------------------------
def calculate_mar(mouth_points):
    vertical = np.linalg.norm(mouth_points[1] - mouth_points[2])
    horizontal = np.linalg.norm(mouth_points[0] - mouth_points[3])

    if horizontal == 0:
        return 0

    return vertical / horizontal


# -----------------------------
# MediaPipe Setup
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [61, 13, 14, 291]


# -----------------------------
# Thresholds
# -----------------------------
EAR_THRESHOLD = 0.15
MAR_THRESHOLD = 0.65
DROWSY_FRAME_LIMIT = 35


# -----------------------------
# Counter
# -----------------------------
closed_eye_frames = 0


# -----------------------------
# Camera Setup
# -----------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Could not access camera.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# -----------------------------
# Main Loop
# -----------------------------
while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read frame.")
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    status = "AWAKE"
    warning_message = "Driver is Awake"
    head_position = "CENTER"
    avg_ear = 0
    mar = 0

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        left_eye_points = []
        right_eye_points = []
        mouth_points = []

        for idx in LEFT_EYE:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            left_eye_points.append([x, y])
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        for idx in RIGHT_EYE:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            right_eye_points.append([x, y])
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        for idx in MOUTH:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            mouth_points.append([x, y])
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

        left_eye_points = np.array(left_eye_points)
        right_eye_points = np.array(right_eye_points)
        mouth_points = np.array(mouth_points)

        left_ear = calculate_ear(left_eye_points)
        right_ear = calculate_ear(right_eye_points)
        avg_ear = (left_ear + right_ear) / 2.0
        mar = calculate_mar(mouth_points)

        # Head position display only
        nose = face_landmarks.landmark[1]
        nose_x = int(nose.x * w)
        nose_y = int(nose.y * h)

        center_x = w // 2
        center_y = h // 2

        cv2.circle(frame, (nose_x, nose_y), 5, (255, 255, 0), -1)

        if nose_x < center_x - 100:
            head_position = "LOOKING LEFT"
        elif nose_x > center_x + 100:
            head_position = "LOOKING RIGHT"
        elif nose_y > center_y + 80:
            head_position = "HEAD DOWN"
        else:
            head_position = "CENTER"

        # Eye drowsiness logic
        if avg_ear < EAR_THRESHOLD:
            closed_eye_frames += 1
        else:
            closed_eye_frames = 0

        # Final decision
        if closed_eye_frames >= DROWSY_FRAME_LIMIT:
            status = "DROWSY"
            warning_message = "DROWSINESS ALERT!"

        elif mar > MAR_THRESHOLD:
            status = "YAWNING"
            warning_message = "YAWNING DETECTED!"

        else:
            status = "AWAKE"
            warning_message = "Driver is Awake"

        # Alarm only for DROWSY
        if status  in ["DROWSY", "YAWNING"]:
            play_alarm()
        else:
            stop_alarm()

    else:
        closed_eye_frames = 0
        stop_alarm()

        cv2.putText(frame, "No face detected", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Display output
    color = (0, 255, 0) if status == "AWAKE" else (0, 0, 255)

    cv2.putText(frame, f"Status: {status}", (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"MAR: {mar:.2f}", (30, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, f"Head: {head_position}", (30, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if warning_message == "YAWNING DETECTED!":
        cv2.putText(frame, warning_message, (30, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

    elif status != "AWAKE":
        cv2.putText(frame, warning_message, (30, 190),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Driver Drowsiness Detection System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


stop_alarm()
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()