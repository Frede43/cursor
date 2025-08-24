#!/usr/bin/env python
"""
Script pour tester exactement l'endpoint API utilisé par le frontend
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

def test_exact_frontend_api():
    """Tester exactement l'endpoint utilisé par le frontend"""
    print("🔍 TEST EXACT DE L'API FRONTEND")
    print("=" * 45)
    
    # Endpoint exact du frontend (use-api.ts ligne 1111)
    url = "http://127.0.0.1:8000/accounts/permissions/list/"
    
    print(f"📡 Endpoint testé: {url}")
    
    try:
        # Test sans authentification d'abord
        print(f"\n1️⃣ Test sans authentification:")
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ⚠️  Authentification requise")
            return test_with_auth(url)
        elif response.status_code == 200:
            return analyze_response(response, "Sans auth")
        else:
            print(f"   ❌ Erreur: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Serveur non accessible")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def test_with_auth(url):
    """Tester avec authentification comme le frontend"""
    print(f"\n2️⃣ Test avec authentification:")
    
    try:
        # Obtenir un token comme le frontend
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {
            "username": "testuser_sales",
            "password": "temp123456"
        }
        
        login_response = requests.post(login_url, json=login_data, timeout=10)
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('access_token') or token_data.get('access')
            
            if token:
                print(f"   ✅ Token obtenu")
                
                # Appel avec token
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(url, headers=headers, timeout=10)
                print(f"   API status: {response.status_code}")
                
                if response.status_code == 200:
                    return analyze_response(response, "Avec auth")
                else:
                    print(f"   ❌ Erreur API: {response.text[:200]}")
                    return False
            else:
                print(f"   ❌ Token non trouvé dans la réponse")
                return False
        else:
            print(f"   ❌ Login échoué: {login_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur auth: {str(e)}")
        return False

def analyze_response(response, context):
    """Analyser la réponse de l'API"""
    print(f"\n📊 ANALYSE RÉPONSE ({context}):")
    
    try:
        data = response.json()
        
        # Vérifier le format
        if isinstance(data, dict) and 'results' in data:
            permissions = data['results']
            print(f"   Format: Paginé")
            print(f"   Count: {data.get('count', 'N/A')}")
        elif isinstance(data, list):
            permissions = data
            print(f"   Format: Liste directe")
        else:
            print(f"   Format: Inconnu - {type(data)}")
            return False
        
        print(f"   Permissions: {len(permissions)}")
        
        # Analyser les catégories
        categories = {}
        for perm in permissions:
            category = perm.get('category', 'Autre')
            if category not in categories:
                categories[category] = []
            categories[category].append(perm)
        
        print(f"\n📁 CATÉGORIES DANS LA RÉPONSE:")
        for category, perms in sorted(categories.items()):
            status = "✅" if category == 'sales' else "📁"
            print(f"   {status} {category}: {len(perms)} permissions")
            
            if category == 'sales':
                print(f"      🎯 SALES TROUVÉ!")
                for perm in perms:
                    print(f"         - {perm.get('name', 'N/A')} ({perm.get('code', 'N/A')})")
        
        # Vérifier Sales spécifiquement
        has_sales = 'sales' in categories
        
        if not has_sales:
            print(f"\n❌ SALES MANQUANT DANS L'API!")
            print(f"   L'API ne retourne pas les permissions Sales")
            print(f"   Vérifiez l'endpoint ou les permissions en base")
        
        return has_sales
        
    except json.JSONDecodeError:
        print(f"   ❌ Réponse non-JSON: {response.text[:200]}")
        return False

def check_api_endpoint_exists():
    """Vérifier que l'endpoint existe"""
    print(f"\n🔍 VÉRIFICATION ENDPOINT:")
    
    try:
        # Test de base de l'API
        base_url = "http://127.0.0.1:8000/api/"
        response = requests.get(base_url, timeout=5)
        print(f"   API base: {response.status_code}")
        
        # Test accounts
        accounts_url = "http://127.0.0.1:8000/api/accounts/"
        response = requests.get(accounts_url, timeout=5)
        print(f"   Accounts: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def verify_database_again():
    """Vérifier encore la base de données"""
    print(f"\n🗄️  VÉRIFICATION BASE (ENCORE):")
    
    sales_perms = Permission.objects.filter(category='sales')
    print(f"   Sales en base: {sales_perms.count()}")
    
    if sales_perms.exists():
        for perm in sales_perms:
            print(f"   • {perm.code} - {perm.name} (ID: {perm.id})")
        return True
    else:
        print(f"   ❌ Aucune permission Sales en base!")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - API FRONTEND")
    print("Pourquoi Sales n'apparaît pas dans le frontend")
    print()
    
    # 1. Vérifier la base encore
    has_sales_db = verify_database_again()
    
    # 2. Vérifier que l'endpoint existe
    endpoint_ok = check_api_endpoint_exists()
    
    # 3. Tester l'API exacte du frontend
    has_sales_api = test_exact_frontend_api()
    
    # 4. Résumé
    print(f"\n" + "=" * 45)
    print(f"📋 DIAGNOSTIC FINAL:")
    
    print(f"   • Base de données: {'✅ Sales présent' if has_sales_db else '❌ Sales absent'}")
    print(f"   • Endpoint API: {'✅ Accessible' if endpoint_ok else '❌ Problème'}")
    print(f"   • API Response: {'✅ Sales retourné' if has_sales_api else '❌ Sales manquant'}")
    
    if has_sales_db and not has_sales_api:
        print(f"\n🔍 PROBLÈME IDENTIFIÉ:")
        print(f"Sales est en base mais l'API ne le retourne pas")
        print(f"Possible causes:")
        print(f"• Endpoint incorrect")
        print(f"• Problème de sérialisation")
        print(f"• Cache API")
        print(f"• Permissions d'accès API")
    elif not has_sales_db:
        print(f"\n🔍 PROBLÈME IDENTIFIÉ:")
        print(f"Sales n'est pas en base de données")
        print(f"Relancez le script de création des permissions")
    elif has_sales_api:
        print(f"\n🎉 TOUT FONCTIONNE!")
        print(f"Le problème est côté frontend ou cache navigateur")

if __name__ == '__main__':
    main()
