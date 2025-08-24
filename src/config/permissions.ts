/**
 * Configuration centralisée des permissions et rôles
 */

import { UserRole, PermissionConfig, RolePermissions } from '@/types/auth';

/**
 * Configuration des permissions disponibles dans le système
 */
export const PERMISSIONS: PermissionConfig = {
  // Dashboard
  'dashboard.view': {
    name: 'Voir le dashboard',
    description: 'Accès au tableau de bord principal',
    category: 'dashboard',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  },

  // Ventes
  'sales.view': {
    name: 'Voir les ventes',
    description: 'Consulter les ventes existantes',
    category: 'sales',
    requiredRoles: ['admin', 'manager', 'cashier']
  },
  'sales.create': {
    name: 'Créer des ventes',
    description: 'Enregistrer de nouvelles ventes',
    category: 'sales',
    requiredRoles: ['admin', 'manager', 'cashier']
  },
  'sales.edit': {
    name: 'Modifier les ventes',
    description: 'Modifier les ventes existantes',
    category: 'sales',
    requiredRoles: ['admin', 'manager']
  },
  'sales.delete': {
    name: 'Supprimer les ventes',
    description: 'Supprimer des ventes',
    category: 'sales',
    requiredRoles: ['admin']
  },

  // Produits
  'products.view': {
    name: 'Voir les produits',
    description: 'Consulter le catalogue des produits',
    category: 'products',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  },
  'products.create': {
    name: 'Créer des produits',
    description: 'Ajouter de nouveaux produits',
    category: 'products',
    requiredRoles: ['admin', 'manager']
  },
  'products.edit': {
    name: 'Modifier les produits',
    description: 'Modifier les produits existants',
    category: 'products',
    requiredRoles: ['admin', 'manager']
  },
  'products.delete': {
    name: 'Supprimer les produits',
    description: 'Supprimer des produits',
    category: 'products',
    requiredRoles: ['admin']
  },

  // Stocks
  'stocks.view': {
    name: 'Voir les stocks',
    description: 'Consulter les niveaux de stock',
    category: 'stocks',
    requiredRoles: ['admin', 'manager']
  },
  'stocks.manage': {
    name: 'Gérer les stocks',
    description: 'Modifier les stocks et mouvements',
    category: 'stocks',
    requiredRoles: ['admin', 'manager']
  },

  // Tables
  'tables.view': {
    name: 'Voir les tables',
    description: 'Consulter les tables du restaurant',
    category: 'tables',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  },
  'tables.manage': {
    name: 'Gérer les tables',
    description: 'Modifier le statut des tables',
    category: 'tables',
    requiredRoles: ['admin', 'manager', 'server']
  },

  // Commandes
  'orders.view': {
    name: 'Voir les commandes',
    description: 'Consulter les commandes',
    category: 'orders',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  },
  'orders.create': {
    name: 'Créer des commandes',
    description: 'Enregistrer de nouvelles commandes',
    category: 'orders',
    requiredRoles: ['admin', 'manager', 'server']
  },
  'orders.edit': {
    name: 'Modifier les commandes',
    description: 'Modifier les commandes existantes',
    category: 'orders',
    requiredRoles: ['admin', 'manager', 'server']
  },

  // Finances
  'finances.view': {
    name: 'Voir les finances',
    description: 'Consulter les données financières',
    category: 'finances',
    requiredRoles: ['admin', 'manager']
  },
  'finances.history': {
    name: 'Historique des ventes',
    description: 'Consulter l\'historique des ventes',
    category: 'finances',
    requiredRoles: ['admin', 'manager', 'cashier']
  },
  'finances.reports': {
    name: 'Rapports financiers',
    description: 'Générer des rapports financiers',
    category: 'finances',
    requiredRoles: ['admin', 'manager']
  },

  // Utilisateurs
  'users.view': {
    name: 'Voir les utilisateurs',
    description: 'Consulter la liste des utilisateurs',
    category: 'users',
    requiredRoles: ['admin']
  },
  'users.create': {
    name: 'Créer des utilisateurs',
    description: 'Ajouter de nouveaux utilisateurs',
    category: 'users',
    requiredRoles: ['admin']
  },
  'users.edit': {
    name: 'Modifier les utilisateurs',
    description: 'Modifier les utilisateurs existants',
    category: 'users',
    requiredRoles: ['admin']
  },
  'users.delete': {
    name: 'Supprimer les utilisateurs',
    description: 'Supprimer des utilisateurs',
    category: 'users',
    requiredRoles: ['admin']
  },

  // Paramètres
  'settings.view': {
    name: 'Voir les paramètres',
    description: 'Consulter les paramètres système',
    category: 'settings',
    requiredRoles: ['admin']
  },
  'settings.edit': {
    name: 'Modifier les paramètres',
    description: 'Modifier les paramètres système',
    category: 'settings',
    requiredRoles: ['admin']
  },

  // Profil
  'profile.view': {
    name: 'Voir le profil',
    description: 'Consulter son propre profil',
    category: 'profile',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  },
  'profile.edit': {
    name: 'Modifier le profil',
    description: 'Modifier son propre profil',
    category: 'profile',
    requiredRoles: ['admin', 'manager', 'server', 'cashier']
  }
};

/**
 * Permissions par défaut pour chaque rôle
 */
export const ROLE_PERMISSIONS: RolePermissions = {
  admin: [
    // Accès complet à tout
    ...Object.keys(PERMISSIONS)
  ],
  
  manager: [
    'dashboard.view',
    'sales.view',
    'sales.create',
    'sales.edit',
    'products.view',
    'products.create',
    'products.edit',
    'stocks.view',
    'stocks.manage',
    'tables.view',
    'tables.manage',
    'orders.view',
    'orders.create',
    'orders.edit',
    'finances.view',
    'finances.history',
    'finances.reports',
    'profile.view',
    'profile.edit'
  ],
  
  server: [
    'dashboard.view',
    'products.view',
    'tables.view',
    'tables.manage',
    'orders.view',
    'orders.create',
    'orders.edit',
    'profile.view',
    'profile.edit'
  ],
  
  cashier: [
    'dashboard.view',
    'sales.view',
    'sales.create',
    'products.view',
    'tables.view',
    'orders.view',
    'finances.history',
    'profile.view',
    'profile.edit'
  ]
};

/**
 * Vérifier si un rôle a une permission spécifique
 */
export function roleHasPermission(role: UserRole, permission: string): boolean {
  return ROLE_PERMISSIONS[role]?.includes(permission) || false;
}

/**
 * Obtenir toutes les permissions d'un rôle
 */
export function getRolePermissions(role: UserRole): string[] {
  return ROLE_PERMISSIONS[role] || [];
}

/**
 * Vérifier si une permission existe
 */
export function permissionExists(permission: string): boolean {
  return permission in PERMISSIONS;
}

/**
 * Obtenir les informations d'une permission
 */
export function getPermissionInfo(permission: string) {
  return PERMISSIONS[permission] || null;
}
