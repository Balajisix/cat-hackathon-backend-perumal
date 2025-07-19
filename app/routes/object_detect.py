from flask import Blueprint, request, jsonify
from PIL import Image
import io
from huggingface_hub import hf_hub_download

object_detect_bp = Blueprint("object_detect", __name__)

yolo_model = hf_hub_download(
    repo_id="balaji2003/yolov8x-model",
    filename="yolov8x.pt"
)

@object_detect_bp.route('/detect-object', methods=['POST'])
def detect_object():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_bytes = file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

    results = yolo_model(image)
    names = yolo_model.names
    boxes = results[0].boxes
    labels_detected = [names[int(cls)] for cls in boxes.cls]

    unique_labels = list(set(labels_detected))

    return jsonify({
        "objects": unique_labels
    }) 