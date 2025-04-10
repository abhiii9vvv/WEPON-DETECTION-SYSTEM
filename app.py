from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import smtplib
import ssl
from email.message import EmailMessage
import pygame
import os
import time
from datetime import datetime

app = Flask(__name__)

# Load ONNX model
net = cv2.dnn.readNetFromONNX("models/best.onnx")

# Classes
CLASSES = ['knife', 'gun']

# Email setup
sender_email = "******@gmail.com"
receiver_email = "******@gmail.com"
password = "******"

# Detection stats and logs
detection_stats = {"gun": 0, "knife": 0}
detection_logs = []

def send_email(image_path):
    try:
        msg = EmailMessage()
        msg.set_content("Weapon detected by the system! See attached image.")
        msg["Subject"] = "Weapon Alert!"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Attach image
        with open(image_path, 'rb') as img:
            img_data = img.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=os.path.basename(image_path))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print("[✔] Email sent successfully!")
    except Exception as e:
        print("[!] Failed to send email:", e)

# Initialize audio
def play_alarm():
    try:
        audio_path = os.path.join(os.getcwd(), 'static', 'audio.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        print("[✔] Alarm sound playing!")
    except Exception as e:
        print("[!] Alarm sound error:", e)

# Process frame
def detect_weapons(frame):
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (640, 640), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward()

    rows = outputs.shape[1]
    image_height, image_width = frame.shape[:2]
    x_factor = image_width / 640
    y_factor = image_height / 640

    detected = False

    for i in range(rows):
        row = outputs[0][i]
        confidence = row[4]
        if confidence >= 0.5:
            class_scores = row[5:]
            class_id = np.argmax(class_scores)
            if class_scores[class_id] > 0.5:
                cx, cy, w, h = row[0:4]
                left = int((cx - w / 2) * x_factor)
                top = int((cy - h / 2) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                detected = True

                label = CLASSES[class_id]
                detection_stats[label] += 1
                detection_logs.append(f"{label.upper()} - {time.strftime('%H:%M:%S')}")

                cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 0, 255), 2)
                label_text = f"{label}: {round(confidence * 100, 2)}%"
                cv2.putText(frame, label_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return frame, detected

# Initialize camera
camera = cv2.VideoCapture(0)

last_alert_time = 0
cooldown = 10  # seconds

def generate_frames():
    global last_alert_time
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame, detected = detect_weapons(frame)

            if detected and (time.time() - last_alert_time > cooldown):
                print("[!] Weapon Detected!")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_path = f'static/detected_{timestamp}.jpg'
                cv2.imwrite(image_path, frame)
                send_email(image_path)
                play_alarm()
                last_alert_time = time.time()

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detection_data')
def detection_data():
    return jsonify({
        "gun": detection_stats["gun"],
        "knife": detection_stats["knife"],
        "logs": detection_logs[-6:]  # Send last 6 logs only
    })

if __name__ == '__main__':
    app.run(debug=True)
