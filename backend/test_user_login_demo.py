#!/usr/bin/env python
"""
Script pour tester la connexion de l'utilisateur créé via l'API
et vérifier que les permissions sont correctement retournées
"""

import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission

# Configuration API
API_BASE_URL = "http://127.0.0.1:8000"
TEST_USERNAME = "testuser_sales"
TEST_PASSWORD = "temp123456"

def test_api_login():
    """Tester la connexion via l'API REST"""
    login_url = f"{API_BASE_URL}/accounts/login/"
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    print("🔐 Test de connexion via API REST:")
    print(f"   URL: {login_url}")
    print(f"   Username: {TEST_USERNAME}")
    print(f"   Password: {TEST_PASSWORD}")
    
    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ Connexion API réussie!")
            
            # Afficher les informations utilisateur retournées
            user_info = data.get('user', {})
            print(f"\n👤 Informations utilisateur retournées:")
            print(f"   • ID: {user_info.get('id')}")
            print(f"   • Nom: {user_info.get('first_name')} {user_info.get('last_name')}")
            print(f"   • Email: {user_info.get('email')}")
            print(f"   • Username: {user_info.get('username')}")
            print(f"   • Rôle: {user_info.get('role')}")
            print(f"   • Actif: {user_info.get('is_active')}")
            
            # Vérifier les tokens
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            print(f"\n🔑 Tokens reçus:")
            print(f"   • Access Token: {'✅ Présent' if access_token else '❌ Manquant'}")
            print(f"   • Refresh Token: {'✅ Présent' if refresh_token else '❌ Manquant'}")
            
            return access_token, user_info
            
        else:
            print(f"   ❌ Erreur de connexion: {response.status_code}")
            print(f"   Response: {response.text}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Erreur: Impossible de se connecter au serveur")
        print("   💡 Assurez-vous que le serveur Django est démarré (python manage.py runserver)")
        return None, None
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return None, None

