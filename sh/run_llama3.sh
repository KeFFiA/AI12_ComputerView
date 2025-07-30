#!/bin/bash
BASE_DIR=$(dirname "$(realpath "$0")")

docker run -d --rm \
  --gpus=all \
  --name llama3-api \
  -p 8000:8000 \
  -v "$BASE_DIR/LLM_Server/Model":/models \
  -v "$BASE_DIR/Medical/data/input_pdfs_claims":/app/data/input_pdfs_claims \
  -e MODEL_PATH=/models/Meta-Llama-3-8B-Instruct.fp16.gguf \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  -e THREADS=32 \
  -e THREADS_BATCH=16 \
  -e BATCH_SIZE=4096 \
  -e N_GPU_LAYERS=100 \
  asg_llama3:latest

echo "llama3-api started"
