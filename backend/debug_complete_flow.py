#!/usr/bin/env python
"""
Script pour diagnostiquer complètement pourquoi Sales n'apparaît pas dans le frontend
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

def test_browser_api_call():
    """Simuler exactement l'appel API du navigateur"""
    print("🌐 SIMULATION APPEL API NAVIGATEUR")
    print("=" * 50)
    
    # 1. Login comme le ferait le frontend
    login_url = "http://127.0.0.1:8000/api/auth/login/"
    login_data = {"username": "admin", "password": "admin"}  # Utiliser admin
    
    try:
        print("🔐 Tentative de connexion admin...")
        login_response = requests.post(login_url, json=login_data, timeout=10)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"   ❌ Échec connexion: {login_response.text[:200]}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token') or token_data.get('access')
        
        if not token:
            print(f"   ❌ Token non trouvé")
            return False
        
        print(f"   ✅ Token obtenu")
        
        # 2. Appel permissions avec token
        permissions_url = "http://127.0.0.1:8000/accounts/permissions/list/"
        headers = {"Authorization": f"Bearer {token}"}
        
        print(f"\n📡 Appel API permissions...")
        response = requests.get(permissions_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Analyser la réponse
            if isinstance(data, dict) and 'results' in data:
                permissions = data['results']
                print(f"   Format: Paginé ({len(permissions)} permissions)")
            elif isinstance(data, list):
                permissions = data
                print(f"   Format: Liste ({len(permissions)} permissions)")
            else:
                print(f"   ❌ Format inconnu: {type(data)}")
                return False
            
            # Chercher Sales
            categories = {}
            for perm in permissions:
                cat = perm.get('category', 'Autre')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(perm)
            
            print(f"\n📁 CATÉGORIES RETOURNÉES:")
            for cat, perms in sorted(categories.items()):
                status = "🎯" if cat == 'sales' else "📁"
                print(f"   {status} {cat}: {len(perms)} permissions")
            
            if 'sales' in categories:
                print(f"\n✅ SALES TROUVÉ DANS L'API!")
                sales_perms = categories['sales']
                for perm in sales_perms:
                    print(f"      • {perm.get('name')} ({perm.get('code')})")
                return True
            else:
                print(f"\n❌ SALES ABSENT DE L'API")
                return False
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def check_frontend_config():
    """Vérifier la configuration frontend"""
    print(f"\n⚙️  VÉRIFICATION CONFIG FRONTEND")
    print("=" * 50)
    
    # Vérifier le fichier de config API
    config_files = [
        "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\src\\lib\\api.ts",
        "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\src\\hooks\\use-api.ts",
        "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\.env",
        "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\.env.local"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ {os.path.basename(config_file)} existe")
            
            # Lire le contenu pour chercher l'URL de l'API
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'localhost' in content or '127.0.0.1' in content or '8000' in content:
                    print(f"      🔗 Contient des références au serveur local")
                    
                    # Extraire les URLs
                    lines = content.split('\n')
                    for line in lines:
                        if ('localhost' in line or '127.0.0.1' in line) and ('8000' in line):
                            print(f"         {line.strip()}")
                            
            except Exception as e:
                print(f"      ⚠️  Erreur lecture: {str(e)}")
        else:
            print(f"   ❌ {os.path.basename(config_file)} absent")

def test_direct_database():
    """Test direct de la base de données"""
    print(f"\n🗄️  TEST DIRECT BASE DE DONNÉES")
    print("=" * 50)
    
    # Vérifier Sales en base
    sales_perms = Permission.objects.filter(category='sales')
    print(f"📊 Permissions Sales en base: {sales_perms.count()}")
    
    if sales_perms.exists():
        for perm in sales_perms:
            status = "✅" if perm.is_active else "❌"
            print(f"   {status} {perm.code} - {perm.name} (Active: {perm.is_active})")
        
        # Vérifier le filtre API
        active_sales = Permission.objects.filter(category='sales', is_active=True)
        print(f"\n📈 Permissions Sales ACTIVES: {active_sales.count()}")
        
        return active_sales.count() > 0
    else:
        print(f"   ❌ Aucune permission Sales en base")
        return False

def force_refresh_everything():
    """Forcer le rafraîchissement complet"""
    print(f"\n🔄 RAFRAÎCHISSEMENT FORCÉ")
    print("=" * 50)
    
    # 1. Recréer les permissions Sales avec is_active=True
    print("1️⃣ Suppression et recréation Sales...")
    Permission.objects.filter(category='sales').delete()
    
    sales_permissions = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Consulter les ventes et transactions',
            'category': 'sales',
            'is_active': True
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Effectuer des ventes et transactions',
            'category': 'sales',
            'is_active': True
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Consulter l\'historique des ventes',
            'category': 'sales',
            'is_active': True
        },
        {
            'code': 'sales.update',
            'name': 'Modifier les ventes',
            'description': 'Modifier les ventes existantes',
            'category': 'sales',
            'is_active': True
        },
        {
            'code': 'sales.delete',
            'name': 'Supprimer les ventes',
            'description': 'Supprimer des ventes',
            'category': 'sales',
            'is_active': True
        }
    ]
    
    created_count = 0
    for perm_data in sales_permissions:
        Permission.objects.create(**perm_data)
        created_count += 1
    
    print(f"   ✅ {created_count} permissions Sales créées")
    
    # 2. Vérifier immédiatement
    active_count = Permission.objects.filter(category='sales', is_active=True).count()
    print(f"   📊 {active_count} permissions Sales actives en base")
    
    return active_count > 0

def main():
    """Diagnostic complet"""
    print("🚀 DIAGNOSTIC COMPLET - FRONTEND FLOW")
    print()
    
    # 1. Test base de données
    print("ÉTAPE 1: Base de données")
    db_ok = test_direct_database()
    
    # 2. Si problème DB, forcer refresh
    if not db_ok:
        print("\n🔧 Correction base de données...")
        db_ok = force_refresh_everything()
    
    # 3. Test API avec authentification
    print("\nÉTAPE 2: API avec authentification")
    api_ok = test_browser_api_call()
    
    # 4. Vérifier config frontend
    print("\nÉTAPE 3: Configuration frontend")
    check_frontend_config()
    
    # 5. Résumé final
    print(f"\n" + "=" * 50)
    print(f"📋 RÉSUMÉ FINAL:")
    print(f"   • Base de données: {'✅ OK' if db_ok else '❌ Problème'}")
    print(f"   • API Backend: {'✅ OK' if api_ok else '❌ Problème'}")
    
    if db_ok and api_ok:
        print(f"\n🎉 BACKEND FONCTIONNEL!")
        print(f"✅ Sales est présent en base ET dans l'API")
        print(f"\n🔍 PROBLÈME PROBABLE:")
        print(f"   • Cache navigateur tenace")
        print(f"   • Frontend non connecté au bon backend")
        print(f"   • Serveur frontend non redémarré")
        print(f"\n💡 SOLUTIONS À ESSAYER:")
        print(f"   1. Redémarrer le serveur frontend (npm run dev)")
        print(f"   2. Ouvrir onglet navigation privée")
        print(f"   3. Vider complètement le cache navigateur")
        print(f"   4. Vérifier l'URL dans la console navigateur")
    else:
        print(f"\n❌ PROBLÈME BACKEND PERSISTANT")
        if not db_ok:
            print(f"   Base de données: permissions Sales non actives")
        if not api_ok:
            print(f"   API: ne retourne pas Sales malgré présence en base")

if __name__ == '__main__':
    main()
