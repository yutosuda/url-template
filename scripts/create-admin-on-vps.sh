#!/bin/bash

# VPS環境での管理者ユーザー作成スクリプト
# Docker環境で動作中のバックエンドコンテナ内で管理者ユーザーを作成します

set -e

# 色付きログ関数
log_info() { echo -e "\033[1;34m[INFO]\033[0m $1"; }
log_success() { echo -e "\033[1;32m[SUCCESS]\033[0m $1"; }
log_warning() { echo -e "\033[1;33m[WARNING]\033[0m $1"; }
log_error() { echo -e "\033[1;31m[ERROR]\033[0m $1"; }

VPS_HOST=${1:-""}
VPS_USER=${2:-"root"}
VPS_PORT=${3:-"22"}

# 使用方法表示
show_usage() {
    echo "使用方法: $0 <VPS_HOST> [VPS_USER] [VPS_PORT]"
    echo ""
    echo "例:"
    echo "  $0 192.168.1.100"
    echo "  $0 your-vps.com root 22"
    echo ""
    echo "パラメータ:"
    echo "  VPS_HOST  : VPSのIPアドレスまたはホスト名 (必須)"
    echo "  VPS_USER  : SSH接続ユーザー名 (デフォルト: root)"
    echo "  VPS_PORT  : SSHポート番号 (デフォルト: 22)"
    exit 1
}

# パラメータチェック
if [ -z "$VPS_HOST" ]; then
    log_error "VPSホストが指定されていません"
    show_usage
fi

log_info "=== VPS環境での管理者ユーザー作成開始 ==="
log_info "VPS Host: $VPS_HOST"
log_info "VPS User: $VPS_USER"
log_info "VPS Port: $VPS_PORT"

# SSH接続テスト（パスワード認証）
log_info "SSH接続をテストしています..."
log_warning "パスワード認証が必要です。VPSのrootパスワードを入力してください。"

# 接続テスト（パスワード認証）
if ! ssh -p "$VPS_PORT" -o ConnectTimeout=10 "$VPS_USER@$VPS_HOST" "echo 'SSH connection successful'" 2>/dev/null; then
    log_error "SSH接続に失敗しました。以下を確認してください:"
    echo "  1. VPSのIPアドレス/ホスト名が正しいか"
    echo "  2. rootパスワードが正しいか"
    echo "  3. ファイアウォールでSSHポートが開いているか"
    exit 1
fi
log_success "SSH接続成功"

# VPS上でDockerコンテナの状態確認
log_info "Dockerコンテナの状態を確認しています..."
ssh -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << 'EOF'
cd /opt/url-template
echo "=== Docker Compose サービス状態 ==="
docker-compose -f docker-compose.production.yml ps
echo ""
echo "=== バックエンドコンテナログ（最新10行） ==="
docker-compose -f docker-compose.production.yml logs --tail=10 backend
EOF

# 管理者ユーザー作成
log_info "管理者ユーザーを作成しています..."
ssh -p "$VPS_PORT" "$VPS_USER@$VPS_HOST" << 'EOF'
cd /opt/url-template
echo "=== 管理者ユーザー作成実行 ==="
docker-compose -f docker-compose.production.yml exec -T backend python3 init_db.py
echo ""
echo "=== データベース内容確認 ==="
docker-compose -f docker-compose.production.yml exec -T backend python3 -c "
import sqlite3
conn = sqlite3.connect('/app/data/app.db')
cursor = conn.cursor()
cursor.execute('SELECT id, email, created_at FROM users')
users = cursor.fetchall()
print('登録済みユーザー:')
for user in users:
    print(f'  ID: {user[0]}, Email: {user[1]}, Created: {user[2]}')
conn.close()
"
EOF

log_success "管理者ユーザー作成完了"
log_info "ログイン情報:"
log_info "  メールアドレス: admin@example.com"
log_info "  パスワード: admin123"
log_info ""
log_info "ブラウザで https://$VPS_HOST にアクセスしてログインしてください。" 