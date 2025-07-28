FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-setuptools \
    python3-dev \
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
    ln -s /usr/bin/python3.10 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

COPY /requirements.txt /app/requirements.txt
WORKDIR /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY ./Claims /app

# ✅ Запуск
CMD ["python", "main.py"]
