/**
 * Hook pour la gestion des permissions et menus
 */

import { useMemo } from 'react';
import { useAuth } from './useAuth';
import { getRolePermissions, PERMISSIONS } from '@/config/permissions';
import { UserRole } from '@/types/auth';

/**
 * Configuration des menus avec leurs permissions requises
 */
export const MENU_PERMISSIONS = {
  // Principal
  dashboard: ['dashboard.view'],
  profile: ['profile.view'],
  
  // Gestion
  products: ['products.view'],
  sales: ['sales.view'],
  kitchen: [], // Accessible selon rôle
  
  // Stocks
  stocks: ['stocks.view'],
  'stock-sync': ['stocks.manage'],
  supplies: ['stocks.manage'],
  
  // Finances
  'sales-history': ['finances.history'],
  'daily-report': ['finances.reports'],
  reports: ['finances.reports'],
  analytics: ['finances.view'],
  expenses: ['finances.view'],
  
  // Opérations
  tables: ['tables.view'],
  orders: ['orders.view'],
  
  // Administration
  users: ['users.view'],
  suppliers: ['stocks.manage'],
  
  // Système
  alerts: [], // Accessible à tous
  monitoring: ['settings.view'],
  settings: ['settings.view'],
  help: [] // Accessible à tous
} as const;

export type MenuKey = keyof typeof MENU_PERMISSIONS;

/**
 * Hook pour vérifier l'accès aux menus
 */
export const usePermissions = () => {
  const { user, hasPermission, hasAnyPermission } = useAuth();

  /**
   * Vérifier si un menu est accessible
   */
  const canAccessMenu = (menuKey: MenuKey): boolean => {
    if (!user) return false;

    const requiredPermissions = MENU_PERMISSIONS[menuKey];
    
    // Si aucune permission requise, accessible à tous les utilisateurs connectés
    if (requiredPermissions.length === 0) {
      return true;
    }

    // Vérifier les permissions
    return hasAnyPermission([...requiredPermissions]);
  };

  /**
   * Obtenir tous les menus accessibles
   */
  const accessibleMenus = useMemo(() => {
    if (!user) return [];

    return Object.keys(MENU_PERMISSIONS).filter(menuKey => 
      canAccessMenu(menuKey as MenuKey)
    );
  }, [user]);

  /**
   * Obtenir les permissions de l'utilisateur actuel
   */
  const userPermissions = useMemo(() => {
    if (!user) return [];
    return getRolePermissions(user.role);
  }, [user]);

  return {
    canAccessMenu,
    accessibleMenus,
    userPermissions,
    hasPermission,
    hasAnyPermission
  };
};

export default usePermissions;
