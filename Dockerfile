FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# ---------- system deps ----------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        curl \
        git \
        ca-certificates \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-rus \
        tesseract-ocr-eng \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# ---------- build python 3.12 ----------
WORKDIR /tmp

RUN wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz && \
    tar -xzf Python-3.12.2.tgz && \
    cd Python-3.12.2 && \
    ./configure \
        --enable-optimizations \
        --with-ensurepip=install && \
    make -j$(nproc) && \
    make altinstall && \
    ln -sf /usr/local/bin/python3.12 /usr/bin/python && \
    ln -sf /usr/local/bin/pip3.12 /usr/bin/pip && \
    cd / && rm -rf /tmp/Python-3.12.2*

# ---------- app ----------
WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install torch==2.3.0+cu121 torchvision==0.18.0+cu121 torchaudio==2.3.0+cu121 \
        --extra-index-url https://download.pytorch.org/whl/cu121 && \
    pip install -r requirements.txt

COPY src /app

CMD ["python", "main.py"]
