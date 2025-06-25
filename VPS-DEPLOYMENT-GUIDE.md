# 🚀 VPSデプロイメントガイド

**X server VPS環境への完全デプロイメント手順**

このガイドでは、URL短縮ツールをX serverのVPS環境に安全かつ効率的にデプロイする方法を説明します。

## 📋 前提条件

### VPS要件
- **OS**: Ubuntu 20.04 LTS 以上 (推奨)
- **RAM**: 最低 2GB (推奨 4GB以上)
- **ストレージ**: 最低 20GB (推奨 50GB以上)
- **ネットワーク**: 固定IPアドレス

### ローカル環境要件
- **SSH**: SSH鍵認証が設定済み
- **Docker**: Docker & Docker Compose がインストール済み
- **Git**: プロジェクトのクローンが完了済み

## 🔧 デプロイメント手順

### 1. SSH鍵の設定

VPSにSSH鍵でアクセスできるように設定してください：

```bash
# SSH鍵生成（まだない場合）
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"

# 公開鍵をVPSにコピー
ssh-copy-id -p 22 root@YOUR_VPS_IP
```

### 2. 自動デプロイスクリプトの実行

**基本的なデプロイ（IPアドレスのみ）:**
```bash
./scripts/deploy-to-vps.sh YOUR_VPS_IP
```

**完全なデプロイ（カスタムユーザー・ポート・ドメイン）:**
```bash
./scripts/deploy-to-vps.sh YOUR_VPS_IP ubuntu 2222 your-domain.com
```

**パラメータ説明:**
- `YOUR_VPS_IP`: VPSのIPアドレスまたはホスト名
- `ubuntu`: SSH接続ユーザー名（デフォルト: root）
- `2222`: SSHポート番号（デフォルト: 22）
- `your-domain.com`: SSL証明書用ドメイン名（オプション）

### 3. デプロイ完了後の確認

デプロイが完了すると、以下のURLでアクセス可能になります：

| サービス | URL | 説明 |
|---------|-----|------|
| **🌐 メインサイト** | `https://YOUR_DOMAIN` | URL短縮ツール |
| **📚 API ドキュメント** | `https://YOUR_DOMAIN/docs` | Swagger UI |
| **🔍 ReDoc** | `https://YOUR_DOMAIN/redoc` | API仕様書 |
| **💓 ヘルスチェック** | `https://YOUR_DOMAIN/health` | サービス状態 |

## 🔒 SSL証明書の設定

### 自己署名証明書（初期設定）

デプロイスクリプトは自動的に自己署名証明書を生成します。ブラウザで警告が表示されますが、機能的には問題ありません。

### Let's Encrypt証明書（推奨）

本番環境では無料のLet's Encrypt証明書を使用することを強く推奨します：

```bash
# VPSにSSH接続
ssh -p 22 root@YOUR_VPS_IP

# Let's Encrypt証明書取得
cd /opt/url-template
./scripts/setup-letsencrypt.sh your-domain.com admin@your-domain.com
```

**注意**: ドメイン名を使用する場合は、事前にDNSレコードを設定してください。

## 🔧 運用・管理コマンド

### 管理者ユーザー作成（初回デプロイ後）
```bash
# ローカルから実行（推奨）
./scripts/create-admin-on-vps.sh YOUR_VPS_IP

# または、VPSに直接SSH接続して実行
ssh root@YOUR_VPS_IP
cd /opt/url-template
docker-compose -f docker-compose.production.yml exec backend python3 init_db.py
```

**デフォルト管理者アカウント:**
- メールアドレス: `admin@example.com`
- パスワード: `admin123`

### サービス状態確認
```bash
# VPSにSSH接続後
cd /opt/url-template
docker-compose -f docker-compose.production.yml ps
```

### ログ確認
```bash
# 全サービスのログ
docker-compose -f docker-compose.production.yml logs -f

# 特定サービスのログ
docker-compose -f docker-compose.production.yml logs -f backend
docker-compose -f docker-compose.production.yml logs -f frontend
docker-compose -f docker-compose.production.yml logs -f nginx
```

