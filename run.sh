#!/bin/bash
set -e

cd "$(dirname "$0")"

source .venv/bin/activate

fastapi dev --port 8001 &
BACKEND_PID=$!
trap "kill $BACKEND_PID" EXIT

# バックエンドが立ち上がるまで待つ
until curl -s -o /dev/null http://127.0.0.1:8001/docs; do
  sleep 0.5
done

cd frontend
npm run dev