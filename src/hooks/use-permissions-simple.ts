// Simplified permissions hook without auth dependency

export const usePermissions = () => {
  // Return all menus accessible (no auth system)
  const accessibleMenus = [
    { path: '/', label: 'Tableau de bord', category: 'dashboard' },
    { path: '/profile', label: 'Profil', category: 'profile' },
    { path: '/products', label: 'Produits', category: 'products' },
    { path: '/sales', label: 'Ventes', category: 'sales' },
    { path: '/kitchen', label: 'Cuisine', category: 'kitchen' },
    { path: '/stocks', label: 'Stocks', category: 'stocks' },
    { path: '/stock-sync', label: 'Sync Stock', category: 'stocks' },
    { path: '/supplies', label: 'Approvisionnement', category: 'supplies' },
    { path: '/sales-history', label: 'Historique', category: 'sales' },
    { path: '/daily-report', label: 'Rapport', category: 'reports' },
    { path: '/settings', label: 'Paramètres', category: 'settings' },
    { path: '/users', label: 'Utilisateurs', category: 'users' },
    { path: '/tables', label: 'Tables', category: 'tables' },
    { path: '/orders', label: 'Commandes', category: 'orders' }
  ];

  return {
    accessibleMenus,
    hasPermission: () => true,
    canAccessMenu: () => true,
    userPermissions: ['*']
  };
};
