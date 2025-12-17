# ---------- stage 1: python 3.12 (jammy) ----------
FROM python:3.12-jammy AS python312

# ---------- stage 2: cuda runtime (jammy) ----------
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# --- system deps ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-rus \
        tesseract-ocr-eng \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# --- copy python 3.12 (glibc-compatible) ---
COPY --from=python312 /usr/local /usr/local

# --- make python default ---
RUN ln -sf /usr/local/bin/python3.12 /usr/bin/python && \
    ln -sf /usr/local/bin/python3.12 /usr/bin/python3

ENV PATH="/usr/local/bin:${PATH}"

# ---------- app ----------
WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install torch==2.3.0+cu121 torchvision==0.18.0+cu121 torchaudio==2.3.0+cu121 \
        --extra-index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r requirements.txt

COPY src /app

CMD ["python", "main.py"]
