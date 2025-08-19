FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_LIB_DIR=/usr/local/cuda/lib64/stubs
ENV LD_LIBRARY_PATH=${CUDA_LIB_DIR}:${LD_LIBRARY_PATH}
ENV LIBRARY_PATH=${CUDA_LIB_DIR}:${LIBRARY_PATH}

RUN apt-get update && apt-get install -y \
    git cmake build-essential curl bash wget unzip ca-certificates \
    libopenblas-dev libboost-all-dev \
    libcurl4-openssl-dev \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN ln -s ${CUDA_LIB_DIR}/libcuda.so /usr/lib/libcuda.so || true && \
    ln -s ${CUDA_LIB_DIR}/libcuda.so /usr/lib/libcuda.so.1 || true

RUN curl -fsSL https://ollama.com/install.sh | bash

EXPOSE 11434

CMD ["ollama", "serve"]
