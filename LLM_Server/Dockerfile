FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential \
    curl libcurl4-openssl-dev \
    python3 python3-pip \
    wget pkg-config libprotobuf-dev protobuf-compiler \
    libopenblas-dev libomp-dev

# Указываем переменные окружения для CUDA
ENV CUDAToolkit_ROOT=/usr/local/cuda
ENV PATH=$CUDAToolkit_ROOT/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDAToolkit_ROOT/lib64:$LD_LIBRARY_PATH

# Клонирование и сборка llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp && \
    cd /llama.cpp && \
    cmake -B build -DGGML_CUDA=on -DCMAKE_CUDA_ARCHITECTURES="all" . && \
    cmake --build build -j && \
    ln -s /llama.cpp/build/bin/server /usr/local/bin/llama-server

# Копируем модель внутрь контейнера
COPY ./Model /Model

# Запуск OpenAI-совместимого сервера
CMD ["llama-server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api", \
     "-ngl", "99"]