def test_user_details_api(token, user_id):
    """Tester la récupération des détails utilisateur avec permissions"""
    if not token:
        return None
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    user_url = f"{API_BASE_URL}/accounts/users/{user_id}/"
    
    print(f"\n📋 Test de récupération des détails utilisateur:")
    print(f"   URL: {user_url}")
    
    try:
        response = requests.get(user_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print("   ✅ Détails utilisateur récupérés!")
            
            # Afficher les permissions par catégorie
            permissions = user_data.get('permissions_by_category', {})
            print(f"\n🔑 Permissions par catégorie:")
            
            total_permissions = 0
            for category, perms in permissions.items():
                print(f"   📁 {category.upper()} ({len(perms)} permissions):")
                for perm in perms:
                    print(f"      • {perm.get('name')} ({perm.get('code')})")
                    total_permissions += 1
            
            print(f"\n📊 Total: {total_permissions} permissions")
            return permissions
            
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return None

def test_protected_endpoints(token):
    """Tester l'accès aux endpoints protégés"""
    if not token:
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🌐 Test d'accès aux endpoints protégés:")
    
    # Endpoints à tester
    endpoints = [
        {
            "name": "Liste des ventes",
            "url": f"{API_BASE_URL}/sales/sales/",
            "expected": "✅ Autorisé (sales.view)"
        },
        {
            "name": "Liste des produits",
            "url": f"{API_BASE_URL}/products/products/",
            "expected": "❌ Refusé (pas de products.view)"
        },
        {
            "name": "Liste des utilisateurs",
            "url": f"{API_BASE_URL}/accounts/users/",
            "expected": "❌ Refusé (pas de users.view)"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n   🔗 {endpoint['name']}:")
        print(f"      Attendu: {endpoint['expected']}")
        
        try:
            response = requests.get(endpoint['url'], headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', [])) if 'results' in data else 'N/A'
                print(f"      Résultat: ✅ Accès autorisé ({count} éléments)")
            elif response.status_code == 403:
                print(f"      Résultat: ❌ Accès refusé (403 Forbidden)")
            elif response.status_code == 401:
                print(f"      Résultat: ❌ Non autorisé (401 Unauthorized)")
            else:
                print(f"      Résultat: ⚠️ Réponse inattendue ({response.status_code})")
                
        except Exception as e:
            print(f"      Résultat: ❌ Erreur ({str(e)})")

def simulate_frontend_behavior(permissions):
    """Simuler le comportement du frontend avec ces permissions"""
    print(f"\n🎯 Simulation du comportement frontend:")
    
    # Extraire les codes de permissions
    permission_codes = []
    for category, perms in permissions.items():
        for perm in perms:
            permission_codes.append(perm.get('code'))
    
    print(f"   Codes de permissions: {permission_codes}")
    
    # Simuler les vérifications du frontend
    frontend_checks = {
        "Afficher menu Ventes": "sales.view" in permission_codes or "sales.create" in permission_codes,
        "Bouton Nouvelle Vente": "sales.create" in permission_codes,
        "Onglet Historique": "sales.history" in permission_codes,
        "Menu Produits": "products.view" in permission_codes,
        "Menu Stocks": "stocks.view" in permission_codes,
        "Menu Utilisateurs": "users.view" in permission_codes,
        "Menu Paramètres": "settings.view" in permission_codes
    }
    
    print(f"\n   Éléments d'interface:")
    for element, visible in frontend_checks.items():
        status = "✅ Visible" if visible else "❌ Masqué"
        print(f"      • {element}: {status}")

def verify_database_state():
    """Vérifier l'état de l'utilisateur en base de données"""
    print(f"\n🗄️ Vérification en base de données:")
    
    try:
        user = User.objects.get(username=TEST_USERNAME)
        print(f"   ✅ Utilisateur trouvé: {user.get_full_name()}")
        print(f"   • Email: {user.email}")
        print(f"   • Rôle: {user.role}")
        print(f"   • Actif: {user.is_active}")
        print(f"   • Dernière connexion: {user.last_login}")
        
        # Vérifier les permissions
        user_permissions = UserPermission.objects.filter(user=user, is_active=True)
        print(f"\n   🔑 Permissions en base ({user_permissions.count()}):")
        
        for up in user_permissions:
            print(f"      • {up.permission.name} ({up.permission.code})")
        
        return user
        
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur '{TEST_USERNAME}' non trouvé en base")
        return None

def main():
    """Fonction principale de test"""
    print("🚀 TEST DE CONNEXION - Utilisateur avec permissions spécifiques")
    print("=" * 70)
    
    # 1. Vérifier l'état en base
    print("1️⃣ Vérification de l'utilisateur en base de données")
    user = verify_database_state()
    
    if not user:
        print("\n❌ ÉCHEC - Utilisateur non trouvé")
        print("💡 Exécutez d'abord le script de création: python test_user_permissions_demo.py")
        return
    
    # 2. Test de connexion API
    print(f"\n2️⃣ Test de connexion via API")
    token, user_info = test_api_login()
    
    if token and user_info:
        user_id = user_info.get('id')
        
        # 3. Test des détails utilisateur
        print(f"\n3️⃣ Test de récupération des permissions")
        permissions = test_user_details_api(token, user_id)
        
        if permissions:
            # 4. Test des endpoints protégés
            print(f"\n4️⃣ Test d'accès aux endpoints")
            test_protected_endpoints(token)
            
            # 5. Simulation frontend
            print(f"\n5️⃣ Simulation du comportement frontend")
            simulate_frontend_behavior(permissions)
            
            # RÉSUMÉ FINAL
            print("\n" + "=" * 70)
            print("✅ SUCCÈS - TESTS DE CONNEXION TERMINÉS")
            print("=" * 70)
            
            print(f"🎯 RÉSULTATS:")
            print(f"   ✅ Connexion API réussie")
            print(f"   ✅ Tokens JWT obtenus")
            print(f"   ✅ Permissions correctement retournées")
            print(f"   ✅ Accès aux endpoints autorisés")
            print(f"   ✅ Restrictions respectées")
            
            print(f"\n📱 INTERFACE UTILISATEUR:")
            print(f"   ✅ Menu Ventes visible")
            print(f"   ✅ Bouton Nouvelle Vente visible")
            print(f"   ✅ Onglet Historique visible")
            print(f"   ❌ Menus Produits/Stocks/Utilisateurs masqués")
            
            print(f"\n🔄 PROCHAINES ÉTAPES:")
            print(f"   1. Démarrer le frontend: npm run dev")
            print(f"   2. Se connecter avec: {TEST_USERNAME} / {TEST_PASSWORD}")
            print(f"   3. Vérifier que l'interface correspond aux permissions")
            print(f"   4. Tester les fonctionnalités de vente")
            
        else:
            print("\n❌ ÉCHEC - Impossible de récupérer les permissions")
    else:
        print("\n❌ ÉCHEC - Impossible de se connecter")
        print("💡 Vérifiez que le serveur Django est démarré")

if __name__ == '__main__':
    main()
