FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Системные зависимости
RUN apt-get update && \
    apt-get install -y git build-essential cmake curl python3 python3-pip

# Сборка llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp /llama.cpp && \
    cd /llama.cpp && \
    cmake -B build -DLLAMA_CUBLAS=on . && \
    cmake --build build -j && \
    ln -s /llama.cpp/build/bin/server /usr/local/bin/llama-server

# Копируем модель
COPY ./models /models

# Запускаем сервер
CMD ["llama-server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api", \
     "-ngl", "99"]
