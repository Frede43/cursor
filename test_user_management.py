#!/usr/bin/env python3
"""
Script de test pour la gestion des utilisateurs BarStockWise
Test complet du workflow : création, connexion, permissions, réinitialisation
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"
ADMIN_CREDENTIALS = {
    "email": "admin@barstockwise.com",
    "password": "admin123"
}

class BarStockWiseTestClient:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_user_id = None
        self.test_user_credentials = None
        self.temp_password = None
        
    def log(self, message, level="INFO"):
        """Logger simple avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def admin_login(self):
        """Connexion admin pour les tests"""
        self.log("🔐 Connexion admin...")
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/login/",
                json=ADMIN_CREDENTIALS
            )
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data.get('access')
                self.session.headers.update({
                    'Authorization': f'Bearer {self.admin_token}'
                })
                self.log("✅ Connexion admin réussie")
                return True
            else:
                self.log(f"❌ Échec connexion admin: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur connexion admin: {e}", "ERROR")
            return False
    
    def get_permissions(self):
        """Récupérer la liste des permissions disponibles"""
        self.log("📋 Récupération des permissions...")
        try:
            response = self.session.get(f"{BASE_URL}/accounts/permissions/list/")
            if response.status_code == 200:
                permissions = response.json().get('results', [])
                self.log(f"✅ {len(permissions)} permissions trouvées")
                for perm in permissions[:3]:  # Afficher les 3 premières
                    self.log(f"   - {perm.get('name', 'N/A')}")
                return permissions
            else:
                self.log(f"❌ Erreur récupération permissions: {response.status_code}", "ERROR")
                return []
        except Exception as e:
            self.log(f"❌ Erreur permissions: {e}", "ERROR")
            return []
    
    def create_test_user(self, permissions):
        """Créer un utilisateur de test"""
        self.log("👤 Création d'un utilisateur test...")
        
        # Sélectionner quelques permissions pour le test
        selected_permissions = permissions[:2] if permissions else []
        
        user_data = {
            "first_name": "Jean",
            "last_name": "Testeur",
            "email": "jean.testeur@barstockwise.com",
            "phone": "123456789",
            "role": "staff",
            "permissions": [p['id'] for p in selected_permissions]
        }
        
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/users/",
                json=user_data
            )
            if response.status_code == 201:
                data = response.json()
                self.test_user_id = data.get('id')
                self.test_user_credentials = {
                    "email": user_data["email"],
                    "password": "temp123456"  # Mot de passe par défaut
                }
                self.log(f"✅ Utilisateur créé avec ID: {self.test_user_id}")
                self.log(f"   Email: {user_data['email']}")
                self.log(f"   Permissions: {len(selected_permissions)}")
                return True
            else:
                self.log(f"❌ Échec création utilisateur: {response.status_code}", "ERROR")
                self.log(f"   Réponse: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur création utilisateur: {e}", "ERROR")
            return False
    
    def test_user_login(self):
        """Tester la connexion avec l'utilisateur créé"""
        self.log("🔑 Test de connexion utilisateur...")
        
        # Créer une nouvelle session pour l'utilisateur
        user_session = requests.Session()
        
        try:
            response = user_session.post(
                f"{BASE_URL}/accounts/login/",
                json=self.test_user_credentials
            )
            if response.status_code == 200:
                data = response.json()
                user_token = data.get('access')
                self.log("✅ Connexion utilisateur réussie")
                
                # Tester l'accès au profil
                user_session.headers.update({
                    'Authorization': f'Bearer {user_token}'
                })
                
                profile_response = user_session.get(f"{BASE_URL}/accounts/profile/")
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    self.log(f"✅ Profil accessible: {profile.get('first_name')} {profile.get('last_name')}")
                    
                    # Vérifier les permissions
                    permissions_response = user_session.get(f"{BASE_URL}/accounts/permissions/")
                    if permissions_response.status_code == 200:
                        perms_data = permissions_response.json()
                        user_perms = perms_data.get('permissions', {})
                        self.log(f"✅ Permissions utilisateur récupérées")
                        for category, perms in user_perms.items():
                            if perms:
                                self.log(f"   {category}: {len(perms)} permissions")
                    
                return True
            else:
                self.log(f"❌ Échec connexion utilisateur: {response.status_code}", "ERROR")
                self.log(f"   Réponse: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur connexion utilisateur: {e}", "ERROR")
            return False
    
    def reset_user_password(self):
        """Réinitialiser le mot de passe de l'utilisateur test"""
        self.log("🔄 Réinitialisation du mot de passe...")
        
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/users/{self.test_user_id}/reset-password/"
            )
            if response.status_code == 200:
                data = response.json()
                self.temp_password = data.get('temp_password')
                self.log(f"✅ Mot de passe réinitialisé")
                self.log(f"   Nouveau mot de passe: {self.temp_password}")
                self.log(f"   Format: {data.get('format', 'N/A')}")
                
                # Mettre à jour les credentials
                self.test_user_credentials["password"] = self.temp_password
                return True
            else:
                self.log(f"❌ Échec réinitialisation: {response.status_code}", "ERROR")
                self.log(f"   Réponse: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur réinitialisation: {e}", "ERROR")
            return False
    
    def test_login_with_new_password(self):
        """Tester la connexion avec le nouveau mot de passe"""
        self.log("🔐 Test connexion avec nouveau mot de passe...")
        
        user_session = requests.Session()
        
        try:
            response = user_session.post(
                f"{BASE_URL}/accounts/login/",
                json=self.test_user_credentials
            )
            if response.status_code == 200:
                self.log("✅ Connexion avec nouveau mot de passe réussie")
                
                # Vérifier l'accès aux données
                data = response.json()
                user_token = data.get('access')
                user_session.headers.update({
                    'Authorization': f'Bearer {user_token}'
                })
                
                profile_response = user_session.get(f"{BASE_URL}/accounts/profile/")
                if profile_response.status_code == 200:
                    self.log("✅ Accès au profil confirmé après réinitialisation")
                    return True
                
            else:
                self.log(f"❌ Échec connexion nouveau mot de passe: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Erreur test nouveau mot de passe: {e}", "ERROR")
            return False
    
    def cleanup(self):
        """Nettoyer l'utilisateur de test"""
        if self.test_user_id:
            self.log("🧹 Nettoyage de l'utilisateur test...")
            try:
                response = self.session.delete(f"{BASE_URL}/accounts/users/{self.test_user_id}/")
                if response.status_code in [204, 200]:
                    self.log("✅ Utilisateur test supprimé")
                else:
                    self.log(f"⚠️ Suppression partielle: {response.status_code}")
            except Exception as e:
                self.log(f"⚠️ Erreur nettoyage: {e}", "WARNING")
    
    def run_full_test(self):
        """Exécuter le test complet"""
        self.log("🚀 Début des tests de gestion utilisateur")
        self.log("=" * 50)
        
        success_count = 0
        total_tests = 5
        
        # Test 1: Connexion admin
        if self.admin_login():
            success_count += 1
        
        # Test 2: Récupération permissions
        permissions = self.get_permissions()
        if permissions:
            success_count += 1
        
        # Test 3: Création utilisateur
        if self.create_test_user(permissions):
            success_count += 1
            
            # Test 4: Connexion utilisateur
            if self.test_user_login():
                success_count += 1
                
                # Test 5: Réinitialisation et reconnexion
                if self.reset_user_password():
                    if self.test_login_with_new_password():
                        success_count += 1
        
        # Nettoyage
        self.cleanup()
        
        # Résumé
        self.log("=" * 50)
        self.log(f"📊 RÉSULTATS: {success_count}/{total_tests} tests réussis")
        
        if success_count == total_tests:
            self.log("🎉 TOUS LES TESTS SONT PASSÉS!")
            self.log("✅ Création d'utilisateur fonctionnelle")
            self.log("✅ Connexion utilisateur fonctionnelle")
            self.log("✅ Permissions correctement attribuées")
            self.log("✅ Réinitialisation mot de passe fonctionnelle")
            self.log("✅ Connexion avec nouveau mot de passe fonctionnelle")
        else:
            self.log("❌ Certains tests ont échoué")
            
        return success_count == total_tests

def main():
    """Point d'entrée principal"""
    print("BarStockWise - Test de Gestion Utilisateur")
    print("=" * 50)
    
    client = BarStockWiseTestClient()
    success = client.run_full_test()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
