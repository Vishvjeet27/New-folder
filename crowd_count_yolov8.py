import cv2
from ultralytics import YOLO

# Load YOLOv8 model (download yolov8n.pt or yolov8s.pt from ultralytics)
model = YOLO('yolov8n.pt')  # Change to yolov8s.pt for better accuracy

# Use webcam as input source
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 inference
    results = model(frame)
    boxes = results[0].boxes
    person_count = 0

    for box in boxes:
        cls = int(box.cls[0])
        if cls == 0:  # Class 0 is 'person' in COCO
            person_count += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            color = (0, 255, 0)  # Green for normal
            if person_count > 35:
                color = (0, 0, 255)  # Red
            elif person_count > 25:
                color = (0, 255, 255)  # Yellow
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Display count and alert
    cv2.putText(frame, f'Count: {person_count}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    if person_count > 35:
        cv2.putText(frame, 'ALERT: Take alternate route!', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
    elif person_count > 25:
        cv2.putText(frame, 'Warning: High crowd density', (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)

    cv2.imshow('Crowd Counting', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
