from ultralytics import YOLO
from PIL import Image
import torch
import torchvision.transforms as transforms

# Load YOLOv8 Classification Model
def load_model(path: str):
    model = YOLO(path) 
    return model

def detect_drowsiness(model, image: Image.Image) -> bool:
    results = model(image)
    prediction = int(results[0].probs.top1) 
    return prediction == 1
