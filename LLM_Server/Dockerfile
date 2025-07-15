FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# --- Установка зависимостей ---
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl ca-certificates \
    libopenblas-dev libboost-all-dev \
    libcurl4-openssl-dev \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --- Клонируем llama.cpp ---
WORKDIR /llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git . \
 && mkdir -p build

# --- Сборка с CUDA ---
WORKDIR /llama.cpp/build
RUN cmake .. -DGGML_CUDA=ON && make -j $(nproc)

# --- Установка Python библиотеки ---
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install llama-cpp-python[server] --no-cache-dir

# --- Копируем модель внутрь контейнера ---
COPY ./Model /models

# --- Указываем путь к модели ---
ENV MODEL_PATH=/models/Meta-Llama-3-8B-Instruct.fp16.gguf

# --- Запускаем OpenAI-совместимый сервер ---
EXPOSE 8000
CMD ["python3", "-m", "llama_cpp.server.openai", \
     "--model", "/models/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", "--port", "8000"]
