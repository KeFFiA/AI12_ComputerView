FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_LIB_DIR=/usr/local/cuda/lib64/stubs
ENV LD_LIBRARY_PATH=${CUDA_LIB_DIR}:${LD_LIBRARY_PATH}
ENV LIBRARY_PATH=${CUDA_LIB_DIR}:${LIBRARY_PATH}

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl ca-certificates \
    libopenblas-dev libboost-all-dev \
    libcurl4-openssl-dev \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Прокладываем символическую ссылку на libcuda
RUN ln -s ${CUDA_LIB_DIR}/libcuda.so /usr/lib/libcuda.so || true && \
    ln -s ${CUDA_LIB_DIR}/libcuda.so /usr/lib/libcuda.so.1 || true

# Клонируем llama.cpp и собираем с поддержкой CUDA
WORKDIR /llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git . && mkdir build

WORKDIR /llama.cpp/build
RUN cmake .. -DGGML_CUDA=ON -DLLAMA_CURL=OFF && make -j $(nproc)

# Установка Python-зависимостей
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install llama-cpp-python[server] --no-cache-dir

# Пробрасываем модель
COPY ./Model /models
ENV MODEL_PATH=/models/Meta-Llama-3-8B-Instruct.fp16.gguf

# Открываем порт API и запускаем сервер совместимый с OpenAI
EXPOSE 8000
CMD ["/llama.cpp/build/bin/llama-server", \
     "--model", "/models/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--n_gpu_layers", "100", \
     "--n_ctx_size", "4096", \
     "--host", "0.0.0.0", "--port", "8000"]