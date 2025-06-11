# URLクリック数管理ツール 開発設計書

---

## 1. **プロジェクト概要**

### 1.1. 目的
- ユーザーがURLを登録すると短縮URLが発行される。
- 発行された短縮URLにアクセスがあるたびに、元URLへリダイレクトし、クリック数を記録する。
- 管理画面で登録済みURL・クリック数を一覧・集計できる。
- バックエンドはPython（FastAPI）、フロントエンドはNext.js＋shadcn/ui。
- 開発・テストはDockerによるローカル環境で完結させる。

### 1.2. 想定ユーザー
- 一般ユーザー（URL短縮・管理）
- 管理者（全URL・統計管理）

### 1.3. 開発・運用体制
- 開発：ローカルDocker環境
- 本番：VPS等への移行を前提

---

## 2. **システム全体構成**

### 2.1. アーキテクチャ図

```
┌────────────┐   ┌────────────┐   ┌────────────┐
│ Frontend   │   │ Backend    │   │ Database   │
│ (Next.js)  │←→│ (FastAPI)  │←→│ (SQLite)   │
└────────────┘   └────────────┘   └────────────┘
      ↑                ↑
   Docker           Docker
   Container        Container
```

### 2.2. サービス構成

- **frontend**: Next.js + shadcn/ui
- **backend**: FastAPI + SQLAlchemy + SQLite
- **database**: SQLite（ファイル永続化、将来的にMySQL/PostgreSQLへ拡張可能）

---

## 3. **ディレクトリ・ファイル構成**

```
url-click-manager/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── pages/
│   ├── components/
│   ├── lib/
│   └── styles/
├── docker-compose.yml
├── backend/Dockerfile
└── frontend/Dockerfile
```

---

## 4. **Dockerによる開発環境設計**

### 4.1. docker-compose.yml（例）

```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - TZ=Asia/Tokyo
  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    environment:
      - TZ=Asia/Tokyo
    depends_on:
      - backend
```

### 4.2. backend/Dockerfile

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 4.3. frontend/Dockerfile

```Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]
```

---

## 5. **バックエンド設計（FastAPI）**

### 5.1. データベース設計

#### 5.1.1. テーブル：urls

| カラム名      | 型           | 説明                         |
|---------------|--------------|------------------------------|
| id            | INTEGER      | 主キー、自動採番             |
| original_url  | TEXT         | 元のURL                      |
| short_code    | VARCHAR(16)  | 短縮コード、一意制約         |
| click_count   | INTEGER      | クリック数                   |
| created_at    | DATETIME     | 登録日時                     |

#### 5.1.2. テーブル：clicks

| カラム名      | 型           | 説明                         |
|---------------|--------------|------------------------------|
| id            | INTEGER      | 主キー、自動採番             |
| url_id        | INTEGER      | urlsテーブルへの外部キー      |
| clicked_at    | DATETIME     | クリック日時                 |
| user_agent    | TEXT         | アクセス元UserAgent          |
| ip_address    | VARCHAR(45)  | アクセス元IP                 |
| referrer      | TEXT         | リファラ                     |

### 5.2. API設計

| メソッド | パス                  | 概要                              |
|----------|-----------------------|-----------------------------------|
| POST     | /api/urls             | URL登録・短縮URL発行              |
| GET      | /api/urls             | 登録済みURL一覧取得               |
| GET      | /r/{short_code}       | リダイレクト＆クリック記録        |
| GET      | /api/urls/{short_code}| 個別URL情報取得                   |

### 5.3. 主な処理フロー

- **URL登録**  
  1. original_urlを受け取る
  2. short_codeをランダム生成（重複チェック）
  3. DBに保存
  4. 短縮URLを返却

- **リダイレクト**  
  1. short_codeでDB検索
  2. 存在すればclick_countをインクリメント
  3. clicksテーブルにアクセス情報を記録
  4. original_urlへリダイレクト

- **一覧取得**  
  1. urlsテーブルから全件取得
  2. 必要に応じてページング

### 5.4. バリデーション・セキュリティ

- original_urlの形式チェック
- SQLインジェクション防止（ORM利用）
- CORS設定（localhost:3000許可）
- エラーハンドリング（404, 400, 500等）

---

## 6. **フロントエンド設計（Next.js + shadcn/ui）**

### 6.1. 画面構成

- **トップページ**
  - URL登録フォーム
  - 登録済みURL一覧（短縮URL、元URL、クリック数表示）
- **管理画面（任意）**
  - 詳細なクリック履歴表示

### 6.2. 主なコンポーネント

- URL登録フォーム（Input, Button）
- URL一覧テーブル（Table）
- クリック数表示
- 通知・エラーメッセージ表示

### 6.3. API通信

- fetch/axiosでバックエンドAPIと連携
- POST/GETリクエストの実装
- エラー時のハンドリング

### 6.4. UI/UX設計

- shadcn/uiで統一感のあるデザイン
- レスポンシブ対応
- 入力値バリデーション
- 操作フィードバック（ローディング、成功/失敗通知）

---

## 7. **開発・テストフロー**

### 7.1. 起動手順

1. リポジトリclone
2. `docker compose up --build`
3. フロントエンド：`http://localhost:3000`  
   バックエンド：`http://localhost:8000`

### 7.2. テスト

- バックエンド：pytest等で単体・APIテスト
- フロントエンド：Jest/React Testing Library等で単体テスト
- E2Eテスト：Cypress/Playwright等（任意）

### 7.3. データ永続化

- SQLite DBファイルをホストにマウント（必要に応じて）

---

## 8. **運用・拡張設計（将来のための備考）**

- 本番移行時はMySQL/PostgreSQL等へのDB切替も容易
- Dockerにより本番・開発環境の差異を最小化
- 機能拡張例：ユーザー認証、APIキー、URL有効期限、詳細な分析機能

---

## 9. **セキュリティ・品質管理**

- CORS制御
- SQLインジェクション/XSS対策
- エラーハンドリング・ログ出力
- Linter/Formatter導入（Black, Prettier等）
- GitHub Actions等によるCI/CD（自動テスト）

---

## 10. **ドキュメント・進捗管理**

- GitHub Issue/Projectsでタスク・進捗管理
- API仕様書（OpenAPI/Swagger）
- 画面遷移図・ER図・シーケンス図（必要に応じて）

---

## 11. **備考・参考**

- Dockerfileやdocker-compose.ymlのサンプルは本設計書内に記載
- 詳細なコーディング規約やテスト仕様は別途ドキュメント化

---