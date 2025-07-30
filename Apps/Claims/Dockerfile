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

RUN pip install --upgrade pip && \
    pip install torch==2.3.0+cu121 torchvision==0.18.0+cu121 torchaudio==2.3.0+cu121 \
    --extra-index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r requirements.txt

COPY ./Claims /app

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib:/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# CMD ["python", "main.py"]
CMD [ "sleep", "infinity" ]
