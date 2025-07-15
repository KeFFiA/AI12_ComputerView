# Используем CUDA с Ubuntu 22.04
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl libcurl4-openssl-dev \
    python3 python3-pip wget pkg-config libprotobuf-dev protobuf-compiler \
    libopenblas-dev libomp-dev

# Симлинки для stub libcuda (для сборки)
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/libcuda.so && \
    ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/lib/libcuda.so.1

# CUDA переменные окружения
ENV CUDAToolkit_ROOT=/usr/local/cuda
ENV PATH=$CUDAToolkit_ROOT/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDAToolkit_ROOT/lib64:$LD_LIBRARY_PATH

# Клонируем llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp

# Сборка с включением API-сервера
WORKDIR /llama.cpp
RUN cmake -B build -DLLAMA_API=ON -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=86 . && \
    cmake --build build -j

# Копируем модель внутрь контейнера
COPY ./Model /Model

# expose порт API
EXPOSE 8000

# Запуск llama_api_server с ключом API "llama"
CMD ["/llama.cpp/build/llama_api_server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api-key", "llama"]
