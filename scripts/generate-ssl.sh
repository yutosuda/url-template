#!/bin/bash

# 自己署名SSL証明書生成スクリプト
# VPS初期設定用（後でLet's Encryptに置き換え推奨）

set -e

SSL_DIR="./nginx/ssl"
DOMAIN=${1:-"localhost"}

echo "🔐 自己署名SSL証明書を生成しています..."
echo "ドメイン: $DOMAIN"

# SSL証明書ディレクトリの作成
mkdir -p "$SSL_DIR"

# 自己署名証明書の生成
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$SSL_DIR/selfsigned.key" \
    -out "$SSL_DIR/selfsigned.crt" \
    -subj "/C=JP/ST=Tokyo/L=Tokyo/O=URL-Template/OU=IT/CN=$DOMAIN"

# 権限設定
chmod 600 "$SSL_DIR/selfsigned.key"
chmod 644 "$SSL_DIR/selfsigned.crt"

echo "✅ SSL証明書が生成されました:"
echo "   証明書: $SSL_DIR/selfsigned.crt"
echo "   秘密鍵: $SSL_DIR/selfsigned.key"
echo ""
echo "⚠️  注意: これは自己署名証明書です。本番環境では Let's Encrypt を使用してください。"
echo ""
echo "Let's Encrypt証明書の取得方法:"
echo "1. Cerbot をインストール"
echo "2. 以下のコマンドを実行:"
echo "   certbot certonly --webroot -w /var/www/html -d $DOMAIN"
echo "3. nginx.conf の SSL設定を更新" 