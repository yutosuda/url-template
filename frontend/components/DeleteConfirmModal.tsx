import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { AlertTriangle } from 'lucide-react';

interface DeleteConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  shortCode: string;
  originalUrl: string;
  isDeleting?: boolean;
}

export function DeleteConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  shortCode,
  originalUrl,
  isDeleting = false,
}: DeleteConfirmModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-red-100">
              <AlertTriangle className="h-5 w-5 text-red-600" />
            </div>
            <div>
              <DialogTitle className="text-lg font-semibold">
                URLを削除しますか？
              </DialogTitle>
              <DialogDescription className="text-sm text-zinc-600 mt-1">
                この操作は取り消すことができません。
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="py-4">
          <div className="space-y-3">
            <div>
              <div className="text-sm font-medium text-zinc-700 mb-1">短縮コード</div>
              <div className="text-sm font-mono bg-zinc-100 px-3 py-2 rounded-md">
                {shortCode}
              </div>
            </div>
            <div>
              <div className="text-sm font-medium text-zinc-700 mb-1">元URL</div>
              <div className="text-sm text-zinc-600 bg-zinc-50 px-3 py-2 rounded-md break-all">
                {originalUrl}
              </div>
            </div>
          </div>
        </div>

        <DialogFooter className="flex gap-2 sm:gap-2">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isDeleting}
            className="flex-1"
          >
            キャンセル
          </Button>
          <Button
            variant="destructive"
            onClick={onConfirm}
            disabled={isDeleting}
            className="flex-1"
          >
            {isDeleting ? '削除中...' : '削除する'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
} 