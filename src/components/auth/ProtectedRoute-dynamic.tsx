import { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/hooks/use-auth-dynamic';
import { UserRole } from '@/types/auth';
import { Loader2 } from 'lucide-react';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRole?: UserRole;
  requiredPermissions?: string[];
  requireAnyPermission?: boolean;
  accessDeniedComponent?: ReactNode;
}

export function ProtectedRoute({ 
  children, 
  requiredRole, 
  requiredPermissions = [],
  requireAnyPermission = false,
  accessDeniedComponent
}: ProtectedRouteProps) {
  const { user, isLoading, isAuthenticated } = useAuth();
  const location = useLocation();

  // Affichage du chargement
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">Vérification de l'authentification...</p>
        </div>
      </div>
    );
  }

  // Redirection vers login si non authentifié
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Vérification du rôle requis
  if (requiredRole && user.role !== requiredRole) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Accès refusé</h2>
          <p className="text-muted-foreground mb-4">
            Vous n'avez pas les permissions nécessaires pour accéder à cette page.
          </p>
          <p className="text-sm text-muted-foreground">
            Rôle requis: {requiredRole} | Votre rôle: {user.role}
          </p>
        </div>
      </div>
    );
  }

  // Vérification des permissions - les admins ont accès à tout
  if (requiredPermissions.length > 0) {
    // Les admins ont accès à toutes les fonctionnalités
    if (user.role === 'admin') {
      return <>{children}</>;
    }
    
    // Pour les autres rôles, vérifier les permissions
    if (user.permissions) {
      const hasPermissions = requireAnyPermission
        ? requiredPermissions.some(permission => user.permissions?.includes(permission))
        : requiredPermissions.every(permission => user.permissions?.includes(permission));

      if (!hasPermissions) {
        console.log('DEBUG - Permission refusée:', {
          userRole: user.role,
          userPermissions: user.permissions,
          requiredPermissions,
          hasPermissions
        });
        // Utiliser le composant personnalisé si fourni, sinon le message par défaut
        if (accessDeniedComponent) {
          return <>{accessDeniedComponent}</>;
        }
        
        return (
          <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Accès refusé
              </h2>
              <p className="text-gray-600">
                Vous n'avez pas les permissions nécessaires pour accéder à cette page.
              </p>
              <p className="text-sm text-gray-500 mt-2">
                Permissions requises: {requiredPermissions.join(', ')}
              </p>
              <p className="text-sm text-gray-500">
                Vos permissions: {user.permissions?.join(', ') || 'Aucune'}
              </p>
            </div>
          </div>
        );
      }
    } else {
      // Si pas de permissions définies pour un utilisateur non-admin
      return (
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Accès refusé
            </h2>
            <p className="text-gray-600">
              Aucune permission définie pour votre compte.
            </p>
          </div>
        </div>
      );
    }
  }

  return <>{children}</>;
}
