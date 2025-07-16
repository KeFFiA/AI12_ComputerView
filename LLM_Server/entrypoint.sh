#!/bin/bash

set -e

MODEL_PATH="${MODEL_PATH:-/models/Meta-Llama-3-8B-Instruct.fp16.gguf}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
N_GPU_LAYERS="${N_GPU_LAYERS:-999}"
N_CTX="${N_CTX:-8192}"
THREADS="${THREADS:-16}"
THREADS_BATCH="${THREADS_BATCH:-8}"
BATCH_SIZE="${BATCH_SIZE:-1024}"
UBATCH_SIZE="${UBATCH_SIZE:-1024}"


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

exec /llama.cpp/build/bin/llama-server \
    --model "$MODEL_PATH" \
    --gpu-layers "$N_GPU_LAYERS" \
    --threads "$THREADS" \
    --threads-batch "$THREADS_BATCH" \
    --flash-attn \
    --mlock \
    --batch-size "$BATCH_SIZE"\
    --ubatch-size "$UBATCH_SIZE"\
    --ctx-size "$N_CTX" \
    --host "$HOST" \
    --port "$PORT"
