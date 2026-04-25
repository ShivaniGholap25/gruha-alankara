import { useState, useEffect } from 'react';

let toastIdCounter = 0;

const toastQueue = [];
let toastListener = null;

export function showToast(message, type = 'success', duration = 2500) {
  const id = ++toastIdCounter;
  const toast = { id, message, type, duration };
  toastQueue.push(toast);
  if (toastListener) toastListener([...toastQueue]);
  setTimeout(() => {
    const idx = toastQueue.findIndex((t) => t.id === id);
    if (idx !== -1) toastQueue.splice(idx, 1);
    if (toastListener) toastListener([...toastQueue]);
  }, duration);
}

export default function Toast() {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    toastListener = setToasts;
    return () => { toastListener = null; };
  }, []);

  if (!toasts.length) return null;

  const bgMap = {
    success: { bg: '#10b981', color: '#052e16' },
    error: { bg: '#ef4444', color: '#fee2e2' },
    info: { bg: '#3b82f6', color: '#eff6ff' },
    warning: { bg: '#f59e0b', color: '#451a03' },
  };

  return (
    <div style={{ position: 'fixed', bottom: 18, right: 18, zIndex: 2000, display: 'flex', flexDirection: 'column', gap: 8 }}>
      {toasts.map((t) => {
        const colors = bgMap[t.type] || bgMap.success;
        return (
          <div key={t.id} style={{
            background: colors.bg,
            color: colors.color,
            padding: '0.75rem 1.2rem',
            borderRadius: 10,
            fontWeight: 700,
            fontSize: '0.9rem',
            boxShadow: '0 4px 20px rgba(0,0,0,0.3)',
            animation: 'fadeIn 0.3s ease-out',
          }}>
            {t.message}
          </div>
        );
      })}
    </div>
  );
}
