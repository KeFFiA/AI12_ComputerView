FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential \
    curl libcurl4-openssl-dev \
    python3 python3-pip \
    wget pkg-config libprotobuf-dev protobuf-compiler \
    libopenblas-dev libomp-dev \ apt-utils

# Установка символических ссылок для libcuda
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/libcuda.so && \
    ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/libcuda.so.1

# Клонирование и сборка llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp && \
    cd /llama.cpp && \
    cmake -B build -DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES=all . && \
    cmake --build build -j && \
    ln -s /llama.cpp/build/bin/server /usr/local/bin/llama-server

# Копируем модель
COPY ./Model /Model

# Запускаем API-сервер
CMD ["llama-server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api", \
     "-ngl", "99"]
