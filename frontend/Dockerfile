FROM node:20-alpine

# タイムゾーンパッケージをインストール
RUN apk add --no-cache tzdata

WORKDIR /app

# パッケージファイルをコピー（package-lock.jsonも含める）
COPY package.json package-lock.json ./

# 依存関係をインストール（npm ciを使用してより高速で確実なインストール）
RUN npm ci --only=production

# アプリケーションコードをコピー
COPY . .

# Next.jsのビルド（本番環境用）
RUN npm run build

# ポート3000を公開
EXPOSE 3000

# 本番サーバーを起動
CMD ["npm", "start"] 