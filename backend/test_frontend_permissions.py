#!/usr/bin/env python
"""
Script pour tester l'API des permissions et vérifier que Sales apparaît dans le frontend
"""

import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission, User
from django.contrib.auth import authenticate

def test_permissions_api():
    """Tester l'API des permissions"""
    print("🔍 TEST DE L'API DES PERMISSIONS")
    print("=" * 40)
    
    # 1. Obtenir un token d'authentification
    print("1️⃣ Authentification...")
    
    try:
        # Authentifier avec testuser_sales
        user = authenticate(username="testuser_sales", password="temp123456")
        if not user:
            print("   ❌ Échec d'authentification")
            return False
        
        print(f"   ✅ Utilisateur authentifié: {user.get_full_name()}")
        
        # Simuler l'appel API pour récupérer les permissions
        print(f"\n2️⃣ Récupération des permissions via API...")
        
        # URL de l'API (à adapter selon votre configuration)
        base_url = "http://127.0.0.1:8000"
        
        # Test de connexion pour obtenir le token
        login_data = {
            "username": "testuser_sales",
            "password": "temp123456"
        }
        
        try:
            response = requests.post(f"{base_url}/api/auth/login/", json=login_data, timeout=5)
            if response.status_code == 200:
                token_data = response.json()
                token = token_data.get('access_token') or token_data.get('access')
                print(f"   ✅ Token obtenu")
                
                # Récupérer les permissions
                headers = {"Authorization": f"Bearer {token}"}
                perms_response = requests.get(f"{base_url}/api/permissions/", headers=headers, timeout=5)
                
                if perms_response.status_code == 200:
                    permissions_data = perms_response.json()
                    print(f"   ✅ Permissions récupérées: {len(permissions_data)} permissions")
                    
                    # Analyser les catégories
                    categories = {}
                    for perm in permissions_data:
                        category = perm.get('category', 'unknown')
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(perm)
                    
                    print(f"\n📁 CATÉGORIES DISPONIBLES:")
                    for category, perms in categories.items():
                        print(f"   • {category}: {len(perms)} permissions")
                        if category == 'sales':
                            print(f"     └─ Sales trouvé! ✅")
                            for perm in perms[:3]:  # Afficher les 3 premières
                                print(f"        - {perm.get('code')} - {perm.get('name')}")
                    
                    return 'sales' in categories
                else:
                    print(f"   ❌ Erreur API permissions: {perms_response.status_code}")
            else:
                print(f"   ❌ Erreur login: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Serveur non accessible: {str(e)}")
            print(f"   💡 Vérifiez que le serveur Django est démarré")
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
    
    return False

def test_permissions_direct():
    """Tester les permissions directement en base"""
    print(f"\n🔍 TEST DIRECT EN BASE DE DONNÉES")
    print("=" * 40)
    
    # Récupérer toutes les permissions
    all_permissions = Permission.objects.all().order_by('category', 'code')
    
    # Grouper par catégorie
    categories = {}
    for perm in all_permissions:
        if perm.category not in categories:
            categories[perm.category] = []
        categories[perm.category].append(perm)
    
    print(f"📊 TOTAL: {all_permissions.count()} permissions dans {len(categories)} catégories")
    
    for category, perms in categories.items():
        print(f"\n📁 {category.upper()} ({len(perms)} permissions)")
        for perm in perms:
            print(f"   • {perm.code} - {perm.name}")
    
    # Vérifier spécifiquement Sales
    sales_permissions = Permission.objects.filter(category='sales')
    print(f"\n🎯 FOCUS SUR SALES:")
    print(f"   • Nombre de permissions Sales: {sales_permissions.count()}")
    
    if sales_permissions.exists():
        print(f"   ✅ Catégorie Sales trouvée!")
        for perm in sales_permissions:
            print(f"      - {perm.code} - {perm.name}")
        return True
    else:
        print(f"   ❌ Aucune permission Sales trouvée")
        return False

