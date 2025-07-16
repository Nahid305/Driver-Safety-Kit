import face_recognition
import os
import numpy as np
import cv2

def load_known_faces(known_faces_dir="known_faces"):
    """Loads known face encodings and their names from the given directory."""
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image = face_recognition.load_image_file(f"{known_faces_dir}/{filename}")
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)

    return known_encodings, known_names

def authenticate_face(frame, known_encodings, known_names):
    """
    Authenticates faces in the frame.
    Returns tuple: (identity, status, color, face_found: bool)
    """
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    if not face_encodings:
        return "No Face Detected", "No Face Detected", (0, 0, 255), False  # Red

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        if True in matches:
            best_match_index = np.argmin(face_distances)
            identity = known_names[best_match_index]
            return identity, "Authenticated", (50, 205, 50), True  # Lime green

    return "Unknown", "Unauthenticated", (0, 0, 255), True  # Red if unknown face
