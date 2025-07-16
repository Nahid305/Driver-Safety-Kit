import cv2
import mediapipe as mp
import time
import numpy as np
from collections import deque
import pygame
import threading
from utility import draw_eye_status, draw_blink_info, draw_yawn_info, draw_mouth_and_eyes

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

# Alarm setup
pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("emergency-alarm.mp3")
alarm_on = False
eyes_closed_start = None
blink_times = deque()
yawn_times = deque()
blink_start_time = time.time()
yawn_active = False

def play_alarm():
    global alarm_on
    while alarm_on:
        if not pygame.mixer.get_busy():
            alarm_sound.play()
        time.sleep(1)

def eye_aspect_ratio(landmarks, eye_points, w, h):
    p = [np.array([int(landmarks[i].x * w), int(landmarks[i].y * h)]) for i in eye_points]
    ear = (np.linalg.norm(p[1] - p[5]) + np.linalg.norm(p[2] - p[4])) / (2.0 * np.linalg.norm(p[0] - p[3]))
    return ear

def detect_drowsiness(frame):
    global alarm_on, eyes_closed_start, blink_times, yawn_times, blink_start_time, yawn_active

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    h, w, _ = frame.shape
    current_time = time.time()

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # EAR Calculation
            left_eye = [33, 160, 158, 133, 153, 144]
            right_eye = [362, 385, 387, 263, 373, 380]
            left_ear = eye_aspect_ratio(face_landmarks.landmark, left_eye, w, h)
            right_ear = eye_aspect_ratio(face_landmarks.landmark, right_eye, w, h)

            eye_threshold = 0.22
            left_status = "open" if left_ear > eye_threshold else "close"
            right_status = "open" if right_ear > eye_threshold else "close"

            #draw_eye_status(frame, left_status, right_status)

            # Alarm logic
            if left_status == "close" and right_status == "close":
                if not eyes_closed_start:
                    eyes_closed_start = current_time
                elif current_time - eyes_closed_start >= 3:
                    if not alarm_on:
                        alarm_on = True
                        threading.Thread(target=play_alarm, daemon=True).start()
                    cv2.putText(frame, "Alert", (20, 260), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            else:
                eyes_closed_start = None
                if alarm_on:
                    alarm_on = False
                    pygame.mixer.stop()

            # Blink Tracking
            if left_status == "close" and right_status == "close":
                if current_time - blink_start_time > 0.2:
                    blink_times.append(current_time)
                    blink_start_time = current_time

            while blink_times and current_time - blink_times[0] > 60:
                blink_times.popleft()

            draw_blink_info(frame, len(blink_times))

            # Yawn Detection
            mouth_points = [
                61, 185, 40, 39, 37, 0, 267, 269, 270, 409,
                291, 375, 321, 405, 314, 17, 84, 181, 91, 146, 61
            ]
            lip_distance = abs(face_landmarks.landmark[13].y - face_landmarks.landmark[14].y)
            yawn_threshold = 0.06

            if lip_distance > yawn_threshold:
                if not yawn_active:
                    yawn_active = True
                    yawn_times.append((current_time, 0))
                yawn_times[-1] = (yawn_times[-1][0], yawn_times[-1][1] + (1 / 30))
            else:
                yawn_active = False

            while yawn_times and current_time - yawn_times[0][0] > 60:
                yawn_times.popleft()

            draw_yawn_info(frame, sum(duration for _, duration in yawn_times))
            #draw_mouth_and_eyes(frame, face_landmarks.landmark, left_eye, right_eye, mouth_points, w, h)

    return frame
