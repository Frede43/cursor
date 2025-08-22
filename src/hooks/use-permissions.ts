import { useQuery } from '@tanstack/react-query';
import { apiService } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

interface UserPermissions {
  role: string;
  permissions: {
    [key: string]: boolean;
  };
}

/**
 * Hook pour récupérer et vérifier les permissions de l'utilisateur connecté
 */
export function useUserPermissions() {
  return useQuery<UserPermissions>({
    queryKey: ['user-permissions'],
    queryFn: () => apiService.get('/accounts/permissions/'),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook pour vérifier si l'utilisateur a une permission spécifique
 */
export function useHasPermission(permissionCode: string) {
  const { data: permissions } = useUserPermissions();
  
  // Les admins ont toutes les permissions
  if (permissions?.role === 'admin') {
    return true;
  }
  
  // Vérifier la permission spécifique
  return permissions?.permissions?.[permissionCode] || false;
}

/**
 * Hook pour vérifier plusieurs permissions
 */
export function useHasAnyPermission(permissionCodes: string[]) {
  const { data: permissions } = useUserPermissions();
  
  // Les admins ont toutes les permissions
  if (permissions?.role === 'admin') {
    return true;
  }
  
  // Vérifier si l'utilisateur a au moins une des permissions
  return permissionCodes.some(code => permissions?.permissions?.[code]);
}

/**
 * Configuration des menus avec leurs permissions requises
 */
export const MENU_PERMISSIONS = {
  // Dashboard - accessible à tous les utilisateurs connectés
  dashboard: [],
  
  // Ventes - permissions étendues
  sales: ['sales.view', 'sales.create'],
  'sales-history': ['sales.history'],
  'sales-manage': ['sales.manage'],
  'sales-refund': ['sales.refund'],
  'sales-discount': ['sales.discount'],
  
  // Produits et stocks - permissions étendues
  products: ['products.view'],
  'products-create': ['products.create'],
  'products-edit': ['products.edit'],
  'products-delete': ['products.delete'],
  stocks: ['stocks.view'],
  'stock-sync': ['stocks.manage'],
  'stocks-adjust': ['stocks.adjust'],
  'stocks-transfer': ['stocks.transfer'],
  supplies: ['stocks.manage'],
  
  // Tables et commandes - permissions étendues
  tables: ['tables.view'],
  'tables-manage': ['tables.manage'],
  orders: ['orders.view'],
  'orders-create': ['orders.create'],
  'orders-edit': ['orders.edit'],
  'orders-cancel': ['orders.cancel'],
  
  // Cuisine - permissions étendues
  kitchen: ['kitchen.view'],
  'kitchen-manage': ['kitchen.manage'],
  
  // Rapports et analyses - permissions étendues
  'daily-report': ['reports.view'],
  reports: ['reports.view'],
  'reports-export': ['reports.export'],
  analytics: ['analytics.view'],
  'analytics-advanced': ['analytics.advanced'],
  
  // Administration - permissions étendues
  users: ['users.view'],
  'users-create': ['users.create'],
  'users-edit': ['users.edit'],
  'users-delete': ['users.delete'],
  'users-permissions': ['users.permissions'],
  suppliers: ['suppliers.view'],
  'suppliers-manage': ['suppliers.manage'],
  expenses: ['expenses.view'],
  'expenses-create': ['expenses.create'],
  'expenses-approve': ['expenses.approve'],
  'expenses-manage': ['expenses.manage'],
  
  // Système - permissions étendues
  settings: ['settings.view'],
  'settings-manage': ['settings.manage'],
  alerts: [], // Accessible à tous
  monitoring: ['monitoring.view'],
  'system-backup': ['system.backup'],
  'system-maintenance': ['system.maintenance'],
  help: [], // Accessible à tous
  
  // Profil - accessible à tous
  profile: [],
  
  // Permissions spéciales pour caissiers
  'cashier-sales': ['sales.view', 'sales.create'],
  'cashier-history': ['sales.history'],
  'cashier-refund': ['sales.refund'],
  
  // Permissions spéciales pour serveurs
  'server-orders': ['orders.view', 'orders.create'],
  'server-tables': ['tables.view'],
  
  // Permissions spéciales pour managers
  'manager-reports': ['reports.view', 'analytics.view'],
  'manager-users': ['users.view', 'users.edit'],
} as const;

/**
 * Hook pour vérifier si un menu est accessible
 */
export function useCanAccessMenu(menuKey: keyof typeof MENU_PERMISSIONS) {
  const requiredPermissions = MENU_PERMISSIONS[menuKey];
  
  // Si aucune permission requise, accessible à tous
  if (requiredPermissions.length === 0) {
    return true;
  }
  
  return useHasAnyPermission([...requiredPermissions]);
}

/**
 * Hook pour filtrer les menus accessibles
 */
export function useAccessibleMenus() {
  const { data: permissions, isLoading } = useUserPermissions();
  
  const getAccessibleMenus = () => {
    if (isLoading || !permissions) return [];
    
    return Object.keys(MENU_PERMISSIONS).filter(menuKey => {
      const requiredPermissions = MENU_PERMISSIONS[menuKey as keyof typeof MENU_PERMISSIONS];
      
      // Si aucune permission requise, accessible à tous
      if (requiredPermissions.length === 0) {
        return true;
      }
      
      // Les admins ont accès à tout
      if (permissions.role === 'admin') {
        return true;
      }
      
      // Vérifier si l'utilisateur a au moins une des permissions requises
      return requiredPermissions.some(code => permissions.permissions?.[code]);
    });
  };
  
  return {
    accessibleMenus: getAccessibleMenus(),
    isLoading,
    userRole: permissions?.role
  };
}

/**
 * Définition des rôles par défaut avec leurs permissions
 */
export const DEFAULT_ROLE_PERMISSIONS = {
  admin: [], // Toutes les permissions
  manager: [
    'sales.view', 'sales.create', 'sales.edit', 'sales.history',
    'products.view', 'products.create', 'products.edit',
    'stocks.view', 'stocks.manage', 'stocks.alerts',
    'tables.view', 'tables.manage',
    'orders.view', 'orders.manage',
    'kitchen.view', 'kitchen.ingredients', 'kitchen.recipes',
    'reports.view', 'reports.advanced', 'reports.export',
    'analytics.view',
    'suppliers.view', 'suppliers.manage',
    'expenses.view', 'expenses.manage',
  ],
  server: [
    'sales.view', 'sales.create',
    'products.view',
    'tables.view', 'tables.manage',
    'orders.view', 'orders.manage',
  ],
  cashier: [
    'sales.view', 'sales.create',
    'products.view',
    'tables.view',
    'orders.view',
  ]
} as const;
