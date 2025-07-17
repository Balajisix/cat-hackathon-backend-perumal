from flask import Blueprint, request, jsonify
from PIL import Image
import torch
import io

seatbelt_bp = Blueprint("seatbelt", __name__)

# Load YOLOv5 model using torch.hub
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=True)

@seatbelt_bp.route('/detect-seatbelt', methods=['POST'])
def detect_seatbelt():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    results = model(image)
    names = model.names

    labels_detected = [names[int(cls)] for cls in results.xyxy[0][:, -1]]

    print("Detected:", labels_detected)

    if "seatbelt" in labels_detected:
        return jsonify({
            "status": "seatbelt_detected",
            "message": "Seatbelt is worn."
        })
    else:
        return jsonify({
            "status": "no_seatbelt",
            "message": "Seatbelt not detected! Please wear it."
        })