### サービス再起動
```bash
# 全サービス再起動
docker-compose -f docker-compose.production.yml restart

# 特定サービス再起動
docker-compose -f docker-compose.production.yml restart backend
```

### アップデート
```bash
# 新しいコードをデプロイ
./scripts/deploy-to-vps.sh YOUR_VPS_IP

# または手動でアップデート
ssh root@YOUR_VPS_IP
cd /opt/url-template
git pull origin main
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

## 🛡️ セキュリティ設定

デプロイスクリプトは以下のセキュリティ設定を自動的に適用します：

### ファイアウォール (UFW)
- SSH (22/tcp)
- HTTP (80/tcp)
- HTTPS (443/tcp)

### Fail2Ban
- SSH攻撃の自動ブロック

### Nginx セキュリティヘッダー
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security (HSTS)

### レート制限
- API: 10リクエスト/秒
- 一般: 30リクエスト/秒

## 📊 監視・メトリクス

### システムリソース監視
```bash
# CPU・メモリ使用量
htop

# ディスク使用量
df -h

# Docker統計
docker stats
```

### アプリケーション監視
```bash
# ヘルスチェック
curl -f https://YOUR_DOMAIN/health

# API統計
curl https://YOUR_DOMAIN/api/stats
```

## 🔄 バックアップ・復旧

### データベースバックアップ
```bash
# SQLiteデータベースのバックアップ
docker-compose -f docker-compose.production.yml exec backend cp /app/data/app.db /app/data/app.db.backup.$(date +%Y%m%d_%H%M%S)

# バックアップファイルをローカルにダウンロード
scp root@YOUR_VPS_IP:/opt/url-template/backend/data/app.db.backup.* ./backups/
```

### 設定ファイルバックアップ
```bash
# 重要な設定ファイルをバックアップ
tar -czf config-backup-$(date +%Y%m%d).tar.gz \
    docker-compose.production.yml \
    nginx/nginx.conf \
    nginx/ssl/
```

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. SSH接続エラー
```bash
# SSH設定確認
ssh -v -p 22 root@YOUR_VPS_IP

# 鍵の権限確認
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

#### 2. Docker起動エラー
```bash
# Dockerサービス状態確認
systemctl status docker

# Dockerサービス再起動
systemctl restart docker
```

#### 3. SSL証明書エラー
```bash
# 証明書の有効性確認
openssl x509 -in /opt/url-template/nginx/ssl/cert.pem -text -noout

# Let's Encrypt証明書の更新
certbot renew --dry-run
```

#### 4. ポート競合エラー
```bash
# ポート使用状況確認
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# 競合するプロセスの停止
sudo systemctl stop apache2  # Apacheが動いている場合
```

### ログレベル設定

デバッグが必要な場合は、ログレベルを変更できます：

```bash
# docker-compose.production.yml の environment セクションを編集
environment:
  - LOG_LEVEL=DEBUG  # INFO から DEBUG に変更
```

## 📞 サポート・連絡先

問題が発生した場合は、以下の情報を含めてお問い合わせください：

1. **エラーメッセージ**: 完全なエラーログ
2. **環境情報**: OS、Docker バージョン
3. **実行コマンド**: 実行したコマンドの履歴
4. **システム状態**: `docker-compose ps` の出力

---

## 🎉 デプロイ完了！

おめでとうございます！URL短縮ツールがVPS環境で正常に動作しています。

**次のステップ:**
1. ✅ SSL証明書の設定（Let's Encrypt推奨）
2. ✅ ドメイン名の設定（DNSレコード）
3. ✅ 定期バックアップの設定
4. ✅ 監視システムの導入

**アクセス情報:**
- 🌐 **Webサイト**: `https://YOUR_DOMAIN`
- 📚 **API ドキュメント**: `https://YOUR_DOMAIN/docs`
- 🔍 **ReDoc**: `https://YOUR_DOMAIN/redoc` 