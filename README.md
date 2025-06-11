# URL短縮・クリック数管理ツール

**高機能なURL短縮サービス** - URLを短縮してクリック数を追跡・管理できるモダンなWebアプリケーション

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.4-black?logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue?logo=typescript)](https://www.typescriptlang.org/)

## 🚀 主要機能

### ✨ URL管理機能
- **🔗 URL短縮**: 長いURLを短縮URLに変換（8文字のランダムコード生成）
- **📊 クリック数追跡**: 短縮URLのアクセス数をリアルタイム自動カウント
- **🔄 自動リダイレクト**: 短縮URLから元URLへの高速リダイレクト
- **🗑️ URL削除**: 不要なURLの削除機能（確認ダイアログ付き）

### 📈 分析・管理機能
- **📋 管理ダッシュボード**: 登録済みURL一覧とクリック数の視覚的表示
- **🕒 時刻管理**: 日本標準時（JST）での正確な時刻表示

### 🎨 ユーザーエクスペリエンス
- **📱 レスポンシブデザイン**: モバイル・タブレット・デスクトップ対応
- **🎯 直感的UI**: shadcn/ui + Radix UIによるモダンなインターフェース
- **⚡ 高速動作**: Next.js + FastAPIによる最適化されたパフォーマンス
- **🔄 リアルタイム更新**: ホットリロード対応の開発環境

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
└── Lucide React 0.294.0      # アイコンライブラリ
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
└── pytest 7.4.3              # テストフレームワーク
```

### インフラストラクチャ
```
Docker + Docker Compose
├── 開発環境: ホットリロード対応
├── 本番環境: 最適化ビルド
├── ボリューム永続化: データベース
└── ネットワーク分離: セキュリティ
```

## 📋 前提条件

- **Docker**: 20.10.0 以上
- **Docker Compose**: 2.0.0 以上
- **ポート**: 3001（フロントエンド）、8000（バックエンド）が利用可能

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

#### 🎯 個別環境起動
```bash
# バックエンドのみ起動
docker-compose -f docker-compose.backend-only.yml up --build -d

# フロントエンドのみ起動
docker-compose -f docker-compose.frontend-only.yml up --build -d
```

### 3. アクセス確認

| サービス | URL | 説明 |
|---------|-----|------|
| **🌐 フロントエンド** | http://localhost:3001 | メインアプリケーション |
| **🔧 バックエンドAPI** | http://localhost:8000 | REST API |
| **📚 API ドキュメント** | http://localhost:8000/docs | Swagger UI |
| **🔍 ReDoc** | http://localhost:8000/redoc | API仕様書 |

## 📖 使用方法

### 🖥️ Web UI（推奨）

1. **アクセス**: http://localhost:3001 をブラウザで開く
2. **URL入力**: 「短縮したいURLを入力してください」フィールドに元URLを入力
3. **短縮実行**: 「短縮」ボタンをクリック
4. **URL管理**: 生成された短縮URLをコピーボタンで取得
5. **統計確認**: カード形式でクリック数と作成日時を確認
6. **URL削除**: ゴミ箱アイコンから不要なURLを削除

### 🔧 API直接利用

#### URL作成
```bash
curl -X POST http://localhost:8000/api/urls \
  -H "Content-Type: application/json" \
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
  "short_url": "http://localhost:8000/r/AbC123Xy"
}
```

#### URL一覧取得
```bash
curl -X GET "http://localhost:8000/api/urls?skip=0&limit=10"
```

#### 統計情報取得
```bash
curl -X GET http://localhost:8000/api/stats
```

#### URL削除
```bash
curl -X DELETE http://localhost:8000/api/urls/AbC123Xy
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
│   ├── 📁 api/                   # APIルート定義
│   │   └── 📄 routes.py          # エンドポイント実装
│   ├── 📁 utils/                 # ユーティリティ関数
│   ├── 📁 tests/                 # テストファイル
│   ├── 📄 requirements.txt       # Python依存関係
│   └── 📄 Dockerfile             # バックエンドコンテナ定義
├── 📁 frontend/                   # Next.jsフロントエンド
│   ├── 📁 pages/                 # Next.jsページコンポーネント
│   │   ├── 📄 index.tsx          # メインページ
│   │   └── 📄 _app.tsx           # アプリケーションルート
│   ├── 📁 components/            # Reactコンポーネント
│   │   ├── 📁 ui/                # shadcn/ui基本コンポーネント
│   │   └── 📄 DeleteConfirmModal.tsx # 削除確認モーダル
│   ├── 📁 lib/                   # ライブラリ・ユーティリティ
│   │   └── 📄 api.ts             # API通信ロジック
│   ├── 📁 hooks/                 # カスタムReactフック
│   ├── 📁 types/                 # TypeScript型定義
│   ├── 📁 styles/                # スタイルファイル
│   ├── 📄 package.json           # Node.js依存関係
│   ├── 📄 Dockerfile             # 本番用コンテナ定義
│   ├── 📄 Dockerfile.dev         # 開発用コンテナ定義
│   ├── 📄 next.config.js         # Next.js設定
│   ├── 📄 tailwind.config.js     # Tailwind CSS設定
│   └── 📄 tsconfig.json          # TypeScript設定
├── 📄 docker-compose.yml         # 統合環境設定
├── 📄 docker-compose.backend-only.yml  # バックエンド専用
├── 📄 docker-compose.frontend-only.yml # フロントエンド専用
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
```

### 🔄 開発モード

両サービスともホットリロード対応：
- **フロントエンド**: ファイル変更時に自動再コンパイル
- **バックエンド**: コード変更時に自動再起動（uvicorn --reload）

### 💾 データベース管理

```bash
# データベースファイルの場所
docker-compose exec backend ls -la /app/data/

