#!/bin/bash

MODEL_PATH="${MODEL_PATH:-/models/Meta-Llama-3-8B-Instruct.fp16.gguf}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
N_CTX="${N_CTX:-4096}"
N_GPU_LAYERS="${N_GPU_LAYERS:-100}"

echo "🚀 Start llama-server:"
echo "  MODEL_PATH:     $MODEL_PATH"
echo "  HOST:           $HOST"
echo "  PORT:           $PORT"
echo "  N_CTX:          $N_CTX"
echo "  N_GPU_LAYERS:   $N_GPU_LAYERS"

exec /llama.cpp/build/bin/llama-server \
    --model "$MODEL_PATH" \
    --n_gpu_layers "$N_GPU_LAYERS" \
    --n_ctx "$N_CTX" \
    --host "$HOST" \
    --port "$PORT"
