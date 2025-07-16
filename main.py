import cv2
import pygame
import time
from authentication import load_known_faces, authenticate_face
from head_pose_estimation import estimate_head_pose
from utility import open_camera, draw_title, draw_driver_info
from drowsiness_detection import detect_drowsiness

# Load known face encodings and names
known_encodings, known_names = load_known_faces()

# Initialize camera and pygame mixer
cap = open_camera()
pygame.mixer.init()

# Main control flags
authenticated_once = False
auth_start_time = None
auth_audio_played = False
show_auth_text = True
head_pose_start_time = None  # Timer to track when to start head pose

# Load authentication success audio
pygame.mixer.music.load("authentication.mp3")  # Make sure this file exists

title_start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    draw_title(frame)

    # Wait for 5 seconds showing just the title
    if time.time() - title_start_time < 5:
        cv2.imshow("Driver Safety Kit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):  # ESC or 'q'
            break
        continue  # Skip the rest and show only title during this time

    if not authenticated_once:
        identity, status, color, face_found = authenticate_face(frame, known_encodings, known_names)

        if status == "Authenticated" and face_found:
            if auth_start_time is None:
                auth_start_time = time.time()
            elif time.time() - auth_start_time >= 5:
                show_auth_text = False
                if not auth_audio_played:
                    pygame.mixer.music.play()
                    auth_audio_played = True
                authenticated_once = True
                head_pose_start_time = time.time()
        else:
            auth_start_time = None
            show_auth_text = True
            auth_audio_played = False

        if show_auth_text:
            draw_driver_info(frame, identity, status, color, face_found)

    else:
        if head_pose_start_time and time.time() - head_pose_start_time >= 10:
            frame = estimate_head_pose(frame)
            frame = detect_drowsiness(frame)

    cv2.imshow("Driver Safety Kit", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
