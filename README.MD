# 🥗 API "Isi Piringku" – Backend FastAPI

API ini digunakan untuk memprediksi komposisi makanan di atas piring menggunakan model segmentasi gambar **YOLOv8**. Hasil prediksi memberikan informasi proporsi makanan, evaluasi kecukupan, dan rekomendasi tambahan jika perlu.

---

## 📦 Endpoint

### `POST /predict-isipiring`

**Deskripsi**:  
Menerima gambar (JPG/PNG) dan mengembalikan:

- Proporsi makanan (buah, sayur, lauk, makanan pokok)
- Evaluasi kecukupan berdasarkan standar "Isi Piringku"
- Rekomendasi tambahan (jika ada kekurangan)
- URL gambar hasil segmentasi

**Form Data**:
- `file`: File gambar (`image/jpeg`, `image/png`)

**Contoh Request (dengan `fetch`)**:
```javascript
const formData = new FormData();
formData.append("file", selectedImageFile); // dari input type="file"

const res = await fetch("http://localhost:8000/predict-isipiring", {
  method: "POST",
  body: formData,
});

const data = await res.json();
console.log(data);
```

**Contoh Respons**:
```json
{
  "proporsi": {
    "buah": 0.25,
    "lauk": 0.3,
    "makanan_pokok": 0.4,
    "sayur": 0.05
  },
  "evaluasi": {
    "lauk": "✅ Cukup",
    "buah": "❌ Kurang",
    "makanan_pokok": "❌ Kurang",
    "sayur": "❌ Kurang"
  },
  "rekomendasi": {
    "buah": "Tambahkan sekitar 1/12 bagian piring buah",
    "makanan_pokok": "Tambahkan sekitar 1/6 bagian piring makanan_pokok",
    "sayur": "Tambahkan sekitar 7/12 bagian piring sayur"
  },
  "image_url": "/result-image/5cf612dc..."
}
```

---

### `GET /result-image/{image_id}`

**Deskripsi**:  
Mengambil gambar hasil segmentasi dengan ID yang diperoleh dari `image_url` pada respons `POST /predict-isipiring`.

**Contoh**:
```http
GET http://localhost:8000/result-image/5cf612dc...
```

**Contoh penggunaan di frontend (React/Next.js)**:
```jsx
<img src={`http://localhost:8000/result-image/${imageId}`} alt="Hasil Segmentasi" />
```

---

## 📁 Struktur Direktori

```
your_project/
├── app/
│   └── main.py  
│   └── yolov8_model.pt  
├── model/
│   └── best.pt          # Model YOLOv8
├── static/
│   └── results/         # Gambar hasil segmentasi disimpan di sini
├── README.MD
├── requirement.txt
```

---

## 🚀 Cara Menjalankan Backend

1. Install dependensi:
```bash
pip install fastapi uvicorn matplotlib ultralytics
```

2. Jalankan server:
```bash
uvicorn app.main:app --reload
```

3. Server akan tersedia di:
```
http://localhost:8000
```

---

## ℹ️ Catatan Tambahan

- Semua respons evaluasi menggunakan icon (✅ / ❌) agar mudah dimengerti oleh pengguna.
- `image_url` bisa langsung digunakan sebagai `src` gambar.
- Gambar yang diunggah disegmentasi berdasarkan 5 kelas:
  - `buah`
  - `sayur`
  - `lauk`
  - `makanan_pokok`
  - `piring` (tidak dihitung dalam proporsi makanan)
