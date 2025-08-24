import { useEffect, useState, useCallback } from 'react';
import { useNotificationHelpers } from './use-notifications';
import { useBottomNotificationContext } from '@/components/notifications/BottomNotificationProvider';

interface StockItem {
  id: number;
  name: string;
  current_stock: number;
  minimum_stock: number;
  category: {
    name: string;
  };
  is_active: boolean;
}

/**
 * Hook pour surveiller les stocks et générer des notifications automatiques
 */
export function useStockNotifications() {
  const { notifyStockAlert } = useNotificationHelpers();
  const { notifyStockOut, notifyStockCritical } = useBottomNotificationContext();
  const [stocksData, setStocksData] = useState<StockItem[]>([]);
  const [notifiedItems, setNotifiedItems] = useState<Set<string>>(new Set());

  // Fonction pour récupérer les alertes de stock depuis l'API
  const fetchStockAlerts = useCallback(async () => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      // Récupérer les alertes actives de type stock
      const alertsResponse = await fetch('http://localhost:8000/api/alerts/active/?type=stock', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (alertsResponse.ok) {
        const alertsData = await alertsResponse.json();
        
        // Traiter les alertes reçues
        alertsData.forEach((alert: any) => {
          const notificationKey = `alert-${alert.id}`;
          
          // Éviter les notifications en double
          if (notifiedItems.has(notificationKey)) return;

          if (alert.priority === 'critical' && alert.related_product) {
            notifyStockAlert(alert.related_product.name, 0, 'out');
            notifyStockOut(alert.related_product.name);
          } else if (alert.priority === 'high' && alert.related_product) {
            const stockMatch = alert.message.match(/(\d+)\s+unité/);
            const quantity = stockMatch ? parseInt(stockMatch[1]) : 1;
            notifyStockAlert(alert.related_product.name, quantity, 'low');
            notifyStockCritical(alert.related_product.name, quantity);
          }

          setNotifiedItems(prev => new Set([...prev, notificationKey]));
        });
      }

      // Récupérer aussi les données de produits pour les statistiques
      const productsResponse = await fetch('http://localhost:8000/api/products/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (productsResponse.ok) {
        const productsData = await productsResponse.json();
        setStocksData(productsData.results || productsData);
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des alertes:', error);
    }
  }, [notifyStockAlert, notifyStockOut, notifyStockCritical, notifiedItems]);

  // Vérifier les stocks et générer les notifications
  useEffect(() => {
    if (!stocksData.length) return;

    const currentNotifications = new Set<string>();

    stocksData.forEach((stock: StockItem) => {
      if (!stock.is_active) return;

      const isOutOfStock = stock.current_stock === 0;
      const isLowStock = stock.current_stock > 0 && stock.current_stock <= stock.minimum_stock;
      
      const notificationKey = `${stock.id}-${stock.current_stock}`;

      // Éviter les notifications en double
      if (notifiedItems.has(notificationKey)) return;

      if (isOutOfStock) {
        notifyStockAlert(stock.name, 0, 'out');
        notifyStockOut(stock.name); // Toast en bas
        currentNotifications.add(notificationKey);
      } else if (isLowStock) {
        notifyStockAlert(stock.name, stock.current_stock, 'low');
        notifyStockCritical(stock.name, stock.current_stock); // Toast en bas
        currentNotifications.add(notificationKey);
      }
    });

    // Mettre à jour les éléments notifiés
    setNotifiedItems(prev => new Set([...prev, ...currentNotifications]));

    // Nettoyer les anciennes notifications après 1 heure
    setTimeout(() => {
      setNotifiedItems(prev => {
        const updated = new Set(prev);
        currentNotifications.forEach(key => updated.delete(key));
        return updated;
      });
    }, 60 * 60 * 1000);

  }, [stocksData, notifyStockAlert, notifiedItems]);

  // Récupérer les alertes toutes les 30 secondes
  useEffect(() => {
    fetchStockAlerts(); // Récupération initiale

    const interval = setInterval(fetchStockAlerts, 30000);
    return () => clearInterval(interval);
  }, [fetchStockAlerts]);

  // Fonction pour forcer une vérification
  const checkStockNow = useCallback(() => {
    fetchStockAlerts();
  }, [fetchStockAlerts]);

  // Retourner les statistiques de stock
  const stockStats = {
    total: stocksData.length,
    outOfStock: stocksData.filter(item => item.current_stock === 0).length,
    lowStock: stocksData.filter(item => 
      item.current_stock > 0 && item.current_stock <= item.minimum_stock
    ).length,
    healthy: stocksData.filter(item => 
      item.current_stock > item.minimum_stock
    ).length
  };

  return {
    stockStats,
    checkStockNow,
    stocksData
  };
}
