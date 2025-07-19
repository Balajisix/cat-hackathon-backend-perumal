import os
import cv2
import uuid
from huggingface_hub import hf_hub_download

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

yolo_model = hf_hub_download(
    repo_id="balaji2003/yolov8x-model",
    filename="yolov8x.pt"
)

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

        results = yolo_model(frame, verbose=False)
        boxes = results[0].boxes
        labels = [yolo_model.names[int(cls)] for cls in boxes.cls]

        if labels:
            detections.append({
                "frame": frame_number,
                "objects": list(set(labels))
            })

        frame_number += 1

    cap.release()
    os.remove(filepath)
    return detections