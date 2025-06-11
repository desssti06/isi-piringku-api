from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from ultralytics import YOLO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from fractions import Fraction
import random
import shutil
import os
import uuid

app = FastAPI()

model = YOLO("https://drive.google.com/file/d/1-Vy38rqtDLvVLgnEQ47YsQpHj5Gq5mzA/view?usp=sharing")  

CATEGORY_MAP = {
    0: "buah",
    1: "lauk",
    2: "makanan_pokok",
    3: "piring",
    4: "sayur"
}

def random_color(alpha=0.4):
    return [random.random(), random.random(), random.random(), alpha]

@app.post("/predict-isipiring")
async def predict(file: UploadFile = File(...)):
    # Simpan gambar temporer
    uid = uuid.uuid4().hex
    temp_filename = f"temp_{uid}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Prediksi
    results = model(temp_filename)[0]

    masks = results.masks.data.cpu().numpy()
    classes = results.boxes.cls.cpu().numpy().astype(int)
    boxes = results.boxes.xyxy.cpu().numpy()
    confs = results.boxes.conf.cpu().numpy()

    area_per_category = {cat: 0 for cat in CATEGORY_MAP.values()}
    total_food_area = 0

    for mask, cls in zip(masks, classes):
        cat_name = CATEGORY_MAP.get(cls)
        if cat_name is None:
            continue
        area = np.sum(mask)
        area_per_category[cat_name] += area
        if cat_name != "piring":
            total_food_area += area

    proporsi = {}
    for cat in area_per_category:
        if cat == "piring":
            continue
        prop = area_per_category[cat] / total_food_area if total_food_area > 0 else 0
        proporsi[cat] = round(prop, 4)

    targets = {
        "lauk": 1/3,
        "buah": 1/3,
        "makanan_pokok": 2/3,
        "sayur": 2/3
    }

    evaluasi = {}
    rekomendasi = {}

    for cat in targets:
        prop = proporsi.get(cat, 0)
        target = targets[cat]
        cukup = prop >= target
        evaluasi[cat] = "✅ Cukup" if cukup else "❌ Kurang"
        if not cukup:
            kekurangan = target - prop
            pecahan = Fraction(float(kekurangan)).limit_denominator(6)
            rekomendasi[cat] = f"Tambahkan sekitar {pecahan.numerator}/{pecahan.denominator} bagian piring {cat}"

    # Gambar hasil
    class_color_map = {cls: random_color() for cls in set(classes)}
    img = plt.imread(temp_filename)
    plt.figure(figsize=(10, 10))
    plt.imshow(img)
    plt.axis('off')

    for mask, cls, box, conf in zip(masks, classes, boxes, confs):
        cat_name = CATEGORY_MAP.get(cls)
        if cat_name is None:
            continue

        color = class_color_map[cls]
        mask_img = np.zeros((mask.shape[0], mask.shape[1], 4))
        mask_img[:, :, 0:3] = color[:3]
        mask_img[:, :, 3] = mask * color[3]
        plt.imshow(mask_img)

        x1, y1, x2, y2 = box
        rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                 linewidth=2, edgecolor=color[:3], facecolor='none')
        plt.gca().add_patch(rect)

        plt.text(x1, y1 - 10, f"{cat_name} ({conf:.2f})",
                 color='white', fontsize=12, weight='bold',
                 bbox=dict(facecolor=color[:3], alpha=0.7, pad=2))

    # Simpan gambar hasil
    output_dir = "static/results"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{uid}.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

    # Hapus gambar asli (opsional)
    os.remove(temp_filename)

    return JSONResponse({
        "proporsi": proporsi,
        "evaluasi": evaluasi,
        "rekomendasi": rekomendasi,
        "image_url": f"/result-image/{uid}"
    })


@app.get("/result-image/{image_id}")
async def get_result_image(image_id: str):
    filepath = f"static/results/{image_id}.png"
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="image/png")
    return JSONResponse({"error": "Image not found"}, status_code=404)
