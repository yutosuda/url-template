# URL短縮・クリック数管理ツール

**エンタープライズグレードURL短縮サービス** - 認証機能付きURL短縮とリアルタイムクリック数追跡を提供するモダンなWebアプリケーション

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.4-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue?logo=typescript)](https://www.typescriptlang.org/)
[![Security](https://img.shields.io/badge/Security-JWT%20Auth-green)](https://jwt.io/)

## 🌐 ライブデモ

**本番環境**: [https://url-click-manager.xvps.jp](https://url-click-manager.xvps.jp)

**デフォルト管理者アカウント**:
- **メールアドレス**: `admin@example.com`
- **パスワード**: `admin123`

## 🚀 主要機能

### 🔐 認証・セキュリティ機能
- **🔑 JWT認証**: セキュアなトークンベース認証システム
- **👤 ユーザー管理**: 管理者アカウントによる安全なアクセス制御
- **🛡️ HTTPS通信**: 全通信の暗号化（本番環境）
- **🔒 セッション管理**: 自動ログアウト機能付き

### ✨ URL管理機能
- **🔗 URL短縮**: 長いURLを8文字のランダムコードに変換
- **📊 リアルタイムクリック追跡**: 短縮URLのアクセス数を自動カウント
- **🔄 高速リダイレクト**: 短縮URLから元URLへの瞬時リダイレクト
- **🗑️ URL削除**: 確認ダイアログ付きの安全な削除機能
- **📋 URL一覧管理**: 作成日時・クリック数での視覚的管理

### 📈 分析・統計機能
- **📊 ダッシュボード**: 登録済みURL一覧とクリック数の視覚的表示
- **🕒 JST時刻管理**: 日本標準時での正確な時刻表示
- **📈 統計情報**: 総URL数、総クリック数、人気URLランキング
- **🔍 クリック履歴**: 詳細なアクセスログ（IP、User-Agent、Referrer）

### 🎨 ユーザーエクスペリエンス
- **📱 完全レスポンシブ**: モバイル・タブレット・デスクトップ最適化
- **🎯 直感的UI**: shadcn/ui + Radix UIによるモダンインターフェース
- **⚡ 高速動作**: Next.js + FastAPIによる最適化されたパフォーマンス
- **🔄 リアルタイム更新**: ホットリロード対応の開発環境
- **🌙 アクセシビリティ**: WCAG準拠のユーザビリティ

## 🏗️ 技術アーキテクチャ

### フロントエンド技術スタック
```
Next.js 14.0.4 (React 18.2.0)
├── TypeScript 5.3.2          # 型安全性
├── Tailwind CSS 3.3.6        # ユーティリティファーストCSS
├── shadcn/ui + Radix UI       # モダンUIコンポーネント
├── React Hook Form 7.48.2    # フォーム管理
├── Axios 1.6.2               # HTTP通信
├── Zod 3.22.4                # スキーマ検証
├── Lucide React 0.294.0      # アイコンライブラリ
└── JWT Decode 4.0.0          # JWT トークン処理
```

### バックエンド技術スタック
```
FastAPI 0.104.1 (Python 3.11)
├── SQLAlchemy 2.0.23         # ORM
├── Pydantic 2.5.0            # データ検証
├── Uvicorn 0.24.0            # ASGIサーバー
├── SQLite                    # データベース
├── Alembic 1.13.0            # マイグレーション
├── pytz 2023.3               # タイムゾーン処理
├── python-jose 3.3.0         # JWT処理
├── passlib 1.7.4             # パスワードハッシュ化
├── bcrypt 4.1.2              # セキュアハッシュ
└── pytest 7.4.3              # テストフレームワーク
```

### インフラストラクチャ
```
Docker + Docker Compose + Nginx
├── 開発環境: ホットリロード対応
├── 本番環境: 最適化ビルド + SSL
├── ボリューム永続化: データベース
├── ネットワーク分離: セキュリティ
├── リバースプロキシ: Nginx
└── SSL/TLS: Let's Encrypt
```

## 📋 前提条件

- **Docker**: 20.10.0 以上
- **Docker Compose**: 2.0.0 以上
- **ポート**: 3000（フロントエンド）、8000（バックエンド）が利用可能
- **メモリ**: 最低 2GB RAM 推奨

## 🛠️ クイックスタート

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd url-template
```

### 2. Docker環境の起動

#### 🔄 統合環境（推奨）
```bash
# フロントエンド + バックエンドを同時起動
docker-compose up --build -d

# ログ確認
docker-compose logs -f
```

**重要**: 初回起動時、バックエンドコンテナが自動的に以下を実行します：
1. データベーステーブルの作成
2. 管理者ユーザーの自動作成
3. 必要な初期データの設定

#### 🎯 個別環境起動
```bash
# バックエンドのみ起動
docker-compose -f docker-compose.backend-only.yml up --build -d

# フロントエンドのみ起動
docker-compose -f docker-compose.frontend-only.yml up --build -d

# 本番環境
docker-compose -f docker-compose.production.yml up --build -d
```

### 3. アクセス確認

| サービス | URL | 説明 |
|---------|-----|------|
| **🌐 メインアプリ** | http://localhost:3000 | URL短縮ツール |
| **🔐 ログイン** | http://localhost:3000/login | 認証ページ |
| **🔧 API** | http://localhost:8000 | REST API |
| **📚 API ドキュメント** | http://localhost:8000/docs | Swagger UI |
| **🔍 ReDoc** | http://localhost:8000/redoc | API仕様書 |

### 4. 初回ログイン

1. **アクセス**: http://localhost:3000 をブラウザで開く
2. **ログイン**: 自動的にログインページにリダイレクト
3. **認証情報入力**:
   - メールアドレス: `admin@example.com`
   - パスワード: `admin123`
4. **ログイン完了**: メインダッシュボードにアクセス

## 📖 使用方法

### 🖥️ Web UI（推奨）

#### 基本的な使用フロー
1. **ログイン**: 管理者アカウントでログイン
2. **URL入力**: 「短縮したいURLを入力してください」フィールドに元URLを入力
3. **短縮実行**: 「短縮」ボタンをクリック
4. **URL管理**: 生成された短縮URLをコピーボタンで取得
5. **統計確認**: カード形式でクリック数と作成日時を確認
6. **URL削除**: ゴミ箱アイコンから不要なURLを削除

#### 詳細機能
- **📋 コピー機能**: ワンクリックで短縮URLをクリップボードにコピー
- **📊 リアルタイム更新**: URL作成・削除時の自動リスト更新
- **🔍 視覚的管理**: クリック数の大きな表示とカード形式のレイアウト
- **📱 モバイル対応**: スマートフォンでの最適化されたUI
- **🚪 セキュアログアウト**: 右上のログアウトボタン（モバイルではアイコンのみ）

### 🔧 API直接利用

#### 認証
```bash
# ログイン（JWTトークン取得）
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
```

**レスポンス例:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "created_at": "2025-06-11T09:13:56+09:00"
  }
}
```

#### URL作成（認証必須）
```bash
# JWTトークンを使用してURL作成
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "original_url": "https://www.example.com/very/long/url/path"
  }'
```

**レスポンス例:**
```json
{
  "id": 1,
  "original_url": "https://www.example.com/very/long/url/path",
  "short_code": "AbC123Xy",
  "click_count": 0,
  "created_at": "2025-06-11T14:30:00+09:00",
  "short_url": "https://url-click-manager.xvps.jp/r/AbC123Xy"
}
```

#### その他のAPI操作
```bash
# URL一覧取得（認証必須）
curl -X GET "http://localhost:8000/api/urls?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 統計情報取得（認証必須）
curl -X GET http://localhost:8000/api/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# URL削除（認証必須）
curl -X DELETE http://localhost:8000/api/urls/1 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 短縮URLアクセス（認証不要）
curl -L http://localhost:8000/r/AbC123Xy
```

## 🗂️ プロジェクト構造

```
url-template/
├── 📁 backend/                    # FastAPIバックエンド
│   ├── 📄 main.py                # アプリケーションエントリーポイント
│   ├── 📄 models.py              # SQLAlchemyデータベースモデル
│   ├── 📄 schemas.py             # Pydanticスキーマ定義
│   ├── 📄 crud.py                # CRUD操作ロジック
│   ├── 📄 database.py            # データベース接続設定
│   ├── 📄 config.py              # アプリケーション設定
│   ├── 📄 init_db.py             # データベース初期化スクリプト
│   ├── 📄 start.sh               # コンテナ起動スクリプト
│   ├── 📁 api/                   # APIルート定義
│   │   ├── 📄 auth.py            # 認証エンドポイント
│   │   ├── 📄 urls.py            # URL管理エンドポイント
│   │   ├── 📄 redirect.py        # リダイレクト処理
│   │   ├── 📄 stats.py           # 統計情報エンドポイント
│   │   ├── 📄 health.py          # ヘルスチェック
│   │   ├── 📄 exceptions.py      # 例外処理
│   │   └── 📄 routes.py          # ルート統合
│   ├── 📁 utils/                 # ユーティリティ関数
│   │   ├── 📄 validators.py      # バリデーション
│   │   └── 📄 logging.py         # ログ設定
│   ├── 📁 tests/                 # テストファイル
│   ├── 📁 data/                  # データベースファイル
│   ├── 📄 requirements.txt       # Python依存関係
│   └── 📄 Dockerfile             # バックエンドコンテナ定義
├── 📁 frontend/                   # Next.jsフロントエンド
│   ├── 📁 pages/                 # Next.jsページコンポーネント
│   │   ├── 📄 index.tsx          # メインダッシュボード
│   │   ├── 📄 login.tsx          # ログインページ
│   │   └── 📄 _app.tsx           # アプリケーションルート
│   ├── 📁 components/            # Reactコンポーネント
│   │   ├── 📁 ui/                # shadcn/ui基本コンポーネント
│   │   └── 📄 DeleteConfirmModal.tsx # 削除確認モーダル
│   ├── 📁 lib/                   # ライブラリ・ユーティリティ
│   │   ├── 📄 api.ts             # API通信ロジック
│   │   └── 📄 utils.ts           # ユーティリティ関数
│   ├── 📁 hooks/                 # カスタムReactフック
│   │   ├── 📄 useAuth.ts         # 認証フック
│   │   └── 📄 use-toast.ts       # トースト通知フック
│   ├── 📁 types/                 # TypeScript型定義
│   ├── 📁 styles/                # スタイルファイル
│   ├── 📄 package.json           # Node.js依存関係
│   ├── 📄 Dockerfile             # 本番用コンテナ定義
│   ├── 📄 Dockerfile.dev         # 開発用コンテナ定義
│   ├── 📄 next.config.js         # Next.js設定
│   ├── 📄 tailwind.config.js     # Tailwind CSS設定
│   └── 📄 tsconfig.json          # TypeScript設定
├── 📁 nginx/                      # Nginxリバースプロキシ
│   ├── 📄 nginx.conf             # Nginx設定
│   └── 📁 ssl/                   # SSL証明書
├── 📁 scripts/                    # 運用スクリプト
│   └── 📄 create-admin-on-vps.sh # VPS管理者作成スクリプト
├── 📄 docker-compose.yml         # 統合環境設定
├── 📄 docker-compose.backend-only.yml  # バックエンド専用
├── 📄 docker-compose.frontend-only.yml # フロントエンド専用
├── 📄 docker-compose.production.yml    # 本番環境設定
├── 📄 VPS-DEPLOYMENT-GUIDE.md    # VPS環境デプロイガイド
└── 📄 README.md                  # このファイル
```

## 🔧 開発ガイド

### 📊 ログ確認

```bash
# 全サービスのログをリアルタイム表示
docker-compose logs -f

# 特定サービスのログ
docker-compose logs -f backend
docker-compose logs -f frontend

# 最新20行のログ
docker-compose logs --tail=20 backend

# エラーログのみ抽出
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep ERROR
```

### 🔄 開発モード

両サービスともホットリロード対応：
- **フロントエンド**: ファイル変更時に自動再コンパイル
- **バックエンド**: コード変更時に自動再起動（uvicorn --reload）

### 💾 データベース管理

```bash
# データベースファイルの場所確認
docker-compose exec backend ls -la /app/data/

# データベース内容確認
docker-compose exec backend sqlite3 /app/data/app.db ".tables"
docker-compose exec backend sqlite3 /app/data/app.db "SELECT * FROM urls LIMIT 5;"
docker-compose exec backend sqlite3 /app/data/app.db "SELECT * FROM users;"
docker-compose exec backend sqlite3 /app/data/app.db "SELECT * FROM clicks LIMIT 5;"

# データベース初期化（注意：全データ削除）
docker-compose exec backend python init_db.py
```

### 🧪 テスト実行

```bash
# バックエンドテスト
docker-compose exec backend pytest

# カバレッジ付きテスト
docker-compose exec backend pytest --cov=. --cov-report=html

# フロントエンドテスト
docker-compose exec frontend npm test

# 型チェック
docker-compose exec frontend npm run type-check
```

## 📊 API エンドポイント仕様

### 🔐 認証

| メソッド | エンドポイント | 説明 | パラメータ |
|---------|---------------|------|-----------|
| `POST` | `/api/auth/login` | ログイン | `{"email": "string", "password": "string"}` |
| `POST` | `/api/auth/register` | 新規登録 | `{"email": "string", "password": "string"}` |
| `GET` | `/api/auth/me` | 現在のユーザー情報 | Authorization ヘッダー必須 |

### 🔗 URL管理（認証必須）

| メソッド | エンドポイント | 説明 | パラメータ |
|---------|---------------|------|-----------|
| `POST` | `/api/urls` | URL作成 | `{"original_url": "string"}` |
| `GET` | `/api/urls` | URL一覧取得 | `?skip=0&limit=100` |
| `DELETE` | `/api/urls/{url_id}` | URL削除 | パスパラメータ: `url_id` |
| `GET` | `/api/urls/{url_id}/clicks` | クリック履歴 | パスパラメータ: `url_id` |

### 📈 アクセス・統計

| メソッド | エンドポイント | 説明 | 機能 |
|---------|---------------|------|------|
| `GET` | `/r/{short_code}` | リダイレクト | クリック数カウント + リダイレクト |
| `GET` | `/{short_code}` | リダイレクト（短縮形） | クリック数カウント + リダイレクト |
| `GET` | `/api/stats` | 統計情報 | 総数・ランキング（認証必須） |

### 🔧 システム

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| `GET` | `/` | ヘルスチェック |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc API仕様書 |

## 🔒 セキュリティ機能

### 🛡️ 実装済みセキュリティ対策

- **JWT認証**: セキュアなトークンベース認証
- **パスワードハッシュ化**: bcrypt による強力なハッシュ化
- **HTTPS通信**: 本番環境での全通信暗号化
- **CORS設定**: クロスオリジンリクエスト制御
- **SQLインジェクション対策**: SQLAlchemy ORM使用
- **入力値検証**: Pydantic + Zodによる厳密な検証
- **エラーハンドリング**: 詳細なエラー情報の適切な隠蔽
- **URL検証**: 有効なURL形式のチェック
- **セッション管理**: 自動ログアウト機能

### 🔐 セキュリティ設定例

```python
# JWT設定（backend/config.py）
secret_key: str = "your-secret-key-change-this-in-production"
algorithm: str = "HS256"
access_token_expire_minutes: int = 30

# CORS設定（backend/main.py）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://url-click-manager.xvps.jp"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Accept", "Content-Type", "Authorization"],
)

# パスワードハッシュ化（backend/auth.py）
bcrypt_rounds: int = 12
```

## 🚀 本番環境デプロイ

### 📋 デプロイ前チェックリスト

- [ ] 環境変数の設定（BASE_URL, SECRET_KEY等）
- [ ] データベースの本番用設定
- [ ] SSL証明書の設定
- [ ] リバースプロキシの設定（Nginx）
- [ ] ログ管理の設定
- [ ] バックアップ戦略の策定
- [ ] 管理者アカウントの作成確認

### 🌐 環境変数設定

```bash
# .env ファイル例
DATABASE_URL=sqlite:///./data/app.db
BASE_URL=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
SECRET_KEY=your-production-secret-key-here
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 🔧 本番用Docker設定

```yaml
# docker-compose.production.yml
version: '3.8'
services:
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=sqlite:///./data/app.db
      - BASE_URL=https://yourdomain.com
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    volumes:
      - backend_data:/app/data
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile  # 本番用Dockerfile
    environment:
      - NEXT_PUBLIC_API_URL=https://yourdomain.com/api
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  backend_data:
```

### 🌐 VPS環境デプロイ

詳細なVPS環境でのデプロイ手順については、[VPS-DEPLOYMENT-GUIDE.md](VPS-DEPLOYMENT-GUIDE.md) を参照してください。

**本番環境例**: [https://url-click-manager.xvps.jp](https://url-click-manager.xvps.jp)

## 🧪 テスト・品質保証

### 📊 テストカバレッジ

```bash
# バックエンドテスト実行
docker-compose exec backend pytest --cov=. --cov-report=html

# フロントエンドテスト実行
docker-compose exec frontend npm run test:coverage

# 統合テスト
docker-compose exec backend pytest tests/test_integration.py
```

### 🔍 コード品質チェック

```bash
# Python コード品質
docker-compose exec backend flake8 .
docker-compose exec backend black . --check
docker-compose exec backend mypy .

# TypeScript 型チェック
docker-compose exec frontend npm run type-check
docker-compose exec frontend npm run lint
docker-compose exec frontend npm run lint:fix
```

## 📈 パフォーマンス最適化

### ⚡ 最適化ポイント

1. **データベース**: 
   - インデックス最適化（short_code, created_at）
   - クエリ最適化（ページネーション）
   - 接続プール設定

2. **フロントエンド**: 
   - コード分割（Next.js dynamic imports）
   - 画像最適化（Next.js Image component）
   - CDN活用（静的アセット）

3. **バックエンド**: 
   - 非同期処理（FastAPI async/await）
   - レスポンスキャッシュ
   - データベース接続最適化

4. **インフラ**: 
   - Nginxリバースプロキシ
   - gzip圧縮
   - SSL/TLS最適化

### 📊 監視・メトリクス

```bash
# リソース使用量確認
docker stats

# 個別コンテナのリソース確認
docker-compose exec backend top
docker-compose exec frontend top

# ログ分析
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep WARNING

# データベースサイズ確認
docker-compose exec backend du -sh /app/data/
```

## 🤝 コントリビューション

### 📝 開発フロー

1. **Fork** このリポジトリ
2. **ブランチ作成** (`git checkout -b feature/amazing-feature`)
3. **変更をコミット** (`git commit -m 'Add amazing feature'`)
4. **ブランチにプッシュ** (`git push origin feature/amazing-feature`)
5. **Pull Request作成**

### 📋 コーディング規約

- **Python**: PEP 8準拠、Black フォーマッター使用
- **TypeScript**: ESLint + Prettier設定に従う
- **コミットメッセージ**: Conventional Commits形式
- **テスト**: 新機能には必ずテストを追加

### 🔍 プルリクエストガイドライン

- [ ] テストが全て通過している
- [ ] コードカバレッジが維持されている
- [ ] ドキュメントが更新されている
- [ ] セキュリティチェックが完了している

## 📝 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🆘 トラブルシューティング

### 🔧 よくある問題と解決方法

#### 認証エラー
```bash
# JWTトークンの確認
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"

# 管理者ユーザーの再作成
docker-compose exec backend python init_db.py
```

#### ポート競合エラー
```bash
# ポート使用状況確認
lsof -i :3000
lsof -i :8000

# Docker コンテナ停止
docker-compose down
```

#### データベース接続エラー
```bash
# ボリューム再作成
docker-compose down -v
docker-compose up --build

# データベース初期化
docker-compose exec backend python init_db.py
```

#### フロントエンド ビルドエラー
```bash
# node_modules 再インストール
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install

# キャッシュクリア
docker-compose build --no-cache frontend
```

#### Mixed Content Error（HTTPS環境）
```bash
# 環境変数確認
docker-compose exec frontend env | grep NEXT_PUBLIC_API_URL
docker-compose exec backend env | grep BASE_URL

# 正しい設定例
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
BASE_URL=https://yourdomain.com
```

### 📞 サポート

問題が発生した場合は、以下の情報を含めてIssueを作成してください：

- **OS・環境情報**: `uname -a`, `docker --version`
- **Docker・Docker Composeバージョン**: `docker-compose --version`
- **エラーメッセージ**: 完全なエラーログ
- **再現手順**: 問題を再現するための詳細な手順
- **期待される動作**: 本来期待していた動作
- **実際の動作**: 実際に発生した動作

### 🔍 デバッグモード

```bash
# デバッグログ有効化
docker-compose exec backend python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
"

# フロントエンドデバッグ
docker-compose exec frontend npm run dev -- --debug
```

---

**🎉 URL短縮・クリック数管理ツールをお楽しみください！**

**本番環境**: [https://url-click-manager.xvps.jp](https://url-click-manager.xvps.jp)  
**管理者アカウント**: `admin@example.com` / `admin123` 