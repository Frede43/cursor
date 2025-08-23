import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"  # URL de l'API backend
API_URL = f"{BASE_URL}/api"

# Couleurs pour les logs
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text.center(70)}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'=' * 70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️ {text}{Colors.END}")

def login_admin():
    """Se connecter en tant qu'administrateur"""
    print_info("Connexion en tant qu'administrateur...")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{API_URL}/token/", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access")
        print_success("Connexion administrateur réussie")
        return access_token
    else:
        print_error(f"Échec de connexion administrateur: {response.status_code}")
        print_error(f"Réponse: {response.text}")
        sys.exit(1)

def create_test_user(admin_token):
    """Créer un utilisateur de test"""
    print_info("Création d'un nouvel utilisateur de test...")
    
    # Générer un nom d'utilisateur unique avec timestamp
    timestamp = int(time.time())
    username = f"testuser{timestamp}"
    
    user_data = {
        "username": username,
        "first_name": "Test",
        "last_name": "Utilisateur",
        "email": f"{username}@example.com",
        "phone": "123456789",
        "role": "server",
        "password": "temp123456",
        "permissions": []  # Permissions de base
    }
    
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_URL}/accounts/users/", json=user_data, headers=headers)
    
    if response.status_code in [200, 201]:
        user_info = response.json()
        print_success(f"Utilisateur créé avec succès: {username}")
        return {
            "username": username,
            "password": "temp123456",
            "user_id": user_info.get("id")
        }
    else:
        print_error(f"Échec de création d'utilisateur: {response.status_code}")
        print_error(f"Réponse: {response.text}")
        return None

def test_user_login(user_info):
    """Tester la connexion de l'utilisateur créé"""
    print_info(f"Test de connexion pour l'utilisateur {user_info['username']}...")
    
    login_data = {
        "username": user_info["username"],
        "password": user_info["password"]
    }
    
    response = requests.post(f"{API_URL}/token/", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print_success(f"Connexion réussie pour {user_info['username']}")
        return token_data
    else:
        print_error(f"Échec de connexion: {response.status_code}")
        print_error(f"Réponse: {response.text}")
        return None

def get_user_profile(user_token):
    """Récupérer le profil de l'utilisateur connecté"""
    print_info("Récupération du profil utilisateur...")
    
    headers = {
        "Authorization": f"Bearer {user_token['access']}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{API_URL}/accounts/profile/", headers=headers)
    
    if response.status_code == 200:
        profile = response.json()
        print_success("Profil récupéré avec succès")
        return profile
    else:
        print_error(f"Échec de récupération du profil: {response.status_code}")
        print_error(f"Réponse: {response.text}")
        return None

def main():
    print_header("TEST DE CRÉATION ET CONNEXION D'UTILISATEUR")
    
    # 1. Connexion en tant qu'admin
    admin_token = login_admin()
    
    # 2. Création d'un utilisateur de test
    user_info = create_test_user(admin_token)
    if not user_info:
        sys.exit(1)
    
    # 3. Test de connexion avec le nouvel utilisateur
    user_token = test_user_login(user_info)
    if not user_token:
        sys.exit(1)
    
    # 4. Récupération du profil utilisateur
    user_profile = get_user_profile(user_token)
    if user_profile:
        print("\n" + "=" * 50)
        print(f"📊 RÉSUMÉ DU TEST")
        print("=" * 50)
        print(f"\nUtilisateur: {user_profile.get('username', 'N/A')}")
        print(f"Nom complet: {user_profile.get('first_name', '')} {user_profile.get('last_name', '')}")
        print(f"Email: {user_profile.get('email', 'N/A')}")
        print(f"Rôle: {user_profile.get('role', 'N/A')}")
        
        print("\n✅ RÉSULTAT: Le nouvel utilisateur peut se connecter avec succès!")
        print("✅ Le système de création d'utilisateur fonctionne correctement")
        print("✅ Le mot de passe temporaire est valide")
        print("✅ L'utilisateur peut accéder à son profil")
    
if __name__ == "__main__":
    main()