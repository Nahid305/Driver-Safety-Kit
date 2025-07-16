# 🚗 Driver Safety Kit 🔐🧠

A real-time AI-powered system to monitor and enhance driver safety using face recognition, drowsiness detection, head pose estimation, and a dummy alcohol detection module. Designed with a modular Python architecture and computer vision techniques.

---

![Driver Safety Kit Banner](assets/banner.png) <!-- Add your own banner here -->

---

## 📌 Features

- 🔒 **Face Authentication**  
  Authenticates the driver against a known faces database using `face_recognition`.

- 🍺 **Alcohol Detection (Simulated)**  
  Simulates alcohol detection using 4 parameters (body temperature, facial gestures, body odor, NDIR sensor) and blocks access if 3 out of 4 tests fail.

- 😴 **Drowsiness Detection**  
  Detects drowsiness based on prolonged eye closure, blink rate, and yawning using Mediapipe FaceMesh.

- 👀 **Head Pose Estimation**  
  Continuously tracks driver's head direction to detect distractions (left/right) for over 10 seconds.

- 🔊 **Audio Alerts**  
  Plays warning alarms using `pygame` when drowsiness or distraction is detected.

---

## 🧠 Project Workflow

1. **Face Authentication**  
   Driver’s face is captured and matched with the pre-registered face database. Access is granted only if a match is found.

2. **Alcohol Detection (Dummy Module)**  
   Simulates 4 checks. If **3 out of 4** are positive, driver is assumed drunk → ❌ Access denied.

3. **Drowsiness Monitoring**  
   Continuously monitors for sleep signs. Alerts are triggered in real-time if thresholds are crossed.

4. **Head Pose Monitoring**  
   Detects if driver is not looking straight. A warning alert is played if distraction lasts too long.

---

## 🗃️ Folder Structure

  Driver-Safety-Kit/
│
├── assets/ # MP3 sounds & banner image
├── known_faces/ # Registered face images (.jpg/.png)
├── modules/
│ ├── authentication.py
│ ├── alcohol_check.py
│ ├── drowsiness_detection.py
│ ├── head_pose_estimation.py
│ ├── utility.py
│
├── logs/ # (optional) session logs
├── main.py # Main controller script
├── requirements.txt
├── LICENSE
└── README.md


---

## ⚙️ Setup Instructions

### ✅ Requirements

- Python 3.7+
- Dependencies:
```bash

pip install -r requirements.txt

📁 Additional Files

.Place known face images in the known_faces/ folder (e.g., john.jpg)
.Place sound files in the assets/ folder:
   .authentication.mp3
   .emergency-alarm.mp3

🚀 Run the Project
  python main.py
  Make sure your webcam is accessible. Press ESC or Q to quit.

🧪Alcohol Detection Logic
  Simulates 4 conditions:
     Body Temperature (simulated value)
     Facial Gestures (random)
     Body Odor (random)
     BAC (simulated)
❌ If 3 out of 4 conditions fail → Driver access is blocked


🌟 Future Improvements
  Integrate actual hardware sensors for alcohol & temperature
  Upload logs to cloud dashboard (Firebase / MongoDB)
  GPS and speed integration
  Mobile notification system for emergency alerts
  Deploy with Streamlit or Gradio for web-based UI

📄 License
MIT License

🙌 Credits
  Built using:
  Python
  OpenCV
  MediaPipe
  Face Recognition
  Pygame

🙌 Created By
Nahid Ansari – AI & Data Science Engineer 💼
Built with ❤️ 