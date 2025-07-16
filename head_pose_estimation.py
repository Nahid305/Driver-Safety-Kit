import cv2
import mediapipe as mp
import time
import pygame

# Initialize Mediapipe modules
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

# Alarm setup
pygame.mixer.init()
alarm_file = "emergency-alarm.mp3"
alarm_playing = False
attention_start_time = None

def estimate_head_pose(frame):
    global alarm_playing, attention_start_time

    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_results = face_detection.process(frame_rgb)

    if not face_results.detections:
        cv2.putText(frame, "No Face Detected", (20, 100),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        attention_start_time = None
        if alarm_playing:
            pygame.mixer.music.stop()
            alarm_playing = False
        return frame

    for detection in face_results.detections:
        bbox = detection.location_data.relative_bounding_box
        x, y, w_bbox, h_bbox = int(bbox.xmin * w), int(bbox.ymin * h), int(bbox.width * w), int(bbox.height * h)

        #cv2.rectangle(frame, (x, y), (x + w_bbox, y + h_bbox), (0, 255, 0), 2)
        #cv2.putText(frame, "Face", (x, y - 20),
                    #cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            nose = landmarks.landmark[1]
            left = landmarks.landmark[234]
            right = landmarks.landmark[454]

            nose_x = int(nose.x * w)
            left_x = int(left.x * w)
            right_x = int(right.x * w)

            if nose_x < left_x:
                status = "Right"
            elif nose_x > right_x:
                status = "Left"
            else:
                status = "Road"

            # Colors
            focus_text = "Focus :"
            focus_color = (0, 255, 0)       # Green
            alert_color = (0, 0, 255)       # Red
            status_color = (0, 255, 255) if status in ["Left", "Right"] else (0, 255, 0)

            position = (20, 100)
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1
            thickness = 2

            # Measure width of "Focus :" to position the status
            (focus_width, _), _ = cv2.getTextSize(focus_text, font, font_scale, thickness)

            # Draw "Focus :" in green
            cv2.putText(frame, focus_text, position, font, font_scale, focus_color, thickness, cv2.LINE_AA)

            # Draw status in yellow/green after "Focus :"
            status_pos = (position[0] + focus_width, position[1])
            cv2.putText(frame, f" {status}", status_pos, font, font_scale, status_color, thickness, cv2.LINE_AA)

            # Handle inattention
            if status in ["Left", "Right"]:
                if attention_start_time is None:
                    attention_start_time = time.time()
                elif time.time() - attention_start_time > 10:
                    # Add " | Not Normal" after status
                    not_normal_text = " | Not Normal"
                    cv2.putText(frame, not_normal_text,
                                (status_pos[0] + 95, position[1]),
                                font, font_scale, alert_color, thickness, cv2.LINE_AA)

                    # Start alarm if not already
                    if not alarm_playing:
                        pygame.mixer.music.load(alarm_file)
                        pygame.mixer.music.play(-1)
                        alarm_playing = True
            else:
                attention_start_time = None
                if alarm_playing:
                    pygame.mixer.music.stop()
                    alarm_playing = False

            # If alarm is playing, draw "Alert" below "Focus"
            if alarm_playing:
                alert_pos = (20, 260)  # Below the "Focus" line
                cv2.putText(frame, "Alert", alert_pos, font, font_scale, alert_color, thickness, cv2.LINE_AA)

    return frame
