#!/bin/bash
BASE_DIR=$(dirname "$(realpath "$0")")

docker run -d --rm \
  --gpus all \
  --name claims_pdf_parser \
  -v "$BASE_DIR/data":/app/data \
  -v "$BASE_DIR/output":/app/output \
  -v "$BASE_DIR/transformers_cache":/app/.cache \
  -e PYTHONUNBUFFERED=1 \
  -e CUDA_VISIBLE_DEVICES=all \
  asg_computerview_claims_parser:latest

echo "claims_pdf_parser started"
