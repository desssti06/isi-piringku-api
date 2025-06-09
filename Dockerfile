FROM python:3.11-slim

# Atur workdir
WORKDIR /app

# Install dependency dasar sistem (karena YOLO butuh OpenCV & matplotlib)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Salin requirement dan install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh source code ke dalam container
COPY . .

# Buka port untuk FastAPI (default 8000)
EXPOSE 8000

# Jalankan server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
