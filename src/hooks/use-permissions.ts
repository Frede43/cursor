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
  
  // Ventes
  sales: ['sales.view', 'sales.create'],
  'sales-history': ['sales.history'],
  
  // Produits et stocks
  products: ['products.view'],
  stocks: ['stocks.view'],
  'stock-sync': ['stocks.manage'],
  supplies: ['stocks.manage'],
  
  // Tables et commandes
  tables: ['tables.view'],
  orders: ['orders.view'],
  
  // Cuisine
  kitchen: ['kitchen.view'],
  
  // Rapports et analyses
  'daily-report': ['reports.view'],
  reports: ['reports.view'],
  analytics: ['analytics.view'],
  
  // Administration
  users: ['users.view'],
  suppliers: ['suppliers.view'],
  expenses: ['expenses.view'],
  
  // Système
  settings: ['settings.view'],
  alerts: [], // Accessible à tous
  monitoring: ['settings.view'],
  help: [], // Accessible à tous
  
  // Profil - accessible à tous
  profile: [],
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
  
  return useHasAnyPermission(requiredPermissions);
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
