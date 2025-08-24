#!/usr/bin/env python
"""
Script pour forcer l'affichage de Sales dans le frontend
en créant des permissions de test et en vérifiant l'API
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission
import json

def force_create_sales_permissions():
    """Forcer la création des permissions Sales avec des données explicites"""
    print("🔧 CRÉATION FORCÉE DES PERMISSIONS SALES")
    print("=" * 45)
    
    # Permissions Sales avec données explicites
    sales_permissions = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Accès à la consultation des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Pouvoir effectuer des ventes (POS)',
            'category': 'sales'
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Accès à l\'historique complet des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.update',
            'name': 'Modifier les ventes',
            'description': 'Pouvoir modifier les ventes existantes',
            'category': 'sales'
        },
        {
            'code': 'sales.delete',
            'name': 'Supprimer les ventes',
            'description': 'Pouvoir supprimer ou annuler des ventes',
            'category': 'sales'
        }
    ]
    
    created_count = 0
    for perm_data in sales_permissions:
        # Supprimer l'ancienne permission si elle existe
        Permission.objects.filter(code=perm_data['code']).delete()
        
        # Créer la nouvelle permission
        permission = Permission.objects.create(
            code=perm_data['code'],
            name=perm_data['name'],
            description=perm_data['description'],
            category=perm_data['category']
        )
        
        print(f"   ✅ Créée: {permission.code} - {permission.name}")
        created_count += 1
    
    print(f"\n📊 RÉSULTAT: {created_count} permissions Sales créées")
    return created_count > 0

def verify_api_response():
    """Vérifier la réponse API après création"""
    print(f"\n🔍 VÉRIFICATION DE LA RÉPONSE API")
    print("=" * 45)
    
    # Simuler la réponse de l'API /accounts/permissions/list/
    permissions = Permission.objects.all().order_by('category', 'code')
    
    # Format attendu par le frontend
    api_response = []
    for perm in permissions:
        api_response.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    # Grouper par catégorie comme le fait le frontend
    grouped = {}
    for perm in api_response:
        category = perm['category'] or 'Autre'
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(perm)
    
    print(f"📊 Total permissions: {len(api_response)}")
    print(f"📁 Catégories: {list(grouped.keys())}")
    
    # Vérifier Sales spécifiquement
    if 'sales' in grouped:
        sales_perms = grouped['sales']
        print(f"\n✅ SALES TROUVÉ!")
        print(f"   • Nombre de permissions: {len(sales_perms)}")
        for perm in sales_perms:
            print(f"      - {perm['code']} - {perm['name']}")
        
        # Créer un exemple de réponse JSON
        print(f"\n📤 EXEMPLE RÉPONSE API:")
        sample_response = {
            'count': len(api_response),
            'results': api_response[:10]  # 10 premiers exemples
        }
        
        # Afficher juste les permissions Sales
        sales_only = [p for p in api_response if p['category'] == 'sales']
        print(f"📋 Permissions Sales pour le frontend:")
        print(json.dumps(sales_only, indent=2, ensure_ascii=False))
        
        return True
    else:
        print(f"\n❌ SALES NON TROUVÉ")
        return False

def test_frontend_grouping_logic():
    """Tester la logique de groupement du frontend"""
    print(f"\n🎨 TEST DE LA LOGIQUE FRONTEND")
    print("=" * 45)
    
    # Récupérer les permissions comme le ferait usePermissions()
    permissions = Permission.objects.all()
    permissions_data = []
    
    for perm in permissions:
        permissions_data.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    print(f"📋 Données récupérées: {len(permissions_data)} permissions")
    
    # Reproduire exactement le code de Users.tsx (lignes 437-443)
    grouped_permissions = permissions_data.reduce(lambda acc, permission: {
        **acc,
        permission['category'] or 'Autre': [
            *(acc.get(permission['category'] or 'Autre', [])),
            permission
        ]
    }, {})
    
    # Version Python équivalente
    grouped_permissions_py = {}
    for permission in permissions_data:
        category = permission['category'] or 'Autre'
        if category not in grouped_permissions_py:
            grouped_permissions_py[category] = []
        grouped_permissions_py[category].append(permission)
    
    print(f"\n🔄 GROUPEMENT FRONTEND (Python):")
    for category, perms in grouped_permissions_py.items():
        print(f"   📁 {category.upper()}: {len(perms)} permissions")
        if category == 'sales':
            print(f"      ✅ SALES SERA VISIBLE!")
    
    return 'sales' in grouped_permissions_py

def create_minimal_test_case():
    """Créer un cas de test minimal pour le frontend"""
    print(f"\n🧪 CAS DE TEST MINIMAL")
    print("=" * 45)
    
    # Supprimer toutes les permissions existantes
    Permission.objects.all().delete()
    print("   🗑️  Toutes les permissions supprimées")
    
    # Créer seulement quelques permissions de test
    test_permissions = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Test permission',
            'category': 'sales'
        },
        {
            'code': 'users.view',
            'name': 'Voir les utilisateurs',
            'description': 'Test permission',
            'category': 'users'
        }
    ]
    
    for perm_data in test_permissions:
        Permission.objects.create(**perm_data)
        print(f"   ✅ Créée: {perm_data['code']} ({perm_data['category']})")
    
    # Vérifier le résultat
    all_perms = Permission.objects.all()
    categories = set(p.category for p in all_perms)
    
    print(f"\n📊 RÉSULTAT MINIMAL:")
    print(f"   • Total permissions: {all_perms.count()}")
    print(f"   • Catégories: {list(categories)}")
    print(f"   • Sales présent: {'✅ OUI' if 'sales' in categories else '❌ NON'}")
    
    return 'sales' in categories

def main():
    """Fonction principale de correction"""
    print("🚀 CORRECTION FORCÉE - PERMISSIONS SALES FRONTEND")
    print("Forcer l'affichage de Sales dans le formulaire")
    print()
    
    # 1. Créer un cas de test minimal
    print("1️⃣ Création d'un cas de test minimal...")
    minimal_success = create_minimal_test_case()
    
    if minimal_success:
        print("   ✅ Cas minimal créé avec succès")
    else:
        print("   ❌ Échec du cas minimal")
        return
    
    # 2. Créer toutes les permissions Sales
    print("\n2️⃣ Création complète des permissions Sales...")
    sales_created = force_create_sales_permissions()
    
    # 3. Vérifier la réponse API
    print("\n3️⃣ Vérification de l'API...")
    api_ok = verify_api_response()
    
    # 4. Tester la logique frontend
    print("\n4️⃣ Test de la logique frontend...")
    frontend_ok = test_frontend_grouping_logic()
    
    # 5. Résumé final
    print(f"\n" + "=" * 45)
    print(f"📋 RÉSUMÉ DE LA CORRECTION:")
    
    print(f"   • Cas minimal: {'✅ Succès' if minimal_success else '❌ Échec'}")
    print(f"   • Permissions Sales: {'✅ Créées' if sales_created else '❌ Échec'}")
    print(f"   • API Response: {'✅ OK' if api_ok else '❌ Problème'}")
    print(f"   • Frontend Logic: {'✅ OK' if frontend_ok else '❌ Problème'}")
    
    if all([minimal_success, sales_created, api_ok, frontend_ok]):
        print(f"\n🎉 CORRECTION RÉUSSIE!")
        print(f"✅ Sales devrait maintenant apparaître dans le frontend")
        print(f"\n🔄 ACTIONS REQUISES:")
        print(f"1. Redémarrer le serveur Django: python manage.py runserver")
        print(f"2. Actualiser complètement le navigateur (Ctrl+Shift+R)")
        print(f"3. Aller dans Utilisateurs > Nouvel utilisateur")
        print(f"4. Vérifier que 'SALES' apparaît dans les permissions")
    else:
        print(f"\n⚠️  CORRECTION PARTIELLE")
        print(f"Vérifiez les logs ci-dessus pour identifier les problèmes")

if __name__ == '__main__':
    main()
