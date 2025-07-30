#!/bin/bash

BASE_DIR=$(pwd)

echo "Starting medical_parser..."
docker run -d --rm \
  --gpus all \
  --name medical_pdf_parser \
  -v "$BASE_DIR/data":/app/data \
  -v "$BASE_DIR/output":/app/output \
  -v "$BASE_DIR/transformers_cache":/app/.cache \
  -e PYTHONUNBUFFERED=1 \
  -e CUDA_VISIBLE_DEVICES=all \
  asg_computerview_medical_parser:latest

echo "Starting claims_parser..."
docker run -d --rm \
  --gpus all \
  --name claims_pdf_parser \
  -v "$BASE_DIR/data":/app/data \
  -v "$BASE_DIR/output":/app/output \
  -v "$BASE_DIR/transformers_cache":/app/.cache \
  -e PYTHONUNBUFFERED=1 \
  -e CUDA_VISIBLE_DEVICES=all \
  asg_computerview_claims_parser:latest

echo "Starting llama3-api..."
docker run -d --rm \
  --gpus all \
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

echo "All services started."
