/**
 * Hook d'authentification professionnel avec gestion des permissions
 */

import { useState, useEffect, createContext, useContext, ReactNode, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToast } from './use-toast';
import { AuthContextType, User, UserRole, LoginCredentials } from '@/types/auth';
import { authService } from '@/services/auth.service';
import { getRolePermissions, roleHasPermission } from '@/config/permissions';

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const { toast } = useToast();

  // Initialisation de l'authentification
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const currentUser = authService.getCurrentUser();
        if (currentUser) {
          setUser(currentUser);
          
          // Vérifier la validité de la session en arrière-plan
          const isValid = await authService.refreshSession();
          if (!isValid) {
            setUser(null);
            navigate('/login');
          }
        }
      } catch (error) {
        console.error('Erreur lors de l\'initialisation de l\'authentification:', error);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, [navigate]);

  // Surveillance de l'activité utilisateur
  useEffect(() => {
    if (!user) return;

    const handleActivity = () => {
      authService.updateActivity();
    };

    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    // Throttle pour éviter trop d'appels
    let lastUpdate = 0;
    const throttledHandler = () => {
      const now = Date.now();
      if (now - lastUpdate > 30000) { // Max toutes les 30 secondes
        lastUpdate = now;
        handleActivity();
      }
    };

    events.forEach(event => {
      document.addEventListener(event, throttledHandler, true);
    });

    return () => {
      events.forEach(event => {
        document.removeEventListener(event, throttledHandler, true);
      });
    };
  }, [user]);

  // Vérification périodique de la session
  useEffect(() => {
    if (!user) return;

    const interval = setInterval(async () => {
      const isValid = await authService.refreshSession();
      if (!isValid) {
        setUser(null);
        navigate('/login');
        toast({
          title: "Session expirée",
          description: "Votre session a expiré. Veuillez vous reconnecter.",
          variant: "destructive",
        });
      }
    }, 5 * 60 * 1000); // Vérifier toutes les 5 minutes

    return () => clearInterval(interval);
  }, [user, navigate, toast]);

  /**
   * Connexion utilisateur
   */
  const login = useCallback(async (credentials: LoginCredentials): Promise<boolean> => {
    if (!credentials.username?.trim() || !credentials.password) {
      toast({
        title: "Erreur de validation",
        description: "Veuillez remplir tous les champs",
        variant: "destructive",
      });
      return false;
    }

    setIsLoading(true);
    try {
      const response = await authService.login(credentials);
      
      if (response.user) {
        setUser(response.user);
        
        toast({
          title: "Connexion réussie",
          description: `Bienvenue ${response.user.first_name || response.user.username}`,
          variant: "default",
        });

        return true;
      }
      
      return false;
    } catch (error: any) {
      console.error("Erreur de connexion:", error);
      
      toast({
        title: "Échec de la connexion",
        description: error.message || "Une erreur s'est produite lors de la connexion",
        variant: "destructive",
      });
      
      return false;
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  /**
   * Déconnexion utilisateur
   */
  const logout = useCallback(async (): Promise<void> => {
    try {
      await authService.logout();
      setUser(null);
      navigate('/login');
      
      toast({
        title: "Déconnexion réussie",
        description: "Vous avez été déconnecté avec succès",
        variant: "default",
      });
    } catch (error) {
      console.error("Erreur lors de la déconnexion:", error);
      // Forcer la déconnexion même en cas d'erreur
      setUser(null);
      navigate('/login');
    }
  }, [navigate, toast]);

  /**
   * Rafraîchir la session
   */
  const refreshSession = useCallback(async (): Promise<boolean> => {
    try {
      const isValid = await authService.refreshSession();
      if (!isValid) {
        setUser(null);
      }
      return isValid;
    } catch (error) {
      console.error("Erreur lors du rafraîchissement de session:", error);
      setUser(null);
      return false;
    }
  }, []);

  /**
   * Vérifier si l'utilisateur a une permission spécifique
   */
  const hasPermission = useCallback((permission: string): boolean => {
    if (!user || !user.is_active) return false;
    
    // Les admins ont toutes les permissions
    if (user.role === 'admin') return true;
    
    // Vérifier via la configuration des rôles
    return roleHasPermission(user.role, permission);
  }, [user]);

  /**
   * Vérifier si l'utilisateur a au moins une des permissions
   */
  const hasAnyPermission = useCallback((permissions: string[]): boolean => {
    return permissions.some(permission => hasPermission(permission));
  }, [hasPermission]);

  /**
   * Vérifier si l'utilisateur a un rôle spécifique
   */
  const hasRole = useCallback((role: UserRole): boolean => {
    return user?.role === role || false;
  }, [user]);

  /**
   * Vérifier si l'utilisateur a au moins un des rôles
   */
  const hasAnyRole = useCallback((roles: UserRole[]): boolean => {
    return user ? roles.includes(user.role) : false;
  }, [user]);

  /**
   * Utilitaires de rôles
   */
  const isAdmin = useCallback((): boolean => hasRole('admin'), [hasRole]);
  const isManager = useCallback((): boolean => hasRole('manager'), [hasRole]);
  const isServer = useCallback((): boolean => hasRole('server'), [hasRole]);
  const isCashier = useCallback((): boolean => hasRole('cashier'), [hasRole]);

  const contextValue: AuthContextType = {
    // État
    user,
    isAuthenticated: !!user && user.is_active,
    isLoading,
    
    // Actions
    login,
    logout,
    refreshSession,
    
    // Vérifications de permissions
    hasPermission,
    hasAnyPermission,
    hasRole,
    hasAnyRole,
    
    // Utilitaires de rôles
    isAdmin,
    isManager,
    isServer,
    isCashier
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Hook pour utiliser le contexte d'authentification
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth doit être utilisé à l\'intérieur d\'un AuthProvider');
  }
  
  return context;
};

export default useAuth;
