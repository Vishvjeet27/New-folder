
# Flask Crowd Counting Website
from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
from ultralytics import YOLO
import os

app = Flask(__name__)
model = YOLO('yolov8n.pt')

person_count = 0
alert_message = ""

def gen_webcam():
    global person_count, alert_message
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        boxes = results[0].boxes
        person_count = 0
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 0:
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = (0, 255, 0)
                if person_count > 35:
                    color = (0, 0, 255)
                elif person_count > 25:
                    color = (0, 255, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        alert_message = ""
        if person_count > 35:
            alert_message = "ALERT: Take route to another zone!"
        elif person_count > 25:
            alert_message = "Warning: High crowd density!"
        cv2.putText(frame, f'Count: {person_count}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if alert_message:
            cv2.putText(frame, alert_message, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255) if person_count>35 else (0,255,255), 3)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def gen_video(path):
    global person_count, alert_message
    cap = cv2.VideoCapture(path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)
        boxes = results[0].boxes
        person_count = 0
        for box in boxes:
            cls = int(box.cls[0])
            if cls == 0:
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = (0, 255, 0)
                if person_count > 35:
                    color = (0, 0, 255)
                elif person_count > 25:
                    color = (0, 255, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        alert_message = ""
        if person_count > 35:
            alert_message = "ALERT: Take route to another zone!"
        elif person_count > 25:
            alert_message = "Warning: High crowd density!"
        cv2.putText(frame, f'Count: {person_count}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if alert_message:
            cv2.putText(frame, alert_message, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255) if person_count>35 else (0,255,255), 3)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template('index.html', count=person_count, alert=alert_message)

@app.route('/video_feed')
def video_feed():
    return Response(gen_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join('uploads', file.filename)
            os.makedirs('uploads', exist_ok=True)
            file.save(filepath)
            return redirect(url_for('analyse', filename=file.filename))
    return render_template('upload.html')

@app.route('/analyse/<filename>')
def analyse(filename):
    filepath = os.path.join('uploads', filename)
    return Response(gen_video(filepath), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