def simulate_frontend_permissions():
    """Simuler la récupération des permissions côté frontend"""
    print(f"\n🎨 SIMULATION FRONTEND")
    print("=" * 40)
    
    # Simuler la structure que le frontend attend
    permissions = Permission.objects.all().order_by('category', 'code')
    
    # Convertir en format JSON comme l'API
    permissions_json = []
    for perm in permissions:
        permissions_json.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    # Grouper par catégorie pour l'affichage frontend
    categories_for_frontend = {}
    for perm in permissions_json:
        category = perm['category']
        if category not in categories_for_frontend:
            categories_for_frontend[category] = []
        categories_for_frontend[category].append(perm)
    
    print(f"📋 STRUCTURE POUR LE FRONTEND:")
    print(f"   • Total permissions: {len(permissions_json)}")
    print(f"   • Catégories: {list(categories_for_frontend.keys())}")
    
    # Vérifier que Sales est présent
    if 'sales' in categories_for_frontend:
        sales_perms = categories_for_frontend['sales']
        print(f"\n✅ SALES DISPONIBLE POUR LE FRONTEND:")
        print(f"   • Nombre de permissions: {len(sales_perms)}")
        for perm in sales_perms:
            print(f"      - {perm['code']} - {perm['name']}")
        
        # Simuler le JSON qui sera envoyé au frontend
        print(f"\n📤 EXEMPLE JSON POUR LE FRONTEND:")
        sample_json = {
            'sales': [
                {
                    'code': perm['code'],
                    'name': perm['name'],
                    'description': perm['description']
                } for perm in sales_perms[:3]  # 3 premiers exemples
            ]
        }
        print(json.dumps(sample_json, indent=2, ensure_ascii=False))
        
        return True
    else:
        print(f"\n❌ SALES NON DISPONIBLE")
        return False

def check_user_permissions_for_frontend():
    """Vérifier les permissions utilisateur pour le frontend"""
    print(f"\n👤 PERMISSIONS UTILISATEUR POUR LE FRONTEND")
    print("=" * 40)
    
    try:
        from accounts.models import UserPermission
        
        user = User.objects.get(username="testuser_sales")
        user_permissions = UserPermission.objects.filter(user=user, is_active=True)
        
        print(f"   • Utilisateur: {user.get_full_name()}")
        print(f"   • Permissions actives: {user_permissions.count()}")
        
        # Simuler la structure pour le frontend
        user_perms_json = []
        for user_perm in user_permissions:
            perm = user_perm.permission
            user_perms_json.append({
                'code': perm.code,
                'name': perm.name,
                'category': perm.category
            })
        
        # Grouper par catégorie
        user_categories = {}
        for perm in user_perms_json:
            category = perm['category']
            if category not in user_categories:
                user_categories[category] = []
            user_categories[category].append(perm)
        
        print(f"\n📋 PERMISSIONS PAR CATÉGORIE:")
        for category, perms in user_categories.items():
            print(f"   📁 {category}: {len(perms)} permissions")
            if category == 'sales':
                for perm in perms:
                    print(f"      ✅ {perm['code']} - {perm['name']}")
        
        return 'sales' in user_categories
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 VÉRIFICATION DES PERMISSIONS SALES POUR LE FRONTEND")
    print("Vérification que Sales apparaît dans le formulaire de permissions")
    print()
    
    # 1. Test direct en base
    has_sales_db = test_permissions_direct()
    
    # 2. Simulation frontend
    has_sales_frontend = simulate_frontend_permissions()
    
    # 3. Test permissions utilisateur
    user_has_sales = check_user_permissions_for_frontend()
    
    # 4. Test API (si serveur disponible)
    has_sales_api = test_permissions_api()
    
    # 5. Résumé final
    print(f"\n" + "=" * 40)
    print(f"📋 RÉSUMÉ FINAL:")
    
    print(f"   • Base de données: {'✅ Sales présent' if has_sales_db else '❌ Sales manquant'}")
    print(f"   • Frontend simulation: {'✅ Sales disponible' if has_sales_frontend else '❌ Sales indisponible'}")
    print(f"   • Utilisateur testuser_sales: {'✅ A permissions Sales' if user_has_sales else '❌ Pas de permissions Sales'}")
    print(f"   • API: {'✅ Sales accessible' if has_sales_api else '⚠️  Non testé (serveur offline)'}")
    
    if has_sales_db and has_sales_frontend:
        print(f"\n🎉 SUCCÈS!")
        print(f"✅ Sales devrait apparaître dans le formulaire de permissions")
        print(f"✅ Redémarrez le serveur Django et actualisez le frontend")
    else:
        print(f"\n⚠️  PROBLÈMES DÉTECTÉS")
        print(f"Vérifiez la création des permissions Sales")

if __name__ == '__main__':
    main()
