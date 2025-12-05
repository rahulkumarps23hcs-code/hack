import { createContext, useCallback, useContext, useState } from 'react';
import { NotificationToast } from '../components/ui/notification-toast.jsx';

const ToastContext = createContext(undefined);

let idCounter = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const addToast = useCallback((toast) => {
    idCounter += 1;
    const id = `toast-${idCounter}`;
    const next = { id, ...toast };
    setToasts((prev) => [...prev, next]);
    if (!toast.persist) {
      window.setTimeout(() => {
        removeToast(id);
      }, toast.duration ?? 3500);
    }
  }, [removeToast]);

  return (
    <ToastContext.Provider value={{ addToast, removeToast }}>
      {children}
      <NotificationToast toasts={toasts} onDismiss={removeToast} />
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within ToastProvider');
  }
  return context;
}
