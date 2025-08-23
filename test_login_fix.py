import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def print_success(text):
    print(f"\033[92m✅ {text}\033[0m")

def print_error(text):
    print(f"\033[91m❌ {text}\033[0m")

def print_info(text):
    print(f"\033[93mℹ️ {text}\033[0m")

def test_user_login(username, password):
    """Tester la connexion de l'utilisateur"""
    print_info(f"Test de connexion pour l'utilisateur {username}...")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    # Utiliser l'URL correcte pour la connexion
    response = requests.post(f"{API_URL}/accounts/login/", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        print_success(f"Connexion réussie pour {username}")
        print_info(f"Tokens: {json.dumps(token_data['tokens'], indent=2)}")
        print_info(f"User: {json.dumps(token_data['user'], indent=2)}")
        return token_data
    else:
        print_error(f"Échec de connexion: {response.status_code}")
        print_error(f"Réponse: {response.text}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test_login_fix.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    
    test_user_login(username, password)