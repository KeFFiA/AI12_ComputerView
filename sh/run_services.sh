#!/bin/bash

BASE_DIR=$(pwd)

echo "Starting all services..."
echo " "

echo "Starting medical_parser..."
bash "$BASE_DIR/run_medical_parser.sh"

echo "Starting claims_parser..."
bash "$BASE_DIR/run_claims_parser.sh"

echo "Starting llama3-api..."
bash "$BASE_DIR/run_llama3.sh"

echo "All services started."
