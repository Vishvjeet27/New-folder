# Ujjain Crowd Counting Dashboard

Al web dashboard for real-time crowd counting and alerting using CCTV or webcam footage. The dashboard provides live monitoring, color-coded alerts, and video upload analysis for crowd management in public spaces.

## Features
- Live crowd count from webcam
- Color-coded alert panel (Green: Normal, Yellow: High Density, Red: Take Alternate Route)
- Real-time alert messages when crowd thresholds are exceeded
- Upload and analyze recorded video footage for crowd counting
- Modern, responsive dashboard design

## Setup Instructions

1. **Clone or download the project folder.**

2. **Install required Python packages:**
   ```
   pip install flask ultralytics opencv-python
   ```

3. **Download the YOLOv8 model weights**
   - Place `yolov8n.pt` in the project folder.
   - You can get the weights from the official Ultralytics repository.

4. **Run the dashboard:**
   ```
   python app.py
   ```

5. **Open your browser and visit:**
   - [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- The homepage displays the live webcam feed, current crowd count, and alert panel.
- Upload a video file to analyze crowd density in recorded footage.
- Alerts and color codes help guide crowd management decisions.

## Folder Structure
```
New folder/
├── app.py
├── crowd_count_yolov8.py
├── yolov8n.pt
├── templates/
│   ├── index.html
│   └── upload.html
└── uploads/
    └── [uploaded videos]
```

## License
This project is provided for educational and public safety purposes.
