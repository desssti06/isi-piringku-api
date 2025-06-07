from ultralytics import YOLO
import numpy as np

CATEGORY_MAP = {
    0: "buah",
    1: "lauk",
    2: "makanan_pokok",
    3: "piring",
    4: "sayur"
}

model = YOLO("model/best.pt")  # ganti path ke modelmu

def predict_image(image_path):
    results = model(image_path)[0]

    masks = results.masks.data.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy().astype(int)
    boxes = results.boxes.xyxy.cpu().numpy()

    return masks, classes, boxes
