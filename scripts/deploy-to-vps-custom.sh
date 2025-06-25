#!/bin/bash

# VPS固有デプロイスクリプト
# X server VPS (85.131.250.117) 専用

set -e

# VPS固有設定
VPS_HOST="85.131.250.117"
VPS_USER="root"
VPS_PORT="22"
DOMAIN="url-click-manager.xvps.jp"
PROJECT_NAME="url-template"
SSH_KEY="$HOME/.ssh/vps_key"

# 色付きログ関数
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

log_info "=== X server VPS デプロイメント開始 ==="
log_info "VPS Host: $VPS_HOST"
log_info "Domain: $DOMAIN"

# SSH接続テスト
log_info "SSH接続をテストしています..."
if ! ssh -i "$SSH_KEY" -p "$VPS_PORT" -o ConnectTimeout=10 -o BatchMode=yes "$VPS_USER@$VPS_HOST" exit 2>/dev/null; then
    log_error "SSH接続に失敗しました"
    exit 1
fi
log_success "SSH接続成功"

# プロジェクトファイルの圧縮
log_info "プロジェクトファイルを圧縮しています..."
tar -czf "/tmp/${PROJECT_NAME}.tar.gz" \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='backend/venv' \
    --exclude='backend/__pycache__' \
    --exclude='frontend/.next' \
    --exclude='*.log' \
    .

# VPSでの環境準備
log_info "VPS環境を準備しています..."
ssh -i "$SSH_KEY" -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << 'EOF'
    # システム更新
    apt-get update && apt-get upgrade -y
    
    # Docker & Docker Composeインストール
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl enable docker
        systemctl start docker
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # 必要なツールのインストール
    apt-get install -y curl wget git htop ufw fail2ban
    
    # ファイアウォール設定
    ufw --force enable
    ufw allow ssh
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # プロジェクトディレクトリ作成
    mkdir -p /opt/url-template
    cd /opt/url-template
EOF

log_success "VPS環境準備完了"

# ファイル転送
log_info "プロジェクトファイルをVPSに転送しています..."
scp -i "$SSH_KEY" -P "$VPS_PORT" "/tmp/${PROJECT_NAME}.tar.gz" "$VPS_USER@$VPS_HOST:/opt/url-template/"

# VPSでのデプロイ実行
log_info "VPSでアプリケーションをデプロイしています..."
ssh -i "$SSH_KEY" -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << EOF
    cd /opt/url-template
    
    # 既存のコンテナを停止・削除
    if [ -f docker-compose.production.yml ]; then
        docker-compose -f docker-compose.production.yml down || true
    fi
    
    # ファイル展開
    tar -xzf ${PROJECT_NAME}.tar.gz
    rm ${PROJECT_NAME}.tar.gz
    
    # 本番環境でビルド・起動
    docker-compose -f docker-compose.production.yml build --no-cache
    docker-compose -f docker-compose.production.yml up -d
    
    # ヘルスチェック
    sleep 30
    docker-compose -f docker-compose.production.yml ps
    
    # サービス状態確認
    echo "=== サービス状態 ==="
    docker-compose -f docker-compose.production.yml logs --tail=20
EOF

# 後処理
rm "/tmp/${PROJECT_NAME}.tar.gz"

log_success "=== デプロイメント完了 ==="
log_info "アクセス情報:"
echo "  🌐 Webサイト: https://$DOMAIN"
echo "  📚 API ドキュメント: https://$DOMAIN/docs"
echo "  🔍 ReDoc: https://$DOMAIN/redoc"
echo ""
log_warning "注意事項:"
echo "  1. 自己署名証明書を使用しているため、ブラウザで警告が表示されます"
echo "  2. 本番環境では Let's Encrypt 証明書の使用を推奨します"
echo ""
log_info "Let's Encrypt証明書取得コマンド:"
echo "  ssh -i $SSH_KEY $VPS_USER@$VPS_HOST 'cd /opt/url-template && ./scripts/setup-letsencrypt.sh $DOMAIN admin@$DOMAIN'" 