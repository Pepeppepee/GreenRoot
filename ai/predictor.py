from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

model = YOLO(MODEL_PATH)

def predict_soil(image_path):
    results = model(image_path)

    probs = results[0].probs
    class_id = probs.top1
    confidence = probs.top1conf

    class_name = results[0].names[class_id]

    return {
        "soil_type": class_name,
        "confidence": float(confidence)
    }
