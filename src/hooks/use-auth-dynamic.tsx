import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthState, LoginCredentials } from '@/types/auth';
import { apiService } from '@/services/api';

interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<boolean>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Vérifier l'authentification au chargement
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const storedUser = localStorage.getItem('user');
      const accessToken = localStorage.getItem('access_token');
      
      if (storedUser && accessToken) {
        const userData = JSON.parse(storedUser);
        
        // Vérifier si le token est encore valide
        try {
          const response = await fetch('http://localhost:8000/api/accounts/profile/', {
            headers: {
              'Authorization': `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            }
          });
          
          if (response.ok) {
            setUser(userData);
            // Configurer le token dans le service API
            apiService.setTokens(
              accessToken, 
              localStorage.getItem('refresh_token') || ''
            );
            
            // Vérifier si nous sommes sur la page de login et rediriger si nécessaire
            if (window.location.pathname === '/login') {
              // Rediriger selon le rôle
              window.location.href = userData.role === 'cashier' ? '/sales' : '/';
            }
          } else {
            // Token invalide, nettoyer les données
            clearAuthData();
          }
        } catch (tokenError) {
          // Erreur de vérification du token, nettoyer
          clearAuthData();
        }
      }
    } catch (error) {
      console.error('Erreur lors de la vérification de l\'authentification:', error);
      clearAuthData();
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      setIsLoading(true);
      
      const response = await fetch('http://localhost:8000/api/accounts/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: credentials.username.toLowerCase().trim(),
          password: credentials.password
        })
      });

      if (response.ok) {
        const data = await response.json();
        
        // Debug: vérifier les permissions reçues
        console.log('DEBUG - Données utilisateur reçues:', data.user);
        console.log('DEBUG - Permissions dans data.user:', data.user.permissions);
        
        // Stocker les données d'authentification
        localStorage.setItem('access_token', data.tokens.access);
        localStorage.setItem('refresh_token', data.tokens.refresh);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Mettre à jour l'état
        setUser(data.user);
        
        // Configurer les tokens dans le service API
        apiService.setTokens(data.tokens.access, data.tokens.refresh);
        
        // Forcer un rafraîchissement de la page pour déclencher la redirection
        window.location.href = data.user.role === 'cashier' ? '/sales' : '/';
        
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Erreur de connexion:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async (): Promise<void> => {
    try {
      // Appeler l'endpoint de déconnexion si disponible
      await fetch('http://localhost:8000/api/accounts/logout/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json',
        }
      });
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error);
    } finally {
      clearAuthData();
    }
  };

  const refreshSession = async (): Promise<boolean> => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return false;

      const response = await fetch('http://localhost:8000/api/accounts/token/refresh/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh: refreshToken
        })
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access);
        
        // Mettre à jour le token dans le service API
        apiService.setTokens(data.access, refreshToken);
        
        return true;
      }
      
      return false;
    } catch (error) {
      console.error('Erreur lors du rafraîchissement de session:', error);
      return false;
    }
  };

  const clearAuthData = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    apiService.clearTokens();
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    refreshSession
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth doit être utilisé à l\'intérieur d\'un AuthProvider');
  }
  return context;
}
