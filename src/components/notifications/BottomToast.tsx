import { useState, useEffect } from 'react';
import { X, Package, Plus, AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface ToastNotification {
  id: string;
  type: 'out_of_stock' | 'critical' | 'product_added';
  title: string;
  message: string;
  timestamp: Date;
}

interface BottomToastProps {
  notifications: ToastNotification[];
  onDismiss: (id: string) => void;
}

export function BottomToast({ notifications, onDismiss }: BottomToastProps) {
  const [visibleNotifications, setVisibleNotifications] = useState<ToastNotification[]>([]);

  useEffect(() => {
    // Afficher les nouvelles notifications
    const newNotifications = notifications.filter(
      notif => !visibleNotifications.find(visible => visible.id === notif.id)
    );

    if (newNotifications.length > 0) {
      setVisibleNotifications(prev => [...prev, ...newNotifications]);

      // Auto-dismiss après 5 secondes
      newNotifications.forEach(notif => {
        setTimeout(() => {
          handleDismiss(notif.id);
        }, 5000);
      });
    }
  }, [notifications, visibleNotifications]);

  const handleDismiss = (id: string) => {
    setVisibleNotifications(prev => prev.filter(notif => notif.id !== id));
    onDismiss(id);
  };

  const getToastStyles = (type: ToastNotification['type']) => {
    switch (type) {
      case 'out_of_stock':
        return 'bg-yellow-500 text-yellow-50 border-yellow-600';
      case 'critical':
        return 'bg-red-500 text-red-50 border-red-600';
      case 'product_added':
        return 'bg-white text-gray-900 border-gray-300 shadow-lg';
      default:
        return 'bg-blue-500 text-blue-50 border-blue-600';
    }
  };

  const getIcon = (type: ToastNotification['type']) => {
    switch (type) {
      case 'out_of_stock':
        return <Package className="h-4 w-4" />;
      case 'critical':
        return <AlertTriangle className="h-4 w-4" />;
      case 'product_added':
        return <Plus className="h-4 w-4" />;
      default:
        return <Package className="h-4 w-4" />;
    }
  };

  if (visibleNotifications.length === 0) return null;

  return (
    <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 space-y-2">
      {visibleNotifications.slice(-3).map((notification) => (
        <div
          key={notification.id}
          className={cn(
            'flex items-center gap-3 px-4 py-3 rounded-lg border shadow-lg min-w-80 max-w-md animate-in slide-in-from-bottom-2',
            getToastStyles(notification.type)
          )}
        >
          <div className="flex-shrink-0">
            {getIcon(notification.type)}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="font-medium text-sm">
              {notification.title}
            </div>
            <div className="text-xs opacity-90 mt-1">
              {notification.message}
            </div>
          </div>

          <Button
            variant="ghost"
            size="sm"
            className={cn(
              "h-6 w-6 p-0 hover:bg-black/10",
              notification.type === 'product_added' ? "hover:bg-gray-200" : ""
            )}
            onClick={() => handleDismiss(notification.id)}
          >
            <X className="h-3 w-3" />
          </Button>
        </div>
      ))}
    </div>
  );
}
