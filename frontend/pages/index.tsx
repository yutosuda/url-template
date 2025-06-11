import { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Copy, ExternalLink, Trash2 } from 'lucide-react';
import { urlApi, URLData, URLCreateRequest } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Toaster } from '@/components/ui/toaster';
import { DeleteConfirmModal } from '@/components/DeleteConfirmModal';

export default function Home() {
  const [url, setUrl] = useState('');
  const [urls, setUrls] = useState<URLData[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [deleteModal, setDeleteModal] = useState<{
    isOpen: boolean;
    urlData: URLData | null;
    isDeleting: boolean;
  }>({
    isOpen: false,
    urlData: null,
    isDeleting: false,
  });
  const { toast } = useToast();

  // URL一覧を取得
  const fetchUrls = useCallback(async () => {
    try {
      setLoading(true);
      const response = await urlApi.getUrls();
      setUrls(response.urls);
    } catch (error) {
      console.error('Error fetching URLs:', error);
      toast({
        title: "エラー",
        description: "URL一覧の取得に失敗しました",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  // 初回読み込み
  useEffect(() => {
    fetchUrls();
  }, [fetchUrls]);

  // URL短縮処理
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    try {
      setSubmitting(true);
      await urlApi.createUrl({ original_url: url });
      setUrl('');
      await fetchUrls(); // 一覧を更新
      toast({
        title: "成功",
        description: "URLが短縮されました",
      });
    } catch (error) {
      console.error('Error creating URL:', error);
      toast({
        title: "エラー",
        description: error instanceof Error ? error.message : "URL短縮に失敗しました",
        variant: "destructive",
      });
    } finally {
      setSubmitting(false);
    }
  };

  // URLをクリップボードにコピー
  const copyToClipboard = async (shortUrl: string) => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      toast({
        title: "コピー完了",
        description: "URLをコピーしました！",
      });
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      toast({
        title: "エラー",
        description: "コピーに失敗しました",
        variant: "destructive",
      });
    }
  };

  // 削除モーダルを開く
  const openDeleteModal = (urlData: URLData) => {
    setDeleteModal({
      isOpen: true,
      urlData,
      isDeleting: false,
    });
  };

  // 削除モーダルを閉じる
  const closeDeleteModal = () => {
    if (deleteModal.isDeleting) return; // 削除中は閉じられない
    setDeleteModal({
      isOpen: false,
      urlData: null,
      isDeleting: false,
    });
  };

  // URL削除処理
  const handleDeleteConfirm = async () => {
    if (!deleteModal.urlData) return;

    try {
      setDeleteModal(prev => ({ ...prev, isDeleting: true }));
      await urlApi.deleteUrl(deleteModal.urlData.short_code);
      await fetchUrls(); // 一覧を更新
      toast({
        title: "削除完了",
        description: "URLが削除されました",
      });
      closeDeleteModal();
    } catch (error) {
      console.error('Error deleting URL:', error);
      toast({
        title: "エラー",
        description: "削除に失敗しました",
        variant: "destructive",
      });
      setDeleteModal(prev => ({ ...prev, isDeleting: false }));
    }
  };

  // 日付フォーマット
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-zinc-50">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-zinc-900 mb-2">URL短縮ツール</h1>
          <p className="text-zinc-600">長いURLを短く、管理しやすくします</p>
        </div>

        {/* URL入力フォーム */}
        <div className="mb-8">
          <form onSubmit={handleSubmit} className="flex gap-3 max-w-2xl mx-auto">
            <Input
              type="url"
              placeholder="短縮したいURLを入力してください"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1 h-9"
              required
            />
            <Button 
              type="submit" 
              disabled={submitting || !url.trim()}
              className="h-9 px-6"
            >
              {submitting ? '処理中...' : '短縮'}
            </Button>
          </form>
        </div>

        {/* URL一覧 */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-zinc-900">短縮URL一覧</h2>
          
          {loading ? (
            <div className="text-center py-8">
              <p className="text-zinc-500">読み込み中...</p>
            </div>
          ) : urls.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-zinc-500">まだURLが登録されていません</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {urls.map((urlData) => (
                <Card key={urlData.id} className="hover:shadow-md transition-shadow duration-200">
                  <CardContent className="p-4">
                    {/* クリック数 - 大きく表示 */}
                    <div className="text-center mb-3">
                      <div className="text-4xl font-bold text-zinc-900">
                        {urlData.click_count.toLocaleString()}
                      </div>
                      <div className="text-sm text-zinc-500">クリック</div>
                    </div>

                    {/* 元URL - 小さく表示 */}
                    <div className="mb-4">
                      <div className="text-xs text-zinc-500 truncate" title={urlData.original_url}>
                        {urlData.original_url}
                      </div>
                    </div>

                    {/* 作成日時 */}
                    <div className="text-xs text-zinc-400 mb-4 text-center">
                      {formatDate(urlData.created_at)}
                    </div>

                    {/* アクションボタン */}
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        className="flex-1"
                        onClick={() => copyToClipboard(urlData.short_url)}
                      >
                        <Copy className="h-3 w-3 mr-1" />
                        コピー
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(urlData.short_url, '_blank')}
                      >
                        <ExternalLink className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => openDeleteModal(urlData)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 削除確認モーダル */}
      {deleteModal.urlData && (
        <DeleteConfirmModal
          isOpen={deleteModal.isOpen}
          onClose={closeDeleteModal}
          onConfirm={handleDeleteConfirm}
          shortCode={deleteModal.urlData.short_code}
          originalUrl={deleteModal.urlData.original_url}
          isDeleting={deleteModal.isDeleting}
        />
      )}

      <Toaster />
    </div>
  );
} 