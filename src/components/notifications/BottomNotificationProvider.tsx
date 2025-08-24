import { createContext, useContext, ReactNode } from 'react';
import { useBottomNotifications } from '@/hooks/use-bottom-notifications';
import { BottomToast } from './BottomToast';

const BottomNotificationContext = createContext<ReturnType<typeof useBottomNotifications> | null>(null);

export function BottomNotificationProvider({ children }: { children: ReactNode }) {
  const bottomNotifications = useBottomNotifications();

  return (
    <BottomNotificationContext.Provider value={bottomNotifications}>
      {children}
      <BottomToast 
        notifications={bottomNotifications.notifications}
        onDismiss={bottomNotifications.dismissNotification}
      />
    </BottomNotificationContext.Provider>
  );
}

export function useBottomNotificationContext() {
  const context = useContext(BottomNotificationContext);
  if (!context) {
    throw new Error('useBottomNotificationContext must be used within BottomNotificationProvider');
  }
  return context;
}
