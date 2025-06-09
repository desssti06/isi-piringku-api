FROM python:3.11-slim

WORKDIR /app

# Install dependencies sistem yang dibutuhkan ultralytics dan opencv
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dan install pip requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Salin semua source code
COPY . .

# Jalankan server FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
