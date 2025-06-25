#!/bin/bash

# データベース初期化
echo "Initializing database..."
python init_db.py

# FastAPIサーバー起動
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload 