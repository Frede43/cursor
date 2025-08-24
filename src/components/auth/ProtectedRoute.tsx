/**
 * Composant de protection des routes avec gestion des permissions
 */

import { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/use-auth';
import { UserRole } from '@/types/auth';
import { LoadingSpinner } from '@/components/ui/loading-spinner';
import { AccessDenied } from '@/components/auth/AccessDenied';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredPermissions?: string[];
  requiredRoles?: UserRole[];
  requireAnyPermission?: boolean; // Si true, une seule permission suffit
  requireAnyRole?: boolean; // Si true, un seul rôle suffit
  fallbackPath?: string;
}

export const ProtectedRoute = ({
  children,
  requiredPermissions = [],
  requiredRoles = [],
  requireAnyPermission = false,
  requireAnyRole = false,
  fallbackPath = '/login'
}: ProtectedRouteProps) => {
  const { 
    user, 
    isAuthenticated, 
    isLoading, 
    hasPermission, 
    hasAnyPermission, 
    hasRole, 
    hasAnyRole 
  } = useAuth();
  const location = useLocation();

  // Affichage du chargement
  if (isLoading) {
    return <LoadingSpinner />;
  }

  // Redirection si non authentifié
  if (!isAuthenticated || !user) {
    return (
      <Navigate 
        to={fallbackPath} 
        state={{ from: location.pathname }} 
        replace 
      />
    );
  }

  // Vérification des rôles requis
  if (requiredRoles.length > 0) {
    const hasRequiredRole = requireAnyRole 
      ? hasAnyRole(requiredRoles)
      : requiredRoles.every(role => hasRole(role));

    if (!hasRequiredRole) {
      return (
        <AccessDenied 
          type="role"
          required={requiredRoles}
          current={user.role}
          message="Votre rôle ne vous permet pas d'accéder à cette page"
        />
      );
    }
  }

  // Vérification des permissions requises
  if (requiredPermissions.length > 0) {
    const hasRequiredPermission = requireAnyPermission
      ? hasAnyPermission(requiredPermissions)
      : requiredPermissions.every(permission => hasPermission(permission));

    if (!hasRequiredPermission) {
      return (
        <AccessDenied 
          type="permission"
          required={requiredPermissions}
          message="Vous n'avez pas les permissions nécessaires pour accéder à cette page"
        />
      );
    }
  }

  // Rendu du contenu protégé
  return <>{children}</>;
};

export default ProtectedRoute;
