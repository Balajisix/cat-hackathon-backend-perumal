from flask import Blueprint, request, jsonify
from ..services.detect_service import detect_objects

detect_bp = Blueprint("detect_bp", __name__, url_prefix="/api")

@detect_bp.route("/upload", methods=["POST"])
def upload_video():
    if "video" not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files["video"]
    detections = detect_objects(video)

    return jsonify({
        "message": "Processed successfully",
        "detections": detections
    })
