import { Navigate } from 'react-router-dom';
import { ReactNode } from 'react';
import { useAuth } from '../hooks/use-auth';
import { useToast } from '../hooks/use-toast';

interface ProtectedRouteProps {
  children: ReactNode;
  requiredRole?: string;
  requiredPermission?: string;
}

const ProtectedRoute = ({ children, requiredRole, requiredPermission }: ProtectedRouteProps) => {
  const { user, isLoading, hasPermission, hasRole } = useAuth();
  const { toast } = useToast();

  // Afficher un écran de chargement pendant la vérification
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  // Rediriger vers la page de connexion si non authentifié
  if (!user) {
    toast({
      title: "Accès refusé",
      description: "Vous devez être connecté pour accéder à cette page",
      variant: "destructive",
    });
    return <Navigate to="/login" replace />;
  }

  // Vérifier le rôle requis
  if (requiredRole && !hasRole(requiredRole)) {
    toast({
      title: "Accès refusé",
      description: "Votre rôle ne vous permet pas d'accéder à cette page",
      variant: "destructive",
    });
    
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center p-8 bg-red-50 rounded-lg border border-red-200 max-w-md mx-auto">
          <div className="text-red-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-red-600 mb-4">Accès refusé</h2>
          <p className="text-gray-600 mb-2">Vous n'avez pas les permissions nécessaires pour accéder à cette page.</p>
          <p className="text-sm text-gray-500 mt-2">Rôle requis: <span className="font-semibold">{requiredRole}</span></p>
          <p className="text-sm text-gray-500">Votre rôle: <span className="font-semibold">{user.role}</span></p>
        </div>
      </div>
    );
  }

  // Vérifier la permission requise
  if (requiredPermission && !hasPermission(requiredPermission)) {
    toast({
      title: "Accès refusé",
      description: "Vous n'avez pas la permission nécessaire pour accéder à cette page",
      variant: "destructive",
    });
    
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center p-8 bg-red-50 rounded-lg border border-red-200 max-w-md mx-auto">
          <div className="text-red-600 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728L5.636 5.636m12.728 12.728L18.364 5.636M5.636 18.364l12.728-12.728" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-red-600 mb-4">Accès refusé</h2>
          <p className="text-gray-600 mb-2">Vous n'avez pas la permission nécessaire pour accéder à cette page.</p>
          <p className="text-sm text-gray-500 mt-2">Permission requise: <span className="font-semibold">{requiredPermission}</span></p>
          <p className="text-sm text-gray-500">Contactez votre administrateur pour obtenir l'accès.</p>
        </div>
      </div>
    );
  }

  // Afficher le contenu protégé si authentifié et autorisé
  return <>{children}</>;
};

export default ProtectedRoute;