import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useToast } from './use-toast';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: 'admin' | 'manager' | 'server' | 'cashier';
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  last_login?: string;
  date_joined: string;
  isLoggedIn: boolean;
  permissions?: string[];
  sessionExpiry?: number;
  lastActivity?: number;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  forceLogout: () => void;
  isLoading: boolean;
  hasPermission: (permission: string) => boolean;
  isAdmin: () => boolean;
  isManager: () => boolean;
  isServer: () => boolean;
  isCashier: () => boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();
  const { toast } = useToast();
  
  // Durée de session : 1 heure (en millisecondes)
  const SESSION_DURATION = 60 * 60 * 1000; // 1 heure
  const ACTIVITY_CHECK_INTERVAL = 5 * 60 * 1000; // Vérifier toutes les 5 minutes

  useEffect(() => {
    // Vérifier si l'utilisateur est déjà connecté au chargement
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        if (userData.isLoggedIn && !isSessionExpired(userData)) {
          // Définir l'utilisateur immédiatement pour éviter le flash de login
          setUser(userData);
          // Vérifier la validité de la session côté serveur en arrière-plan
          validateSession(userData);
        } else {
          // Session expirée, nettoyer le localStorage
          localStorage.removeItem('user');
          setIsLoading(false);
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des données utilisateur:', error);
        localStorage.removeItem('user');
        setIsLoading(false);
      }
    } else {
      setIsLoading(false);
    }
  }, []);

  // Vérification périodique de l'activité et de la session
  useEffect(() => {
    if (!user) return;

    const activityInterval = setInterval(() => {
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const userData = JSON.parse(storedUser);
          if (isSessionExpired(userData)) {
            handleSessionExpiry();
          }
        } catch (error) {
          console.error('Erreur lors de la vérification de session:', error);
        }
      }
    }, ACTIVITY_CHECK_INTERVAL);

    return () => clearInterval(activityInterval);
  }, [user]);

  // Mise à jour de l'activité utilisateur
  useEffect(() => {
    if (!user) return;

    const updateActivity = () => {
      const now = Date.now();
      const updatedUser = {
        ...user,
        lastActivity: now
      };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
    };

    // Écouter les événements d'activité
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    // Throttle pour éviter trop d'appels
    let lastUpdate = 0;
    const throttledUpdate = () => {
      const now = Date.now();
      if (now - lastUpdate > 30000) { // Mise à jour max toutes les 30 secondes
        lastUpdate = now;
        updateActivity();
      }
    };

    events.forEach(event => {
      document.addEventListener(event, throttledUpdate, true);
    });

    return () => {
      events.forEach(event => {
        document.removeEventListener(event, throttledUpdate, true);
      });
    };
  }, [user]);

  // Vérifier si la session est expirée
  const isSessionExpired = (userData: User): boolean => {
    if (!userData.sessionExpiry) return false;
    return Date.now() > userData.sessionExpiry;
  };

  // Gérer l'expiration de session
  const handleSessionExpiry = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
    toast({
      title: "Session expirée",
      description: "Votre session a expiré après 1 heure d'inactivité. Veuillez vous reconnecter.",
      variant: "destructive",
    });
  };

  // Fonction pour valider la session côté serveur
  const validateSession = async (userData: User) => {
    try {
      const { apiService } = await import('../services/api');
      // Tenter un appel API pour vérifier si la session est toujours valide
      await apiService.get('/accounts/profile/');
      // Si succès, la session est valide - l'utilisateur est déjà défini
      setIsLoading(false);
    } catch (error) {
      // Session invalide, forcer la déconnexion
      console.log('Session expirée, déconnexion automatique');
      handleSessionExpiry();
      setIsLoading(false);
    }
  };

  const login = async (username: string, password: string): Promise<boolean> => {
    if (!username || !password) {
      toast({
        title: "Erreur de validation",
        description: "Veuillez remplir tous les champs",
        variant: "destructive",
      });
      return false;
    }

    setIsLoading(true);
    try {
      const { apiService } = await import('../services/api');

      const response = await apiService.login({
        username: username.toLowerCase(), // Normaliser le nom d'utilisateur
        password: password
      });

      // Stocker les données utilisateur avec le rôle et la session
      const now = Date.now();
      const userData: User = {
        ...response.user,
        role: (response.user.role as 'admin' | 'manager' | 'server' | 'cashier') || 'server',
        permissions: (response.user as any).permissions || [],
        is_active: response.user.is_active ?? true,
        is_staff: response.user.is_staff ?? false,
        is_superuser: response.user.is_superuser ?? false,
        date_joined: response.user.date_joined ?? new Date().toISOString(),
        isLoggedIn: true,
        sessionExpiry: now + SESSION_DURATION,
        lastActivity: now
      };

      // Sauvegarder dans le localStorage
      localStorage.setItem('user', JSON.stringify(userData));
      
      setUser(userData);

      // Notification de succès
      toast({
        title: "Connexion réussie",
        description: `Bienvenue ${response.user.first_name || response.user.username}`,
        variant: "default",
      });

      return true;

    } catch (error: any) {
      console.error("Erreur de connexion:", error);

      // Gestion des erreurs spécifiques
      let errorMessage = "Une erreur s'est produite. Veuillez réessayer.";

      if (error.message.includes('mot de passe incorrect')) {
        errorMessage = "Nom d'utilisateur ou mot de passe incorrect";
      } else if (error.message.includes('serveur')) {
        errorMessage = "Impossible de se connecter au serveur. Veuillez vérifier votre connexion internet.";
      } else if (error.message.includes('compte est désactivé')) {
        errorMessage = "Votre compte est désactivé. Veuillez contacter l'administrateur.";
      }

      toast({
        title: "Échec de la connexion",
        description: errorMessage,
        variant: "destructive",
      });

      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Appel API pour déconnexion côté serveur
      const { apiService } = await import('../services/api');
      await apiService.logout();
    } catch (error) {
      console.error("Erreur lors de la déconnexion:", error);
    }

    // Nettoyage côté client
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');

    toast({
      title: "Déconnexion réussie",
      description: "Vous avez été déconnecté avec succès",
      variant: "default",
    });
  };

  // Fonction pour forcer la déconnexion (appelée en cas d'erreur d'authentification)
  const forceLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
    toast({
      title: "Session expirée",
      description: "Veuillez vous reconnecter",
      variant: "destructive",
    });
  };

  // Prolonger la session lors d'une activité
  const extendSession = () => {
    if (!user) return;
    
    const now = Date.now();
    const updatedUser = {
      ...user,
      sessionExpiry: now + SESSION_DURATION,
      lastActivity: now
    };
    
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
  };

  // Fonctions utilitaires pour vérifier les rôles et permissions
  const hasPermission = (permission: string): boolean => {
    if (!user) return false;
    if (isSessionExpired(user)) {
      handleSessionExpiry();
      return false;
    }
    if (user.role === 'admin') return true; // Les admins ont toutes les permissions
    return user.permissions?.includes(permission) || false;
  };

  const isAdmin = (): boolean => {
    if (!user) return false;
    if (isSessionExpired(user)) {
      handleSessionExpiry();
      return false;
    }
    return user.role === 'admin';
  };

  const isManager = (): boolean => {
    if (!user) return false;
    if (isSessionExpired(user)) {
      handleSessionExpiry();
      return false;
    }
    return user.role === 'manager';
  };

  const isServer = (): boolean => {
    if (!user) return false;
    if (isSessionExpired(user)) {
      handleSessionExpiry();
      return false;
    }
    return user.role === 'server';
  };

  const isCashier = (): boolean => {
    if (!user) return false;
    if (isSessionExpired(user)) {
      handleSessionExpiry();
      return false;
    }
    return user.role === 'cashier';
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      logout, 
      isLoading, 
      forceLogout,
      hasPermission,
      isAdmin,
      isManager,
      isServer,
      isCashier
    }}>
      {children}
    </AuthContext.Provider>
  );
};

function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth doit être utilisé à l\'intérieur d\'un AuthProvider');
  }
  return context;
}

export { useAuth, AuthProvider };