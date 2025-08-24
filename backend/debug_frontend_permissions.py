#!/usr/bin/env python
"""
Script pour diagnostiquer pourquoi Sales n'apparaît pas dans le frontend
et vérifier l'API des permissions
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission
import json

def check_permissions_api_response():
    """Vérifier la réponse de l'API des permissions"""
    print("🔍 DIAGNOSTIC DE L'API DES PERMISSIONS")
    print("=" * 45)
    
    # Simuler la réponse de l'API
    permissions = Permission.objects.all().order_by('category', 'code')
    
    # Convertir en format API
    permissions_api = []
    for perm in permissions:
        permissions_api.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    print(f"📊 TOTAL PERMISSIONS: {len(permissions_api)}")
    
    # Grouper par catégorie
    categories = {}
    for perm in permissions_api:
        category = perm['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(perm)
    
    print(f"\n📁 CATÉGORIES DISPONIBLES:")
    for category, perms in categories.items():
        print(f"   • {category}: {len(perms)} permissions")
        if category == 'sales':
            print(f"     ✅ SALES TROUVÉ!")
            for perm in perms[:3]:
                print(f"        - {perm['code']} - {perm['name']}")
    
    # Vérifier si Sales existe
    has_sales = 'sales' in categories
    print(f"\n🎯 RÉSULTAT: Sales {'✅ PRÉSENT' if has_sales else '❌ ABSENT'}")
    
    if has_sales:
        print(f"\n📤 EXEMPLE RÉPONSE API POUR SALES:")
        sales_response = {
            'sales': categories['sales']
        }
        print(json.dumps(sales_response, indent=2, ensure_ascii=False))
    
    return has_sales, categories

def simulate_frontend_grouping():
    """Simuler le groupement des permissions côté frontend"""
    print(f"\n🎨 SIMULATION DU GROUPEMENT FRONTEND")
    print("=" * 45)
    
    # Récupérer les permissions comme le ferait l'API
    permissions = Permission.objects.all()
    permissions_data = []
    
    for perm in permissions:
        permissions_data.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category or 'Autre'
        })
    
    print(f"📋 Permissions récupérées: {len(permissions_data)}")
    
    # Simuler le code frontend (Users.tsx ligne 438-443)
    grouped_permissions = {}
    for permission in permissions_data:
        category = permission['category'] or 'Autre'
        if category not in grouped_permissions:
            grouped_permissions[category] = []
        grouped_permissions[category].append(permission)
    
    print(f"\n🔄 GROUPEMENT FRONTEND:")
    for category, perms in grouped_permissions.items():
        print(f"   📁 {category.upper()}: {len(perms)} permissions")
        if category == 'sales':
            print(f"      ✅ SALES SERA AFFICHÉ!")
            for perm in perms:
                print(f"         - {perm['name']} ({perm['code']})")
    
    return 'sales' in grouped_permissions

def check_api_endpoint():
    """Vérifier l'endpoint API des permissions"""
    print(f"\n🌐 VÉRIFICATION DE L'ENDPOINT API")
    print("=" * 45)
    
    # Vérifier le endpoint utilisé dans use-api.ts
    endpoint = "/accounts/permissions/list/"
    print(f"📡 Endpoint utilisé: {endpoint}")
    
    # Simuler la réponse
    permissions = Permission.objects.all()
    
    # Format de réponse paginée
    response_paginated = {
        'count': permissions.count(),
        'next': None,
        'previous': None,
        'results': [
            {
                'id': perm.id,
                'code': perm.code,
                'name': perm.name,
                'description': perm.description,
                'category': perm.category
            } for perm in permissions
        ]
    }
    
    # Format de réponse simple
    response_simple = [
        {
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        } for perm in permissions
    ]
    
    print(f"📊 Réponse paginée: {response_paginated['count']} permissions")
    print(f"📊 Réponse simple: {len(response_simple)} permissions")
    
    # Vérifier Sales dans les deux formats
    sales_in_paginated = any(p['category'] == 'sales' for p in response_paginated['results'])
    sales_in_simple = any(p['category'] == 'sales' for p in response_simple)
    
    print(f"\n🎯 SALES dans réponse paginée: {'✅ OUI' if sales_in_paginated else '❌ NON'}")
    print(f"🎯 SALES dans réponse simple: {'✅ OUI' if sales_in_simple else '❌ NON'}")
    
    return sales_in_paginated or sales_in_simple

