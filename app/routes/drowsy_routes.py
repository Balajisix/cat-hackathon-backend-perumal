from flask import Blueprint, request, jsonify
from PIL import Image
import time

from util import load_model, detect_drowsiness

drowsy_bp = Blueprint("drowsy", __name__)
model = load_model("model/best.pt")

drowsy_start_time = None
last_escalation_time = 0
ESCALATION_DELAY = 60 

@drowsy_bp.route("/detect", methods=["POST"])
def detect():
    global drowsy_start_time, last_escalation_time

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image = Image.open(image_file).convert('RGB')

    is_drowsy = detect_drowsiness(model, image)
    current_time = time.time()

    if is_drowsy:
        if drowsy_start_time is None:
            drowsy_start_time = current_time

        drowsy_duration = current_time - drowsy_start_time

        if drowsy_duration >= ESCALATION_DELAY and (current_time - last_escalation_time > ESCALATION_DELAY):
            last_escalation_time = current_time
            notify_manager()

            return jsonify({
                "status": "drowsy",
                "message": "Hey operator, you feel drowsy? Have a break.",
                "escalation": True
            })

        return jsonify({
            "status": "drowsy",
            "message": "Hey operator, you feel drowsy? Have a break.",
            "escalation": False
        })

    else:
        drowsy_start_time = None
        return jsonify({
            "status": "alert",
            "message": "You're alert!",
            "escalation": False
        })


def notify_manager():
    print("🚨 Escalation: Operator drowsy for over 60 seconds. Notifying manager/operator.")
