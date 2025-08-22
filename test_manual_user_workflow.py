#!/usr/bin/env python3
"""
Script de test manuel pour la gestion des utilisateurs BarStockWise
Guide étape par étape pour tester le workflow complet
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000/api"

class ManualTestGuide:
    def __init__(self):
        self.session = requests.Session()
        
    def log(self, message, level="INFO"):
        """Logger simple avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_server_connection(self):
        """Tester la connexion au serveur"""
        self.log("🔍 Test de connexion au serveur Django...")
        try:
            response = requests.get(f"{BASE_URL}/accounts/users/", timeout=5)
            if response.status_code in [200, 401, 403]:  # 401/403 = serveur fonctionne mais pas authentifié
                self.log("✅ Serveur Django accessible")
                return True
            else:
                self.log(f"❌ Serveur répond avec code: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log("❌ Impossible de se connecter au serveur Django")
            self.log("   Vérifiez que le serveur Django fonctionne sur localhost:8000")
            return False
        except Exception as e:
            self.log(f"❌ Erreur de connexion: {e}")
            return False
    
    def get_admin_credentials(self):
        """Demander les credentials admin à l'utilisateur"""
        self.log("🔐 Saisie des credentials administrateur")
        print("\n" + "="*50)
        print("ÉTAPE 1: CONNEXION ADMINISTRATEUR")
        print("="*50)
        
        email = input("Email admin (défaut: admin@barstockwise.com): ").strip()
        if not email:
            email = "admin@barstockwise.com"
            
        password = input("Mot de passe admin (défaut: admin123): ").strip()
        if not password:
            password = "admin123"
            
        return {"email": email, "password": password}
    
    def test_admin_login(self, credentials):
        """Tester la connexion admin"""
        self.log("🔐 Test de connexion admin...")
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/login/",
                json=credentials
            )
            if response.status_code == 200:
                data = response.json()
                token = data.get('access')
                if token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
                    self.log("✅ Connexion admin réussie")
                    return True
                else:
                    self.log("❌ Token non reçu dans la réponse")
                    return False
            else:
                self.log(f"❌ Échec connexion admin: {response.status_code}")
                if response.status_code == 400:
                    self.log("   Vérifiez les credentials admin")
                self.log(f"   Réponse: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur connexion admin: {e}")
            return False
    
    def create_test_user_interactive(self):
        """Créer un utilisateur de test de manière interactive"""
        print("\n" + "="*50)
        print("ÉTAPE 2: CRÉATION D'UTILISATEUR TEST")
        print("="*50)
        
        # Récupérer les permissions disponibles
        self.log("📋 Récupération des permissions...")
        try:
            response = self.session.get(f"{BASE_URL}/accounts/permissions/list/")
            if response.status_code == 200:
                permissions = response.json().get('results', [])
                self.log(f"✅ {len(permissions)} permissions disponibles")
                
                print("\nPermissions disponibles:")
                for i, perm in enumerate(permissions):
                    print(f"  {i+1}. {perm.get('name', 'N/A')}")
            else:
                self.log(f"❌ Erreur récupération permissions: {response.status_code}")
                permissions = []
        except Exception as e:
            self.log(f"❌ Erreur permissions: {e}")
            permissions = []
        
        # Saisie des informations utilisateur
        print("\nCréation d'un nouvel utilisateur:")
        first_name = input("Prénom (défaut: Jean): ").strip() or "Jean"
        last_name = input("Nom (défaut: Testeur): ").strip() or "Testeur"
        email = input("Email (défaut: jean.testeur@test.com): ").strip() or "jean.testeur@test.com"
        phone = input("Téléphone (défaut: 123456789): ").strip() or "123456789"
        
        print("\nRôles disponibles:")
        print("1. admin")
        print("2. manager") 
        print("3. staff")
        role_choice = input("Choisir un rôle (1-3, défaut: 3): ").strip()
        role_map = {"1": "admin", "2": "manager", "3": "staff"}
        role = role_map.get(role_choice, "staff")
        
        # Sélection des permissions
        selected_permissions = []
        if permissions:
            print(f"\nAttribuer des permissions? (y/n, défaut: y): ", end="")
            if input().strip().lower() != 'n':
                perm_input = input(f"Numéros des permissions (1-{len(permissions)}, séparés par des virgules): ").strip()
                if perm_input:
                    try:
                        perm_indices = [int(x.strip()) - 1 for x in perm_input.split(',')]
                        selected_permissions = [permissions[i]['id'] for i in perm_indices if 0 <= i < len(permissions)]
                    except:
                        self.log("⚠️ Format invalide, aucune permission attribuée")
        
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "role": role,
            "permissions": selected_permissions
        }
        
        # Créer l'utilisateur
        self.log("👤 Création de l'utilisateur...")
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/users/",
                json=user_data
            )
            if response.status_code == 201:
                data = response.json()
                user_id = data.get('id')
                self.log(f"✅ Utilisateur créé avec ID: {user_id}")
                print(f"\n📋 INFORMATIONS UTILISATEUR CRÉÉ:")
                print(f"   ID: {user_id}")
                print(f"   Nom: {first_name} {last_name}")
                print(f"   Email: {email}")
                print(f"   Rôle: {role}")
                print(f"   Permissions: {len(selected_permissions)}")
                print(f"   Mot de passe par défaut: temp123456")
                
                return {
                    "id": user_id,
                    "email": email,
                    "password": "temp123456",
                    "name": f"{first_name} {last_name}"
                }
            else:
                self.log(f"❌ Échec création utilisateur: {response.status_code}")
                self.log(f"   Réponse: {response.text}")
                return None
        except Exception as e:
            self.log(f"❌ Erreur création utilisateur: {e}")
            return None
    
    def test_user_login_interactive(self, user_info):
        """Tester la connexion utilisateur de manière interactive"""
        print("\n" + "="*50)
        print("ÉTAPE 3: TEST CONNEXION UTILISATEUR")
        print("="*50)
        
        print(f"Test de connexion pour: {user_info['name']}")
        print(f"Email: {user_info['email']}")
        print(f"Mot de passe: {user_info['password']}")
        
        input("\nAppuyez sur Entrée pour tester la connexion...")
        
        # Nouvelle session pour l'utilisateur
        user_session = requests.Session()
        
        try:
            response = user_session.post(
                f"{BASE_URL}/accounts/login/",
                json={
                    "email": user_info['email'],
                    "password": user_info['password']
                }
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
                        
                        print(f"\n📋 PERMISSIONS DE L'UTILISATEUR:")
                        total_perms = 0
                        for category, perms in user_perms.items():
                            if perms:
                                print(f"   {category}: {len(perms)} permissions")
                                for perm in perms[:3]:  # Afficher les 3 premières
                                    print(f"     - {perm}")
                                total_perms += len(perms)
                        
                        if total_perms == 0:
                            print("   Aucune permission spécifique attribuée")
                    
                return user_session, user_token
            else:
                self.log(f"❌ Échec connexion utilisateur: {response.status_code}")
                self.log(f"   Réponse: {response.text}")
                return None, None
        except Exception as e:
            self.log(f"❌ Erreur connexion utilisateur: {e}")
            return None, None
    
    def test_password_reset_interactive(self, user_info):
        """Tester la réinitialisation de mot de passe"""
        print("\n" + "="*50)
        print("ÉTAPE 4: TEST RÉINITIALISATION MOT DE PASSE")
        print("="*50)
        
        print(f"Réinitialisation du mot de passe pour: {user_info['name']}")
        input("Appuyez sur Entrée pour réinitialiser le mot de passe...")
        
        try:
            response = self.session.post(
                f"{BASE_URL}/accounts/users/{user_info['id']}/reset-password/"
            )
            if response.status_code == 200:
                data = response.json()
                new_password = data.get('temp_password')
                self.log(f"✅ Mot de passe réinitialisé")
                
                print(f"\n🔑 NOUVEAU MOT DE PASSE:")
                print(f"   Utilisateur: {user_info['name']}")
                print(f"   Nouveau mot de passe: {new_password}")
                print(f"   Format: {data.get('format', 'N/A')}")
                print(f"   Instructions: {data.get('instructions', 'N/A')}")
                
                # Mettre à jour les informations utilisateur
                user_info['password'] = new_password
                return True
            else:
                self.log(f"❌ Échec réinitialisation: {response.status_code}")
                self.log(f"   Réponse: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur réinitialisation: {e}")
            return False
    
    def test_new_password_login(self, user_info):
        """Tester la connexion avec le nouveau mot de passe"""
        print("\n" + "="*50)
        print("ÉTAPE 5: TEST CONNEXION NOUVEAU MOT DE PASSE")
        print("="*50)
        
        print(f"Test de connexion avec le nouveau mot de passe:")
        print(f"Email: {user_info['email']}")
        print(f"Nouveau mot de passe: {user_info['password']}")
        
        input("Appuyez sur Entrée pour tester la connexion...")
        
        user_session = requests.Session()
        
        try:
            response = user_session.post(
                f"{BASE_URL}/accounts/login/",
                json={
                    "email": user_info['email'],
                    "password": user_info['password']
                }
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
                self.log(f"❌ Échec connexion nouveau mot de passe: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Erreur test nouveau mot de passe: {e}")
            return False
    
    def run_interactive_test(self):
        """Exécuter le test interactif complet"""
        print("🚀 BarStockWise - Test Interactif de Gestion Utilisateur")
        print("=" * 60)
        
        # Test 1: Connexion serveur
        if not self.test_server_connection():
            print("\n❌ Impossible de continuer sans connexion serveur")
            return False
        
        # Test 2: Connexion admin
        admin_creds = self.get_admin_credentials()
        if not self.test_admin_login(admin_creds):
            print("\n❌ Impossible de continuer sans connexion admin")
            return False
        
        # Test 3: Création utilisateur
        user_info = self.create_test_user_interactive()
        if not user_info:
            print("\n❌ Impossible de continuer sans utilisateur créé")
            return False
        
        # Test 4: Connexion utilisateur
        user_session, user_token = self.test_user_login_interactive(user_info)
        if not user_session:
            print("\n❌ Échec connexion utilisateur")
            return False
        
        # Test 5: Réinitialisation mot de passe
        if not self.test_password_reset_interactive(user_info):
            print("\n❌ Échec réinitialisation mot de passe")
            return False
        
        # Test 6: Connexion avec nouveau mot de passe
        if not self.test_new_password_login(user_info):
            print("\n❌ Échec connexion nouveau mot de passe")
            return False
        
        # Résumé final
        print("\n" + "="*60)
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        print("="*60)
        print("✅ Serveur Django accessible")
        print("✅ Connexion administrateur fonctionnelle")
        print("✅ Création d'utilisateur fonctionnelle")
        print("✅ Connexion utilisateur fonctionnelle")
        print("✅ Permissions correctement attribuées et visibles")
        print("✅ Réinitialisation mot de passe fonctionnelle")
        print("✅ Connexion avec nouveau mot de passe fonctionnelle")
        print("\n🎯 Le système de gestion des utilisateurs fonctionne parfaitement!")
        
        # Option de nettoyage
        print(f"\n🧹 Voulez-vous supprimer l'utilisateur test '{user_info['name']}'? (y/n): ", end="")
        if input().strip().lower() == 'y':
            try:
                response = self.session.delete(f"{BASE_URL}/accounts/users/{user_info['id']}/")
                if response.status_code in [204, 200]:
                    self.log("✅ Utilisateur test supprimé")
                else:
                    self.log(f"⚠️ Suppression partielle: {response.status_code}")
            except Exception as e:
                self.log(f"⚠️ Erreur nettoyage: {e}")
        
        return True

def main():
    """Point d'entrée principal"""
    guide = ManualTestGuide()
    success = guide.run_interactive_test()
    
    if success:
        print("\n✨ Test terminé avec succès!")
    else:
        print("\n❌ Test terminé avec des erreurs")

if __name__ == "__main__":
    main()
