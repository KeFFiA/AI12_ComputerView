FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# --- Установка зависимостей ---
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl ca-certificates \
    libopenblas-dev libboost-all-dev \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --- Клонируем llama.cpp ---
WORKDIR /llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git . \
 && mkdir -p build

# --- Сборка с поддержкой CUDA и сервера ---
WORKDIR /llama.cpp/build
RUN cmake .. \
    -DLLAMA_BUILD_SERVER=ON \
    -DGGML_CUDA=ON \
 && make -j $(nproc)

# --- Копируем модель ---
COPY ./Model /models

ENV MODEL_PATH=/models/Meta-Llama-3-8B-Instruct.fp16.gguf

# --- Запуск llama-server ---
EXPOSE 8000
CMD ["/llama.cpp/build/bin/llama-server", \
     "-m", "/models/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api-key", "llama"]
