#!/bin/bash

# Let's Encrypt SSL証明書自動取得・更新スクリプト
# VPS上で実行してください

set -e

DOMAIN=${1:-""}
EMAIL=${2:-""}

# 色付きログ関数
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# 使用方法表示
show_usage() {
    echo "使用方法: $0 <DOMAIN> <EMAIL>"
    echo ""
    echo "例:"
    echo "  $0 example.com admin@example.com"
    echo ""
    echo "パラメータ:"
    echo "  DOMAIN : SSL証明書を取得するドメイン名 (必須)"
    echo "  EMAIL  : Let's Encryptアカウント用メールアドレス (必須)"
    exit 1
}

# パラメータチェック
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
    log_error "ドメイン名とメールアドレスが必要です"
    show_usage
fi

log_info "=== Let's Encrypt SSL証明書取得開始 ==="
log_info "Domain: $DOMAIN"
log_info "Email: $EMAIL"

# Certbotインストール
log_info "Certbotをインストールしています..."
if ! command -v certbot &> /dev/null; then
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# 一時的にNginxを停止
log_info "一時的にNginxコンテナを停止しています..."
cd /opt/url-template
docker-compose -f docker-compose.production.yml stop nginx

# Let's Encrypt証明書取得
log_info "Let's Encrypt証明書を取得しています..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email "$EMAIL" \
    -d "$DOMAIN"

# 証明書をNginxディレクトリにコピー
log_info "証明書をNginxディレクトリにコピーしています..."
mkdir -p ./nginx/ssl
cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" "./nginx/ssl/cert.pem"
cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" "./nginx/ssl/key.pem"

# nginx.confを更新（Let's Encrypt証明書を使用）
log_info "Nginx設定を更新しています..."
sed -i 's|ssl_certificate /etc/nginx/ssl/selfsigned.crt;|ssl_certificate /etc/nginx/ssl/cert.pem;|g' ./nginx/nginx.conf
sed -i 's|ssl_certificate_key /etc/nginx/ssl/selfsigned.key;|ssl_certificate_key /etc/nginx/ssl/key.pem;|g' ./nginx/nginx.conf

# 自己署名証明書の設定をコメントアウト
sed -i 's|ssl_certificate /etc/nginx/ssl/selfsigned|# ssl_certificate /etc/nginx/ssl/selfsigned|g' ./nginx/nginx.conf

# Nginxコンテナを再起動
log_info "Nginxコンテナを再起動しています..."
docker-compose -f docker-compose.production.yml up -d --force-recreate nginx

# 証明書自動更新の設定
log_info "証明書自動更新を設定しています..."
cat > /etc/cron.d/certbot-renew << EOF
# Let's Encrypt証明書自動更新
0 12 * * * root certbot renew --quiet --post-hook "cd /opt/url-template && cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ./nginx/ssl/cert.pem && cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ./nginx/ssl/key.pem && docker-compose -f docker-compose.production.yml restart nginx"
EOF

log_success "=== Let's Encrypt SSL証明書設定完了 ==="
log_info "証明書情報:"
certbot certificates

log_info "アクセス確認:"
echo "  🌐 Webサイト: https://$DOMAIN"
echo "  📚 API ドキュメント: https://$DOMAIN/docs"

log_success "SSL証明書は自動的に更新されます（毎日12:00に確認）" 