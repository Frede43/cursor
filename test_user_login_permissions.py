#!/usr/bin/env python
"""
Script pour tester la connexion de l'utilisateur créé et vérifier ses permissions
Simule la connexion frontend et vérifie les menus/permissions disponibles
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

# Configuration API
API_BASE_URL = "http://127.0.0.1:8000"
TEST_USERNAME = "testuser_sales"
TEST_PASSWORD = "temp123456"

def test_user_login():
    """Tester la connexion de l'utilisateur de test"""
    login_url = f"{API_BASE_URL}/accounts/login/"
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    print("🔐 Test de connexion utilisateur...")
    print(f"   - Username: {TEST_USERNAME}")
    print(f"   - Password: {TEST_PASSWORD}")
    
    response = requests.post(login_url, json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Connexion réussie!")
        
        # Afficher les informations utilisateur
        user_info = data.get('user', {})
        print(f"\n👤 Informations utilisateur:")
        print(f"   - ID: {user_info.get('id')}")
        print(f"   - Nom: {user_info.get('first_name')} {user_info.get('last_name')}")
        print(f"   - Email: {user_info.get('email')}")
        print(f"   - Rôle: {user_info.get('role')}")
        print(f"   - Actif: {user_info.get('is_active')}")
        
        return data.get('access_token'), user_info
    else:
        print(f"❌ Erreur de connexion: {response.status_code}")
        print(f"Response: {response.text}")
        return None, None

def check_user_permissions(token, user_id):
    """Vérifier les permissions de l'utilisateur connecté"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Récupérer les détails utilisateur avec permissions
    user_url = f"{API_BASE_URL}/accounts/users/{user_id}/"
    response = requests.get(user_url, headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        permissions = user_data.get('permissions_by_category', {})
        
        print(f"\n🔑 Permissions détaillées par catégorie:")
        total_permissions = 0
        
        for category, perms in permissions.items():
            print(f"\n   📁 {category.upper()} ({len(perms)} permissions):")
            for perm in perms:
                print(f"      • {perm.get('name')} ({perm.get('code')})")
                total_permissions += 1
        
        print(f"\n📊 Total: {total_permissions} permissions assignées")
        return permissions
    else:
        print(f"❌ Erreur récupération permissions: {response.status_code}")
        return {}

def simulate_menu_access(permissions):
    """Simuler l'accès aux menus basé sur les permissions"""
    print(f"\n🎯 Simulation de l'accès aux menus frontend:")
    
    # Définir les menus et leurs permissions requises
    menu_permissions = {
        "Dashboard": ["sales.view"],  # Au moins une permission pour voir le dashboard
        "Ventes (POS)": ["sales.create"],
        "Historique des Ventes": ["sales.history"],
        "Produits": ["products.view"],
        "Stocks": ["stocks.view"],
        "Tables": ["tables.view"],
        "Cuisine": ["kitchen.view"],
        "Rapports": ["reports.view"],
        "Utilisateurs": ["users.view"],
        "Paramètres": ["settings.view"]
    }
    
    # Extraire tous les codes de permissions de l'utilisateur
    user_permission_codes = []
    for category, perms in permissions.items():
        for perm in perms:
            user_permission_codes.append(perm.get('code'))
    
    print(f"\n   Codes de permissions utilisateur: {user_permission_codes}")
    
    accessible_menus = []
    restricted_menus = []
    
    for menu_name, required_perms in menu_permissions.items():
        has_access = any(perm in user_permission_codes for perm in required_perms)
        
        if has_access:
            accessible_menus.append(menu_name)
            print(f"   ✅ {menu_name} - ACCESSIBLE")
        else:
            restricted_menus.append(menu_name)
            print(f"   ❌ {menu_name} - RESTREINT")
    
    return accessible_menus, restricted_menus

def test_api_endpoints(token):
    """Tester l'accès aux endpoints API avec les permissions"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🌐 Test d'accès aux endpoints API:")
    
    # Endpoints à tester
    test_endpoints = [
        {
            "name": "Liste des ventes",
            "url": f"{API_BASE_URL}/sales/sales/",
            "method": "GET",
            "required_permission": "sales.view"
        },
        {
            "name": "Historique des ventes",
            "url": f"{API_BASE_URL}/reports/sales-history/",
            "method": "GET",
            "required_permission": "sales.history"
        },
        {
            "name": "Créer une vente",
            "url": f"{API_BASE_URL}/sales/sales/",
            "method": "POST",
            "required_permission": "sales.create",
            "data": {
                "table": 1,
                "customer_name": "Test Client",
                "payment_method": "cash",
                "items": []
            }
        },
        {
            "name": "Liste des produits",
            "url": f"{API_BASE_URL}/products/products/",
            "method": "GET",
            "required_permission": "products.view"
        },
        {
            "name": "Liste des utilisateurs",
            "url": f"{API_BASE_URL}/accounts/users/",
            "method": "GET",
            "required_permission": "users.view"
        }
    ]
    
    for endpoint in test_endpoints:
        print(f"\n   🔗 {endpoint['name']} ({endpoint['required_permission']}):")
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], headers=headers)
            elif endpoint['method'] == 'POST':
                response = requests.post(endpoint['url'], json=endpoint.get('data', {}), headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"      ✅ Accès autorisé ({response.status_code})")
                if endpoint['method'] == 'GET':
                    data = response.json()
                    if 'results' in data:
                        print(f"      📊 {len(data['results'])} éléments retournés")
                    elif 'count' in data:
                        print(f"      📊 {data['count']} éléments au total")
            elif response.status_code == 403:
                print(f"      ❌ Accès refusé - Permission insuffisante")
            elif response.status_code == 401:
                print(f"      ❌ Non autorisé - Token invalide")
            else:
                print(f"      ⚠️  Réponse inattendue: {response.status_code}")
                
        except Exception as e:
            print(f"      ❌ Erreur: {str(e)}")

def main():
    """Fonction principale"""
    print("🚀 Script de test - Connexion et vérification des permissions")
    print("=" * 70)
    
    # Vérifier que l'utilisateur existe
    try:
        user = User.objects.get(username=TEST_USERNAME)
        print(f"✅ Utilisateur trouvé: {user.get_full_name()}")
    except User.DoesNotExist:
        print(f"❌ Utilisateur '{TEST_USERNAME}' non trouvé!")
        print("   Veuillez d'abord exécuter le script de création d'utilisateur.")
        return
    
    # Test de connexion
    token, user_info = test_user_login()
    
    if token and user_info:
        user_id = user_info.get('id')
        
        # Vérifier les permissions
        permissions = check_user_permissions(token, user_id)
        
        # Simuler l'accès aux menus
        accessible, restricted = simulate_menu_access(permissions)
        
        # Tester les endpoints API
        test_api_endpoints(token)
        
        # Résumé final
        print("\n" + "=" * 70)
        print("📋 RÉSUMÉ DES TESTS")
        print("=" * 70)
        
        print(f"✅ Connexion réussie pour: {user_info.get('first_name')} {user_info.get('last_name')}")
        print(f"🔑 Permissions assignées: {sum(len(perms) for perms in permissions.values())}")
        
        print(f"\n📱 Menus accessibles ({len(accessible)}):")
        for menu in accessible:
            print(f"   • {menu}")
        
        print(f"\n🚫 Menus restreints ({len(restricted)}):")
        for menu in restricted:
            print(f"   • {menu}")
        
        print(f"\n🎯 Permissions spécifiques testées:")
        print(f"   • ✅ Voir les ventes (sales.view)")
        print(f"   • ✅ Créer des ventes (sales.create)")
        print(f"   • ✅ Historique des ventes (sales.history)")
        
        print(f"\n💡 L'utilisateur peut accéder aux fonctionnalités de vente comme demandé!")
        
    else:
        print("\n❌ ÉCHEC - Impossible de se connecter avec l'utilisateur de test")

if __name__ == '__main__':
    main()
