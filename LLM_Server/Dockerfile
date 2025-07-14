FROM ghcr.io/ggerganov/llama.cpp:latest

# Копируем модель внутрь контейнера
COPY ./Model /Model

# Запускаем сервер с поддержкой OpenAI API
CMD ["./server", \
     "-m", "/Model/Meta-Llama-3-8B-Instruct.fp16.gguf", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--api", \
     "-ngl", "99"]