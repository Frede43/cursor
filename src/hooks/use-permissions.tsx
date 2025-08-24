import { useAuth } from './use-auth';

// Définition des permissions par rôle
const ROLE_PERMISSIONS = {
  admin: [
    'dashboard', 'profile', 'products', 'sales', 'kitchen', 
    'stocks', 'stock-sync', 'supplies', 'sales-history', 
    'daily-report', 'settings', 'users', 'tables', 'orders'
  ],
  manager: [
    'dashboard', 'profile', 'products', 'sales', 'kitchen', 
    'stocks', 'stock-sync', 'supplies', 'sales-history', 
    'daily-report', 'tables', 'orders'
  ],
  cashier: [
    'dashboard', 'profile', 'sales', 'sales-history', 
    'tables', 'orders'
  ],
  server: [
    'dashboard', 'profile', 'sales', 'tables', 'orders'
  ]
};

export const usePermissions = () => {
  const { user, hasRole } = useAuth();
  
  // Déterminer les menus accessibles en fonction du rôle
  const getAccessibleMenus = () => {
    if (!user) return [];
    
    // Si l'utilisateur est superuser, il a accès à tout
    if (user.is_superuser) {
      return Object.values(ROLE_PERMISSIONS).flat();
    }
    
    // Vérifier le rôle de l'utilisateur
    for (const [role, permissions] of Object.entries(ROLE_PERMISSIONS)) {
      if (hasRole(role)) {
        return permissions;
      }
    }
    
    // Par défaut, accès minimal
    return ['dashboard', 'profile'];
  };
  
  // Vérifier si l'utilisateur peut accéder à un menu spécifique
  const canAccessMenu = (menuKey: string) => {
    if (!user) return false;
    
    // Si l'utilisateur est superuser, il a accès à tout
    if (user.is_superuser) return true;
    
    // Vérifier si le menu est dans les permissions du rôle
    return getAccessibleMenus().includes(menuKey);
  };
  
  // Récupérer les menus accessibles
  const accessibleMenus = getAccessibleMenus();
  
  return {
    canAccessMenu,
    accessibleMenus
  };
};