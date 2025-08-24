/**
 * Types pour le système d'authentification
 */

export type UserRole = 'admin' | 'manager' | 'server' | 'cashier';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: UserRole;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  last_login?: string;
  date_joined: string;
  permissions?: string[];
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  sessionExpiry?: number;
  lastActivity?: number;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  token?: string;
  refresh_token?: string;
}

export interface AuthContextType {
  // État
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<boolean>;
  
  // Vérifications de permissions
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasRole: (role: UserRole) => boolean;
  hasAnyRole: (roles: UserRole[]) => boolean;
  
  // Utilitaires de rôles
  isAdmin: () => boolean;
  isManager: () => boolean;
  isServer: () => boolean;
  isCashier: () => boolean;
}

export interface PermissionConfig {
  [key: string]: {
    name: string;
    description: string;
    category: string;
    requiredRoles?: UserRole[];
  };
}

export type RolePermissions = {
  [K in UserRole]: string[];
}
