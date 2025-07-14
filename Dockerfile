FROM python:3.10-slim

# Установим зависимости системы
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

# Установим Python зависимости
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь проект
COPY ./Medical /app

# Запуск основного скрипта по умолчанию
CMD ["python", "main.py"]