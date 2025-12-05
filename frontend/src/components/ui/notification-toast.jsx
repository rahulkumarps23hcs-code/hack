import { AnimatePresence, motion } from 'framer-motion';
import { CheckCircle2, Info, XCircle, AlertTriangle, X } from 'lucide-react';
import Button from './button.jsx';
import { cn } from '../../utils/cn.js';

function getIcon(variant) {
  switch (variant) {
    case 'success':
      return <CheckCircle2 className="h-4 w-4 text-green-500" />;
    case 'error':
      return <XCircle className="h-4 w-4 text-red-500" />;
    case 'warning':
      return <AlertTriangle className="h-4 w-4 text-amber-500" />;
    default:
      return <Info className="h-4 w-4 text-blue-500" />;
  }
}

function NotificationToast({ toasts, onDismiss }) {
  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-3 z-50 flex flex-col items-center gap-2 sm:items-end sm:px-4">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            className={cn(
              'pointer-events-auto w-full max-w-xs rounded-xl border border-slate-200/80 bg-slate-950/95 px-3 py-2.5 text-xs text-slate-50 shadow-soft sm:max-w-sm',
              'dark:border-slate-700/80'
            )}
            initial={{ opacity: 0, y: 16, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.97 }}
            transition={{ duration: 0.22, ease: 'easeOut' }}
          >
            <div className="flex items-start gap-3">
              <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-slate-900">
                {getIcon(toast.variant)}
              </div>
              <div className="flex-1">
                {toast.title && (
                  <p className="text-xs font-semibold text-slate-50">{toast.title}</p>
                )}
                {toast.description && (
                  <p className="mt-1 text-[11px] text-slate-300">{toast.description}</p>
                )}
              </div>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-6 w-6 rounded-full p-0 text-slate-400 hover:bg-slate-800 hover:text-slate-100"
                onClick={() => onDismiss(toast.id)}
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}

export { NotificationToast };