# データベース内容確認
docker-compose exec backend sqlite3 /app/data/app.db ".tables"
docker-compose exec backend sqlite3 /app/data/app.db "SELECT * FROM urls LIMIT 5;"
```

### 🧪 テスト実行

```bash
# バックエンドテスト
docker-compose exec backend pytest

# フロントエンドテスト
docker-compose exec frontend npm test

# 型チェック
docker-compose exec frontend npm run type-check
```

## 📊 API エンドポイント仕様

### 🔗 URL管理

| メソッド | エンドポイント | 説明 | パラメータ |
|---------|---------------|------|-----------|
| `POST` | `/api/urls` | URL作成 | `{"original_url": "string"}` |
| `GET` | `/api/urls` | URL一覧取得 | `?skip=0&limit=100` |
| `GET` | `/api/urls/{short_code}` | 個別URL情報 | パスパラメータ: `short_code` |
| `DELETE` | `/api/urls/{short_code}` | URL削除 | パスパラメータ: `short_code` |

### 📈 アクセス・統計

| メソッド | エンドポイント | 説明 | 機能 |
|---------|---------------|------|------|
| `GET` | `/r/{short_code}` | リダイレクト | クリック数カウント + リダイレクト |
| `GET` | `/api/urls/{short_code}/clicks` | クリック履歴 | アクセスログ詳細 |
| `GET` | `/api/stats` | 統計情報 | 総数・ランキング |

### 🔧 システム

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| `GET` | `/` | ヘルスチェック |
| `GET` | `/docs` | Swagger UI |
| `GET` | `/redoc` | ReDoc API仕様書 |

## 🔒 セキュリティ機能

### 🛡️ 実装済みセキュリティ対策

- **CORS設定**: クロスオリジンリクエスト制御
- **SQLインジェクション対策**: SQLAlchemy ORM使用
- **入力値検証**: Pydantic + Zodによる厳密な検証
- **エラーハンドリング**: 詳細なエラー情報の適切な隠蔽
- **URL検証**: 有効なURL形式のチェック
- **レート制限**: 過度なリクエストの制御（実装可能）

### 🔐 セキュリティ設定例

```python
# CORS設定（backend/main.py）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

## 🚀 本番環境デプロイ

### 📋 デプロイ前チェックリスト

- [ ] 環境変数の設定
- [ ] データベースの本番用設定
- [ ] SSL証明書の設定
- [ ] リバースプロキシの設定
- [ ] ログ管理の設定
- [ ] バックアップ戦略の策定

### 🌐 環境変数設定

```bash
# .env ファイル例
DATABASE_URL=postgresql://user:password@localhost/urlshortener
BASE_URL=https://yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 🔧 本番用Docker設定

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BASE_URL=${BASE_URL}
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile  # 本番用Dockerfile
    environment:
      - NEXT_PUBLIC_API_URL=${BASE_URL}
    restart: unless-stopped
```

## 🧪 テスト・品質保証

### 📊 テストカバレッジ

```bash
# バックエンドテスト実行
docker-compose exec backend pytest --cov=. --cov-report=html

# フロントエンドテスト実行
docker-compose exec frontend npm run test:coverage
```

### 🔍 コード品質チェック

```bash
# Python コード品質
docker-compose exec backend flake8 .
docker-compose exec backend black . --check

# TypeScript 型チェック
docker-compose exec frontend npm run type-check
docker-compose exec frontend npm run lint
```

## 📈 パフォーマンス最適化

### ⚡ 最適化ポイント

1. **データベース**: インデックス最適化、クエリ最適化
2. **フロントエンド**: コード分割、画像最適化、CDN活用
3. **バックエンド**: 非同期処理、キャッシュ戦略
4. **インフラ**: ロードバランサー、オートスケーリング

### 📊 監視・メトリクス

```bash
# リソース使用量確認
docker-compose exec backend top
docker-compose exec frontend top

# ログ分析
docker-compose logs backend | grep ERROR
docker-compose logs frontend | grep WARNING
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

## 📝 ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 🆘 トラブルシューティング

### 🔧 よくある問題と解決方法

#### ポート競合エラー
```bash
# ポート使用状況確認
lsof -i :3001
lsof -i :8000

# Docker コンテナ停止
docker-compose down
```

#### データベース接続エラー
```bash
# ボリューム再作成
docker-compose down -v
docker-compose up --build
```

#### フロントエンド ビルドエラー
```bash
# node_modules 再インストール
docker-compose exec frontend rm -rf node_modules
docker-compose exec frontend npm install
```

### 📞 サポート

問題が発生した場合は、以下の情報を含めてIssueを作成してください：

- OS・環境情報
- Docker・Docker Composeバージョン
- エラーメッセージ
- 再現手順

---

**🎉 URL短縮・クリック数管理ツールをお楽しみください！** 