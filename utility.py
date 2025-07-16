import cv2

def open_camera():
    """Opens the default camera and returns the VideoCapture object."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera. Check your webcam or permissions.")
    return cap

def draw_title(frame):
    """Draws the title 'Driver Safety Kit' in blue on the given frame."""
    color = (255, 153, 0)  # Bright blue (BGR)
    cv2.putText(
        frame, "Driver Safety Kit", (20, 40),
        cv2.FONT_HERSHEY_DUPLEX, 1, color, 2,
        cv2.LINE_AA
    )

def draw_driver_info(frame, identity, status, color, face_found):
    """
    Draws identity/status only if face is found.
    If no face, prints 'No Face Detected' in red.
    """
    font = cv2.FONT_HERSHEY_DUPLEX

    if face_found:
        cv2.putText(frame, f"Driver : {identity}", (20, 95), font, 1, color, 2)
        cv2.putText(frame, status, (20, 140), font, 1, color, 2)
    else:
        red = (0, 0, 255)
        cv2.putText(frame, "No Face Detected", (20, 95), font, 1, red, 2)

def draw_face_box(frame, x, y, w, h):
    """Draws a green rectangle around the detected face and a label 'Face'."""
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, "Face", (x, y - 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def draw_head_status(frame, status, color):
    """Displays the head direction status on the frame."""
    cv2.putText(frame, status, (30, 100), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2, cv2.LINE_AA)

def draw_attention_alerts(frame):
    """Displays 'Not Normal' and 'Alert' messages with red warning."""
    red = (0, 0, 255)
    cv2.putText(frame, "Not Normal", (30, 160), cv2.FONT_HERSHEY_DUPLEX, 1, red, 2, cv2.LINE_AA)
    cv2.putText(frame, "Alert", (30, 220), cv2.FONT_HERSHEY_DUPLEX, 1, red, 2, cv2.LINE_AA)

def draw_eye_status(frame, left_status, right_status):
    color_left = (255, 0, 0) if left_status == "open" else (0, 0, 255)
    color_right = (255, 0, 0) if right_status == "open" else (0, 0, 255)
    cv2.putText(frame, f"LEFT EYE  : {left_status.upper()}", (30, 40), cv2.FONT_HERSHEY_DUPLEX, 0.7, color_left, 1)
    cv2.putText(frame, f"RIGHT EYE : {right_status.upper()}", (30, 70), cv2.FONT_HERSHEY_DUPLEX, 0.7, color_right, 1)

def draw_blink_info(frame, blink_count):
    text = f"{blink_count} times | NORMAL"
    color = (0, 0, 0)
    if blink_count > 25:
        text = f"{blink_count} times | SLEEPY"
        color = (0, 0, 255)
    cv2.putText(frame, f"Blinks : {text}", (20, 150), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

def draw_yawn_info(frame, yawn_duration):
    text = f"{round(yawn_duration, 1)} sec | NORMAL"
    color = (0, 0, 0)
    if yawn_duration > 6:
        text = f"{round(yawn_duration, 1)} sec | SLEEPY"
        color = (0, 0, 255)
    cv2.putText(frame, f"Yawns : {text}", (20, 200), cv2.FONT_HERSHEY_DUPLEX, 1, color, 2)

def draw_mouth_and_eyes(frame, landmarks, left_eye, right_eye, mouth_points, w, h):
    for eye in [left_eye, right_eye]:
        for idx in eye:
            x, y = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 2, (0, 255, 255), -1)

    for i in range(len(mouth_points) - 1):
        pt1 = (int(landmarks[mouth_points[i]].x * w), int(landmarks[mouth_points[i]].y * h))
        pt2 = (int(landmarks[mouth_points[i + 1]].x * w), int(landmarks[mouth_points[i + 1]].y * h))
        cv2.line(frame, pt1, pt2, (0, 165, 255), 2)
