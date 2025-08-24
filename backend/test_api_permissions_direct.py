#!/usr/bin/env python
"""
Script pour tester directement l'API des permissions
"""

import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def test_permissions_api_direct():
    """Tester l'API des permissions directement"""
    print("🌐 TEST DIRECT DE L'API DES PERMISSIONS")
    print("=" * 50)
    
    try:
        # Test de l'endpoint API
        url = "http://127.0.0.1:8000/api/accounts/permissions/list/"
        
        print(f"📡 Test de l'endpoint: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Vérifier le format de la réponse
            if isinstance(data, dict) and 'results' in data:
                permissions = data['results']
                print(f"   Format: Paginé ({len(permissions)} permissions)")
            elif isinstance(data, list):
                permissions = data
                print(f"   Format: Liste directe ({len(permissions)} permissions)")
            else:
                print(f"   Format: Inconnu - {type(data)}")
                return False
            
            # Grouper par catégorie
            categories = {}
            for perm in permissions:
                category = perm.get('category', 'Autre')
                if category not in categories:
                    categories[category] = []
                categories[category].append(perm)
            
            print(f"\n📁 CATÉGORIES RETOURNÉES PAR L'API:")
            for category, perms in sorted(categories.items()):
                print(f"   • {category}: {len(perms)} permissions")
                if category == 'sales':
                    print(f"     ✅ SALES TROUVÉ!")
                    for perm in perms[:3]:
                        print(f"        - {perm.get('name', 'N/A')}")
            
            return 'sales' in categories
            
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            print(f"   Réponse: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Impossible de se connecter au serveur")
        print("   💡 Vérifiez que le serveur Django est démarré")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def check_database_permissions():
    """Vérifier les permissions en base de données"""
    print(f"\n🗄️  VÉRIFICATION BASE DE DONNÉES")
    print("=" * 50)
    
    # Vérifier toutes les permissions
    all_permissions = Permission.objects.all()
    print(f"📊 Total permissions en base: {all_permissions.count()}")
    
    # Vérifier Sales spécifiquement
    sales_permissions = Permission.objects.filter(category='sales')
    print(f"💰 Permissions Sales en base: {sales_permissions.count()}")
    
    if sales_permissions.exists():
        print(f"\n✅ SALES EN BASE:")
        for perm in sales_permissions:
            print(f"   • {perm.code} - {perm.name}")
        return True
    else:
        print(f"\n❌ SALES ABSENT DE LA BASE")
        return False

def test_frontend_data_flow():
    """Simuler le flux de données frontend"""
    print(f"\n🎨 SIMULATION FLUX FRONTEND")
    print("=" * 50)
    
    # Simuler usePermissions() hook
    permissions = Permission.objects.all()
    
    # Format comme l'API
    permissions_data = []
    for perm in permissions:
        permissions_data.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    print(f"📋 Données simulées: {len(permissions_data)} permissions")
    
    # Simuler le groupement frontend (Users.tsx ligne 438)
    grouped = {}
    for permission in permissions_data:
        category = permission['category'] or 'Autre'
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(permission)
    
    print(f"\n🔄 GROUPEMENT FRONTEND:")
    for category, perms in sorted(grouped.items()):
        print(f"   📁 {category.upper()}: {len(perms)} permissions")
    
    return 'sales' in grouped

def force_recreate_sales():
    """Forcer la recréation de Sales si nécessaire"""
    print(f"\n🔧 RECRÉATION FORCÉE DE SALES")
    print("=" * 50)
    
    # Supprimer toutes les permissions sales
    deleted_count = Permission.objects.filter(category='sales').delete()[0]
    print(f"   🗑️  {deleted_count} permissions sales supprimées")
    
    # Recréer Sales
    sales_permissions = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Consulter les ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Effectuer des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Voir l\'historique',
            'category': 'sales'
        }
    ]
    
    created_count = 0
    for perm_data in sales_permissions:
        Permission.objects.create(**perm_data)
        print(f"   ✅ Créée: {perm_data['code']}")
        created_count += 1
    
    print(f"\n📊 {created_count} permissions Sales recréées")
    return created_count > 0

def main():
    """Fonction principale de diagnostic"""
    print("🚀 DIAGNOSTIC COMPLET - PERMISSIONS SALES")
    print()
    
    # 1. Vérifier la base de données
    has_sales_db = check_database_permissions()
    
    # 2. Tester l'API directement
    has_sales_api = test_permissions_api_direct()
    
    # 3. Simuler le frontend
    has_sales_frontend = test_frontend_data_flow()
    
    # 4. Si Sales manque, le recréer
    if not has_sales_db:
        print(f"\n🔧 SALES MANQUANT - RECRÉATION...")
        recreated = force_recreate_sales()
        if recreated:
            # Re-tester après recréation
            has_sales_db = check_database_permissions()
            has_sales_api = test_permissions_api_direct()
            has_sales_frontend = test_frontend_data_flow()
    
    # 5. Résumé final
    print(f"\n" + "=" * 50)
    print(f"📋 DIAGNOSTIC FINAL:")
    
    print(f"   • Base de données: {'✅ Sales présent' if has_sales_db else '❌ Sales absent'}")
    print(f"   • API Response: {'✅ Sales retourné' if has_sales_api else '❌ Sales manquant'}")
    print(f"   • Frontend Flow: {'✅ Sales groupé' if has_sales_frontend else '❌ Sales non groupé'}")
    
    if has_sales_db and has_sales_api and has_sales_frontend:
        print(f"\n🎉 SALES FONCTIONNEL!")
        print(f"✅ Sales devrait apparaître dans le formulaire")
        print(f"✅ Actualisez le navigateur (Ctrl+Shift+R)")
    elif has_sales_db and not has_sales_api:
        print(f"\n⚠️  PROBLÈME API!")
        print(f"Sales est en base mais l'API ne le retourne pas")
        print(f"Vérifiez l'endpoint /api/accounts/permissions/list/")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        print(f"Sales n'est pas correctement configuré")

if __name__ == '__main__':
    main()
