#!/bin/bash

set -e

MODEL_PATH="${MODEL_PATH:-/models/Meta-Llama-3-8B-Instruct.fp16.gguf}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
N_GPU_LAYERS="${N_GPU_LAYERS:-100}"
N_CTX="${N_CTX:-4096}"

echo "== STARTING LLAMA SERVER ==" >&1
echo "  Модель: $MODEL_PATH" >&1
echo "  Host: $HOST" >&1
echo "  Port: $PORT" >&1
echo "  GPU layers: $N_GPU_LAYERS" >&1
echo "  Context size: $N_CTX" >&1

echo "== Contents of current dir: ==" >&1
ls -la >&1
echo "== Contents of /models: ==" >&1
ls -la /models >&1

/llama.cpp/build/bin/llama-server \
    --model "$MODEL_PATH" \
    --n_gpu_layers "$N_GPU_LAYERS" \
    --n_ctx "$N_CTX" \
    --host "$HOST" \
    --port "$PORT"
