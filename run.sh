#!/bin/bash
set -e

cd "$(dirname "$0")"

source .venv/bin/activate

# 終了時にプロセスグループ全体を落とす（trapの再発動を防ぐため最初に解除）
trap 'trap - EXIT INT TERM; kill 0' EXIT INT TERM

fastapi dev --port 8002 &

# バックエンドが立ち上がるまで待つ
until curl -s -o /dev/null http://127.0.0.1:8002/docs; do
  sleep 0.5
done

npm --prefix frontend run dev