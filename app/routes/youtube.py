from flask import Blueprint, request, jsonify
import requests
import os

youtube_api = Blueprint('youtube_api', __name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@youtube_api.route("/api/search_video", methods=["GET"])
def search_video():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=5"

    response = requests.get(youtube_url)
    if response.status_code != 200:
        return jsonify({"error": "YouTube API error"}), 500

    data = response.json()

    results = [
        {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        for item in data.get("items", [])
    ]

    return jsonify(results)
