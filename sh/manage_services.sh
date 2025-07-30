#!/bin/bash
BASE_DIR=$(dirname "$(realpath "$0")")

function start() {
  case "$2" in
    medical)
      bash "$BASE_DIR/run_medical_parser.sh"
      ;;
    claims)
      bash "$BASE_DIR/run_claims_parser.sh"
      ;;
    llama3)
      bash "$BASE_DIR/run_llama3.sh"
      ;;
    all)
      bash "$BASE_DIR/run_services.sh"
      ;;
    *)
      echo "Usage: $0 start {medical|claims|llama3|all}"
      ;;
  esac
}

function stop() {
  case "$2" in
    medical)
      docker stop medical_pdf_parser
      ;;
    claims)
      docker stop claims_pdf_parser
      ;;
    llama3)
      docker stop llama3-api
      ;;
    all)
      echo "Stopping all services..."
      docker stop medical_pdf_parser claims_pdf_parser llama3-api
      ;;
    *)
      echo "Usage: $0 stop {medical|claims|llama3|all}"
      ;;
  esac
}

function status() {
  echo "Containers status:"
  docker ps --filter "name=medical_pdf_parser" --filter "name=claims_pdf_parser" --filter "name=llama3-api"
}

function logs() {
  case "$2" in
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
      echo "Tailing logs for all containers. Use Ctrl+C to stop."
      docker logs -f medical_pdf_parser &
      docker logs -f claims_pdf_parser &
      docker logs -f llama3-api &
      wait
      ;;
    *)
      echo "Usage: $0 logs {medical|claims|llama3|all}"
      ;;
  esac
}

case "$1" in
  start)
    start "$@"
    ;;
  stop)
    stop "$@"
    ;;
  status)
    status
    ;;
  logs)
    logs "$@"
    ;;
  *)
    echo "Usage: $0 {start|stop|status|logs}"
    ;;
esac
