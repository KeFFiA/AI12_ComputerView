#!/bin/bash

set -e

MODEL_PATH="${MODEL_PATH:-/models/Meta-Llama-3-8B-Instruct.fp16.gguf}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
N_GPU_LAYERS="${N_GPU_LAYERS:-100}"
N_CTX="${N_CTX:-4096}"

echo "Starting llama-server:"
echo "  Модель: $MODEL_PATH"
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  GPU layers: $N_GPU_LAYERS"
echo "  Context size: $N_CTX"

ls
ls /models

exec /llama.cpp/build/bin/llama-server \
    --model "$MODEL_PATH" \
    --n_gpu_layers "$N_GPU_LAYERS" \
    --n_ctx "$N_CTX" \
    --host "$HOST" \
    --port "$PORT"
