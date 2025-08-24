import { useState, useCallback } from 'react';

interface ToastNotification {
  id: string;
  type: 'out_of_stock' | 'critical' | 'product_added';
  title: string;
  message: string;
  timestamp: Date;
}

export function useBottomNotifications() {
  const [notifications, setNotifications] = useState<ToastNotification[]>([]);

  const addNotification = useCallback((
    type: ToastNotification['type'],
    title: string,
    message: string
  ) => {
    const notification: ToastNotification = {
      id: `toast_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      type,
      title,
      message,
      timestamp: new Date(),
    };

    setNotifications(prev => [...prev, notification]);
  }, []);

  const dismissNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  }, []);

  const notifyStockOut = useCallback((productName: string) => {
    addNotification(
      'out_of_stock',
      'Stock épuisé',
      `${productName} n'est plus en stock`
    );
  }, [addNotification]);

  const notifyStockCritical = useCallback((productName: string, quantity: number) => {
    addNotification(
      'critical',
      'Stock critique',
      `${productName}: ${quantity} unité${quantity > 1 ? 's' : ''} restante${quantity > 1 ? 's' : ''}`
    );
  }, [addNotification]);

  const notifyProductAdded = useCallback((productName: string) => {
    addNotification(
      'product_added',
      'Produit ajouté',
      `${productName} a été ajouté avec succès`
    );
  }, [addNotification]);

  return {
    notifications,
    dismissNotification,
    notifyStockOut,
    notifyStockCritical,
    notifyProductAdded,
  };
}
