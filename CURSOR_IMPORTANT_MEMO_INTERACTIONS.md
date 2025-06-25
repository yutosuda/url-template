# Cursor 重要なインタラクション記録

## 2025-06-25: URL 短縮問題の分析と解決

### 問題の概要

- 特定の URL（`https://www.niigata-ogawaya.co.jp/`）が短縮できない問題が発生
- バックエンド API では正常に動作するが、フロントエンドで失敗

### 根本原因

- **HTML の`<input type="url">`要素のブラウザネイティブ検証**が原因
- 日本語ドメイン名や国際化ドメイン名（IDN）に対してブラウザごとに異なる検証結果
- 特に日本語地名を含むドメイン名で問題が発生しやすい

### 技術的詳細

1. **問題の URL**: `https://www.niigata-ogawaya.co.jp/`
2. **バックエンド**: 正常動作（Pydantic HttpUrl 検証通過）
3. **フロントエンド**: `type="url"`のブラウザ検証で阻止

### 実装した解決策

#### 1. Input 要素の修正

```typescript
// 修正前
<Input type="url" ... />

// 修正後
<Input
  type="text"
  pattern="https?://.*"
  title="http://またはhttps://で始まる有効なURLを入力してください"
  ...
/>
```

#### 2. フォームに noValidate 属性追加

```typescript
<form onSubmit={handleSubmit} className="..." noValidate>
```

#### 3. クライアントサイド URL 検証の強化

```typescript
// 基本的なURL形式チェック
if (!trimmedUrl.match(/^https?:\/\/.+/i)) {
  // エラー処理
}

// JavaScript URL コンストラクタによる検証
try {
  new URL(trimmedUrl);
} catch (urlError) {
  // エラー処理
}
```

#### 4. API クライアントのログ強化

- URL 作成時の詳細ログ追加
- エラー時の詳細情報記録

### 学習事項

1. **ブラウザネイティブ検証の制限**: `type="url"`は国際化ドメインに対して完全ではない
2. **カスタム検証の重要性**: より柔軟で正確な検証のために JavaScript による検証が必要
3. **段階的デバッグ**: バックエンドとフロントエンドを分離してテストすることの重要性

### 今後の対応

- 他の国際化ドメインでのテストを実施
- ユーザビリティ向上のためのエラーメッセージ改善
- より包括的な URL 検証パターンの検討

### 関連ファイル

- `frontend/pages/index.tsx`: メインの修正
- `frontend/lib/api.ts`: ログ強化
- `backend/api/urls.py`: 参考（正常動作確認済み）
