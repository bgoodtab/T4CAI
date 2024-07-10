from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_files(path):
    return app.send_static_file(path)

@app.route('/detect', methods=['POST'])
def detect():
    # Save the uploaded image
    image_file = request.files['image']
    image_path = 'input_image.jpg'
    image_file.save(image_path)

    # Perform posture detection
    posture = detect_posture(image_path)

    # Clean up
    os.remove(image_path)

    return jsonify({'posture': posture})

def detect_posture(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape

    # Simple rule-based detection: check if the head is centered
    head_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    heads = head_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(heads) == 0:
        return "No head detected"
    
    (x, y, w, h) = heads[0]
    head_center_x = x + w // 2
    mid_x = width // 2

    if abs(head_center_x - mid_x) > width * 0.1:
        return "Bad posture"
    else:
        return "Good posture"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
