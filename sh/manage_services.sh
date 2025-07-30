#!/bin/bash
BASE_DIR=$(dirname "$(realpath "$0")")

function start_all() {
  echo "Starting all services..."
  bash "$BASE_DIR/run_medical_parser.sh"
  bash "$BASE_DIR/run_claims_parser.sh"
  bash "$BASE_DIR/run_llama3.sh"
}

function stop_all() {
  echo "Stopping all services..."
  docker stop medical_pdf_parser claims_pdf_parser llama3-api
}

function status() {
  echo "Containers status:"
  docker ps --filter "name=medical_pdf_parser" --filter "name=claims_pdf_parser" --filter "name=llama3-api"
}

function logs() {
  case "$1" in
    medical)
      bash "$BASE_DIR/logs_medical_parser.sh"
      ;;
    claims)
      bash "$BASE_DIR/logs_claims_parser.sh"
      ;;
    llama3)
      bash "$BASE_DIR/logs_llama3.sh"
      ;;
    all)
      bash "$BASE_DIR/logs_llama3.sh"
      ;;
    *)
      echo "Using: $0 logs {medical|claims|llama3|all}"
      ;;
  esac
}

case "$1" in
  start)
    start_all
    ;;
  stop)
    stop_all
    ;;
  status)
    status
    ;;
  logs)
    logs "$2"
    ;;
  *)
    echo "Using: $0 {start|stop|status|logs}"
    ;;
esac