def create_test_permissions_response():
    """Créer une réponse de test pour le frontend"""
    print(f"\n🧪 CRÉATION D'UNE RÉPONSE DE TEST")
    print("=" * 45)
    
    # Créer une réponse avec Sales explicitement inclus
    test_permissions = [
        {
            'id': 1,
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Accès à la page des ventes',
            'category': 'sales'
        },
        {
            'id': 2,
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Pouvoir effectuer des ventes',
            'category': 'sales'
        },
        {
            'id': 3,
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Accès à l\'historique des ventes',
            'category': 'sales'
        },
        {
            'id': 4,
            'code': 'users.view',
            'name': 'Voir les utilisateurs',
            'description': 'Accès à la liste des utilisateurs',
            'category': 'users'
        }
    ]
    
    print(f"📤 RÉPONSE DE TEST:")
    print(json.dumps(test_permissions, indent=2, ensure_ascii=False))
    
    # Simuler le groupement frontend
    grouped = {}
    for perm in test_permissions:
        category = perm['category']
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(perm)
    
    print(f"\n🔄 GROUPEMENT RÉSULTANT:")
    for category, perms in grouped.items():
        print(f"   📁 {category.upper()}: {len(perms)} permissions")
    
    return 'sales' in grouped

def main():
    """Fonction principale de diagnostic"""
    print("🚀 DIAGNOSTIC COMPLET - PERMISSIONS SALES FRONTEND")
    print("Pourquoi Sales n'apparaît pas dans le formulaire")
    print()
    
    # 1. Vérifier l'API
    has_sales_api, categories = check_permissions_api_response()
    
    # 2. Simuler le frontend
    has_sales_frontend = simulate_frontend_grouping()
    
    # 3. Vérifier l'endpoint
    has_sales_endpoint = check_api_endpoint()
    
    # 4. Test avec données fictives
    has_sales_test = create_test_permissions_response()
    
    # 5. Résumé et solution
    print(f"\n" + "=" * 45)
    print(f"📋 RÉSUMÉ DU DIAGNOSTIC:")
    
    print(f"   • API Backend: {'✅ Sales présent' if has_sales_api else '❌ Sales absent'}")
    print(f"   • Groupement Frontend: {'✅ Fonctionnel' if has_sales_frontend else '❌ Problème'}")
    print(f"   • Endpoint API: {'✅ Sales accessible' if has_sales_endpoint else '❌ Sales inaccessible'}")
    print(f"   • Test fictif: {'✅ Groupement OK' if has_sales_test else '❌ Groupement KO'}")
    
    if has_sales_api and has_sales_frontend:
        print(f"\n🎉 DIAGNOSTIC POSITIF!")
        print(f"✅ Sales devrait apparaître dans le frontend")
        print(f"\n💡 SOLUTIONS POSSIBLES:")
        print(f"1. Redémarrer le serveur Django")
        print(f"2. Vider le cache du navigateur (Ctrl+Shift+R)")
        print(f"3. Vérifier la console du navigateur pour erreurs")
        print(f"4. Tester l'endpoint API manuellement")
    else:
        print(f"\n⚠️  PROBLÈMES DÉTECTÉS!")
        if not has_sales_api:
            print(f"❌ Sales manquant dans l'API backend")
        if not has_sales_frontend:
            print(f"❌ Problème de groupement frontend")
    
    # Afficher les catégories disponibles
    if categories:
        print(f"\n📁 CATÉGORIES DISPONIBLES:")
        for category, perms in categories.items():
            print(f"   • {category}: {len(perms)} permissions")

if __name__ == '__main__':
    main()
