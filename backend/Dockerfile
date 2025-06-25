FROM python:3.11-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# データディレクトリを作成
RUN mkdir -p /app/data

# 初期化スクリプトを実行可能にする
RUN chmod +x init_db.py

# ポート8000を公開
EXPOSE 8000

# 起動スクリプトを作成
RUN echo '#!/bin/bash\n\
echo "=== アプリケーション起動準備 ==="\n\
python3 init_db.py\n\
echo "=== FastAPIサーバー起動 ==="\n\
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload\n\
' > /app/start.sh && chmod +x /app/start.sh

# 起動スクリプトを実行
CMD ["/app/start.sh"] 