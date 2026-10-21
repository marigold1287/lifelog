#!/bin/bash
set -e

cd "$(dirname "$0")"

npm --prefix frontend run build

source .venv/bin/activate

exec fastapi run app/main.py --port 8001