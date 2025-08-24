#!/usr/bin/env python
"""
Script pour tester la création d'un utilisateur avec des permissions spécifiques
- Permission de visualiser l'historique des ventes (sales.history)
- Permission de gérer les ventes (sales.create, sales.view)
"""

import os
import sys
import django
import requests
import json

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission
from django.contrib.auth import authenticate

# Configuration API
API_BASE_URL = "http://127.0.0.1:8000"
ADMIN_USERNAME = "admin"  # Remplacez par votre admin
ADMIN_PASSWORD = "admin123"  # Remplacez par votre mot de passe admin

def get_admin_token():
    """Obtenir le token d'authentification admin"""
    login_url = f"{API_BASE_URL}/accounts/login/"
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    print("🔐 Connexion admin...")
    response = requests.post(login_url, json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Connexion admin réussie")
        return data.get('access_token')
    else:
        print(f"❌ Erreur connexion admin: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_test_user_with_permissions():
    """Créer un utilisateur de test avec permissions spécifiques"""
    
    # Obtenir le token admin
    token = get_admin_token()
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Données du nouvel utilisateur
    user_data = {
        "username": "testuser_sales",
        "first_name": "Jean",
        "last_name": "Vendeur",
        "email": "jean.vendeur@barstock.com",
        "phone": "+257 79 123 456",
        "role": "server",
        "password": "temp123456",
        "permissions": [
            "sales.view",      # Voir les ventes
            "sales.create",    # Créer des ventes (gérer les ventes)
            "sales.history"    # Visualiser l'historique des ventes
        ]
    }
    
    print("\n👤 Création de l'utilisateur de test...")
    print(f"   - Nom d'utilisateur: {user_data['username']}")
    print(f"   - Nom complet: {user_data['first_name']} {user_data['last_name']}")
    print(f"   - Email: {user_data['email']}")
    print(f"   - Rôle: {user_data['role']}")
    print(f"   - Permissions: {', '.join(user_data['permissions'])}")
    
    # Créer l'utilisateur via l'API
    create_url = f"{API_BASE_URL}/accounts/users/"
    response = requests.post(create_url, json=user_data, headers=headers)
    
    if response.status_code == 201:
        user_response = response.json()
        print("✅ Utilisateur créé avec succès!")
        print(f"   - ID: {user_response.get('id')}")
        print(f"   - Username: {user_response.get('username')}")
        
        # Vérifier les permissions assignées
        user_id = user_response.get('id')
        permissions_url = f"{API_BASE_URL}/accounts/users/{user_id}/"
        perm_response = requests.get(permissions_url, headers=headers)
        
        if perm_response.status_code == 200:
            user_details = perm_response.json()
            permissions = user_details.get('permissions_by_category', {})
            
            print("\n🔑 Permissions assignées:")
            for category, perms in permissions.items():
                print(f"   - {category.upper()}:")
                for perm in perms:
                    print(f"     • {perm.get('name')} ({perm.get('code')})")
        
        return True
        
    else:
        print(f"❌ Erreur lors de la création: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def verify_user_creation():
    """Vérifier que l'utilisateur a été créé correctement"""
    print("\n🔍 Vérification dans la base de données...")
    
    try:
        user = User.objects.get(username="testuser_sales")
        print(f"✅ Utilisateur trouvé: {user.get_full_name()} ({user.username})")
        print(f"   - Email: {user.email}")
        print(f"   - Rôle: {user.role}")
        print(f"   - Actif: {user.is_active}")
        
        # Vérifier les permissions
        user_permissions = UserPermission.objects.filter(user=user, is_active=True)
        print(f"\n🔑 Permissions en base ({user_permissions.count()}):")
        
        for up in user_permissions:
            print(f"   • {up.permission.name} ({up.permission.code})")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur non trouvé en base")
        return False

def main():
    """Fonction principale"""
    print("🚀 Script de test - Création utilisateur avec permissions")
    print("=" * 60)
    
    # Vérifier si l'utilisateur existe déjà
    try:
        existing_user = User.objects.get(username="testuser_sales")
        print("⚠️  L'utilisateur 'testuser_sales' existe déjà")
        print("   Suppression de l'utilisateur existant...")
        existing_user.delete()
        print("✅ Utilisateur supprimé")
    except User.DoesNotExist:
        pass
    
    # Créer l'utilisateur
    success = create_test_user_with_permissions()
    
    if success:
        # Vérifier la création
        verify_user_creation()
        
        print("\n" + "=" * 60)
        print("✅ SUCCÈS - Utilisateur créé avec les permissions:")
        print("   • sales.view - Voir les ventes")
        print("   • sales.create - Créer des ventes (gérer les ventes)")
        print("   • sales.history - Visualiser l'historique des ventes")
        print("\n📝 Informations de connexion:")
        print("   - Username: testuser_sales")
        print("   - Password: temp123456")
        print("\n🔄 Vous pouvez maintenant tester la connexion avec le script de test de connexion.")
        
    else:
        print("\n❌ ÉCHEC - Impossible de créer l'utilisateur")

if __name__ == '__main__':
    main()
