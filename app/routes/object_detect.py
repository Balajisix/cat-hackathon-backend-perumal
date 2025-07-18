from flask import Blueprint, request, jsonify
from PIL import Image
import io
from ultralytics import YOLO

object_detect_bp = Blueprint("object_detect", __name__)

# Load YOLOv8 model (make sure yolov8x.pt is in the correct path)
model = YOLO("yolov8x.pt")

@object_detect_bp.route('/detect-object', methods=['POST'])
def detect_object():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    results = model(image)
    names = model.names
    boxes = results[0].boxes
    labels_detected = [names[int(cls)] for cls in boxes.cls]

    # Remove duplicates
    unique_labels = list(set(labels_detected))

    return jsonify({
        "objects": unique_labels
    }) 