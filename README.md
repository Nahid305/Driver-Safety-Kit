# Driver Safety Kit

A real-time safety monitoring system that combines driver authentication, drowsiness detection, head pose estimation, and alcohol detection using computer vision and audio alerts.

## Features

- Face Authentication: Recognizes and verifies the driver using facial recognition.
- Drowsiness Detection: Monitors eye closure, blinking rate, and yawning using Mediapipe FaceMesh.
- Head Pose Estimation: Detects if the driver is distracted or not facing the road.
- Alcohol Detection (Coming Soon): To be integrated using sensors or equivalent module.
- Audio Alerts: Raises alarm when signs of drowsiness or inattention are detected.

## Modules

- `main.py`: Main control loop integrating all modules.
- `authentication.py`: Face recognition and identity verification.
- `head_pose_estimation.py`: Detects head orientation using 3D face landmarks.
- `drowsiness_detection.py`: Analyzes eyes and mouth for drowsiness signs.
- `utility.py`: Contains helper functions for drawing, audio, camera handling, etc.

## Setup

### Requirements
- Python 3.7+
- Install dependencies:
```sh
pip install -r requirements.txt
```

### Additional Files
- Place known driver images in a `known_faces/` directory.
- Ensure `authentication.mp3` and `emergency-alarm.mp3` exist in the root or `assets/` folder.

### Run the Application
```sh
python main.py
```

## Future Improvements

- Integrate alcohol detection using hardware sensor input.
- Upload alerts/logs to a cloud dashboard.
- GPS and speed tracking integration.
- Mobile app notification system.

## License

Licensed under the MIT License
