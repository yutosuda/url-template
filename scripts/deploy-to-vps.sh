#!/bin/bash

# VPSデプロイ自動化スクリプト
# X server VPS環境への安全なデプロイメント

set -e

# 設定変数
VPS_HOST=${1:-""}
VPS_USER=${2:-"root"}
VPS_PORT=${3:-"22"}
DOMAIN=${4:-""}
PROJECT_NAME="url-template"

# 色付きログ関数
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

# 使用方法表示
show_usage() {
    echo "使用方法: $0 <VPS_HOST> [VPS_USER] [VPS_PORT] [DOMAIN]"
    echo ""
    echo "例:"
    echo "  $0 192.168.1.100 root 22 example.com"
    echo "  $0 your-vps.com ubuntu 2222 your-domain.com"
    echo ""
    echo "パラメータ:"
    echo "  VPS_HOST  : VPSのIPアドレスまたはホスト名 (必須)"
    echo "  VPS_USER  : SSH接続ユーザー名 (デフォルト: root)"
    echo "  VPS_PORT  : SSHポート番号 (デフォルト: 22)"
    echo "  DOMAIN    : SSL証明書用ドメイン名 (デフォルト: VPS_HOST)"
    exit 1
}

# パラメータチェック
if [ -z "$VPS_HOST" ]; then
    log_error "VPSホストが指定されていません"
    show_usage
fi

if [ -z "$DOMAIN" ]; then
    DOMAIN="$VPS_HOST"
fi

log_info "=== VPSデプロイメント開始 ==="
log_info "VPS Host: $VPS_HOST"
log_info "VPS User: $VPS_USER"
log_info "VPS Port: $VPS_PORT"
log_info "Domain: $DOMAIN"

# SSH接続テスト
log_info "SSH接続をテストしています..."
if ! ssh -p "$VPS_PORT" -o ConnectTimeout=10 -o BatchMode=yes "$VPS_USER@$VPS_HOST" exit 2>/dev/null; then
    log_error "SSH接続に失敗しました。以下を確認してください:"
    echo "  1. VPSのIPアドレス/ホスト名が正しいか"
    echo "  2. SSHキーが設定されているか"
    echo "  3. ファイアウォールでSSHポートが開いているか"
    exit 1
fi
log_success "SSH接続成功"

# ローカルでの事前準備
log_info "ローカル環境での事前準備を実行しています..."

# SSL証明書生成
if [ ! -f "./nginx/ssl/selfsigned.crt" ]; then
    log_info "SSL証明書を生成しています..."
    ./scripts/generate-ssl.sh "$DOMAIN"
fi

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
ssh -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << 'EOF'
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
scp -P "$VPS_PORT" "/tmp/${PROJECT_NAME}.tar.gz" "$VPS_USER@$VPS_HOST:/opt/url-template/"

# VPSでのデプロイ実行
log_info "VPSでアプリケーションをデプロイしています..."
ssh -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << EOF
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
echo "  3. ドメイン名を使用する場合は、DNSレコードの設定が必要です"
echo ""
log_info "ログ確認コマンド:"
echo "  ssh -p $VPS_PORT $VPS_USER@$VPS_HOST 'cd /opt/url-template && docker-compose -f docker-compose.production.yml logs -f'" 