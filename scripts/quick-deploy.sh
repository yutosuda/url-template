#!/bin/bash

# クイックデプロイスクリプト
# 使用方法: ./scripts/quick-deploy.sh VPS_IP

set -e

VPS_IP=${1:-""}

if [ -z "$VPS_IP" ]; then
    echo "❌ エラー: VPSのIPアドレスを指定してください"
    echo "使用方法: $0 <VPS_IP>"
    echo "例: $0 192.168.1.100"
    exit 1
fi

echo "🚀 クイックデプロイを開始します..."
echo "VPS IP: $VPS_IP"

# デプロイスクリプトを実行
./scripts/deploy-to-vps.sh "$VPS_IP"

echo ""
echo "✅ デプロイ完了！"
echo "🌐 アクセス: https://$VPS_IP"
echo "📚 API ドキュメント: https://$VPS_IP/docs" 