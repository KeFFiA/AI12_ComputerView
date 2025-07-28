FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY /Apps/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./Claims /app

CMD ["python", "main.py"]