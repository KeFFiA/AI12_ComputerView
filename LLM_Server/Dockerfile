FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential \
    curl libcurl4-openssl-dev \
    python3 python3-pip \
    apt-utils

# Клонирование и сборка llama.cpp с поддержкой CUDA
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp && \
    cd /llama.cpp && \
    cmake -B build -DGGML_CUDA=on . && \
    cmake --build build -j && \
    ln -s /llama.cpp/build/bin/server /usr/local/bin/llama-server

# Копирование модели внутрь контейнера
COPY ./Model /Model

# Запуск LLaMA сервера с OpenAI-совместимым API
CMD ["llama-server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api", \
     "-ngl", "99"]
