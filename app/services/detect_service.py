import os
import cv2
from ultralytics import YOLO
import uuid

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = YOLO("yolov8x.pt")  # Download yolov8x.pt beforehand

def detect_objects(video_file):
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video_file.save(filepath)

    cap = cv2.VideoCapture(filepath)
    frame_number = 0
    detections = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, verbose=False)
        boxes = results[0].boxes
        labels = [model.names[int(cls)] for cls in boxes.cls]

        if labels:
            detections.append({
                "frame": frame_number,
                "objects": list(set(labels))
            })

        frame_number += 1

    cap.release()
    os.remove(filepath)
    return detections
