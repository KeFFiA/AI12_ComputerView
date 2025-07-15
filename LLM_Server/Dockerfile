FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl libcurl4-openssl-dev \
    python3 python3-pip wget pkg-config libprotobuf-dev protobuf-compiler \
    libopenblas-dev libomp-dev && \
    rm -rf /var/lib/apt/lists/*

# CUDA окружение
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

# Клонируем llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git /llama.cpp

# Сборка llama_api_server
WORKDIR /llama.cpp
RUN cmake -S . -B build \
    -DLLAMA_CUBLAS=on \
    -DLLAMA_BUILD_SERVER=on && \
    cmake --build build --target llama_api_server -j

# Копируем модель
COPY ./Model /Model

# Открываем порт
EXPOSE 8000

# Запуск REST-сервера
CMD ["/llama.cpp/build/bin/llama_api_server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api-key", "llama"]
