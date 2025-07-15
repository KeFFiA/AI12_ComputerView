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

# Символические ссылки на libcuda
RUN ln -s ${CUDA_LIB_DIR}/libcuda.so /usr/lib/libcuda.so || true && \
    ln -s ${CUDA_LIB_DIR}/libcuda.so.1 /usr/lib/libcuda.so.1 || true

# Клонируем и собираем llama.cpp
WORKDIR /llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git . && mkdir build

WORKDIR /llama.cpp/build
RUN cmake .. -DGGML_CUDA=ON -DLLAMA_CURL=OFF && make -j $(nproc)

# Установка Python-зависимостей
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install llama-cpp-python[server] --no-cache-dir

# Копируем универсальный entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Указываем volume для моделей
VOLUME ["/models"]

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
