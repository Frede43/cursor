/**
 * Service d'authentification professionnel
 */

import { LoginCredentials, LoginResponse, User, UserRole } from '@/types/auth';
import { apiService } from './api';

const AUTH_STORAGE_KEY = 'barstock_auth';
const SESSION_DURATION = 8 * 60 * 60 * 1000; // 8 heures

interface StoredAuthData {
  user: User;
  sessionExpiry: number;
  lastActivity: number;
}

export class AuthService {
  private static instance: AuthService;
  
  private constructor() {}
  
  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  /**
   * Connexion utilisateur
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await apiService.login({
        username: credentials.username.toLowerCase().trim(),
        password: credentials.password
      });

      if (response?.user) {
        const authData: StoredAuthData = {
          user: {
            ...response.user,
            role: response.user.role as UserRole
          },
          sessionExpiry: Date.now() + SESSION_DURATION,
          lastActivity: Date.now()
        };
        
        this.storeAuthData(authData);
        return {
          ...response,
          user: {
            ...response.user,
            role: response.user.role as UserRole
          }
        };
      }
      
      throw new Error('Réponse de connexion invalide');
    } catch (error: any) {
      console.error('Erreur de connexion:', error);
      throw this.handleAuthError(error);
    }
  }

  /**
   * Déconnexion utilisateur
   */
  async logout(): Promise<void> {
    try {
      await apiService.logout();
    } catch (error) {
      console.warn('Erreur lors de la déconnexion côté serveur:', error);
    } finally {
      this.clearAuthData();
    }
  }

  /**
   * Récupérer l'utilisateur actuel depuis le stockage
   */
  getCurrentUser(): User | null {
    const authData = this.getStoredAuthData();
    
    if (!authData) {
      return null;
    }

    if (this.isSessionExpired(authData)) {
      this.clearAuthData();
      return null;
    }

    // Mettre à jour l'activité
    this.updateActivity();
    return authData.user;
  }

  /**
   * Vérifier si l'utilisateur est connecté
   */
  isAuthenticated(): boolean {
    return this.getCurrentUser() !== null;
  }

  /**
   * Rafraîchir la session
   */
  async refreshSession(): Promise<boolean> {
    try {
      const authData = this.getStoredAuthData();
      if (!authData) {
        return false;
      }

      // Vérifier la validité côté serveur
      await apiService.get('/accounts/profile/');
      
      // Étendre la session
      authData.sessionExpiry = Date.now() + SESSION_DURATION;
      authData.lastActivity = Date.now();
      this.storeAuthData(authData);
      
      return true;
    } catch (error) {
      console.error('Erreur lors du rafraîchissement de session:', error);
      this.clearAuthData();
      return false;
    }
  }

  /**
   * Mettre à jour l'activité utilisateur
   */
  updateActivity(): void {
    const authData = this.getStoredAuthData();
    if (authData) {
      authData.lastActivity = Date.now();
      this.storeAuthData(authData);
    }
  }

  /**
   * Vérifier si la session est expirée
   */
  private isSessionExpired(authData: StoredAuthData): boolean {
    const now = Date.now();
    const sessionExpired = now > authData.sessionExpiry;
    const inactivityTimeout = now - authData.lastActivity > (2 * 60 * 60 * 1000); // 2h d'inactivité
    
    return sessionExpired || inactivityTimeout;
  }

  /**
   * Stocker les données d'authentification
   */
  private storeAuthData(authData: StoredAuthData): void {
    try {
      localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(authData));
    } catch (error) {
      console.error('Erreur lors du stockage des données d\'authentification:', error);
    }
  }

  /**
   * Récupérer les données d'authentification stockées
   */
  private getStoredAuthData(): StoredAuthData | null {
    try {
      const stored = localStorage.getItem(AUTH_STORAGE_KEY);
      if (!stored) {
        return null;
      }
      
      const parsed = JSON.parse(stored);
      
      // Validation des données
      if (!parsed.user || !parsed.sessionExpiry || !parsed.lastActivity) {
        this.clearAuthData();
        return null;
      }
      
      return parsed;
    } catch (error) {
      console.error('Erreur lors de la récupération des données d\'authentification:', error);
      this.clearAuthData();
      return null;
    }
  }

  /**
   * Nettoyer les données d'authentification
   */
  private clearAuthData(): void {
    try {
      localStorage.removeItem(AUTH_STORAGE_KEY);
    } catch (error) {
      console.error('Erreur lors du nettoyage des données d\'authentification:', error);
    }
  }

  /**
   * Gérer les erreurs d'authentification
   */
  private handleAuthError(error: any): Error {
    if (error.message?.includes('401') || error.message?.includes('Unauthorized')) {
      return new Error('Nom d\'utilisateur ou mot de passe incorrect');
    }
    
    if (error.message?.includes('403') || error.message?.includes('Forbidden')) {
      return new Error('Compte désactivé. Contactez l\'administrateur');
    }
    
    if (error.message?.includes('Network') || error.message?.includes('fetch')) {
      return new Error('Impossible de se connecter au serveur. Vérifiez votre connexion');
    }
    
    return new Error(error.message || 'Erreur de connexion inconnue');
  }
}

// Instance singleton
export const authService = AuthService.getInstance();
