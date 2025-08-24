#!/usr/bin/env python
"""
Script pour forcer l'ajout des permissions Sales qui manquent
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def force_add_sales_permissions():
    """Forcer l'ajout des permissions Sales"""
    print("🔧 AJOUT FORCÉ DES PERMISSIONS SALES")
    print("=" * 45)
    
    # Supprimer d'abord toutes les permissions sales existantes
    existing_sales = Permission.objects.filter(category='sales')
    if existing_sales.exists():
        existing_sales.delete()
        print(f"   🗑️  {existing_sales.count()} permissions sales supprimées")
    
    # Permissions Sales à créer
    sales_permissions = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Consulter la liste des ventes et accéder au POS',
            'category': 'sales'
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Effectuer des ventes via le système POS',
            'category': 'sales'
        },
        {
            'code': 'sales.update',
            'name': 'Modifier les ventes',
            'description': 'Modifier les ventes existantes',
            'category': 'sales'
        },
        {
            'code': 'sales.delete',
            'name': 'Supprimer les ventes',
            'description': 'Annuler ou supprimer des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Accès à l\'historique complet des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.approve',
            'name': 'Approuver les ventes',
            'description': 'Valider les ventes en attente',
            'category': 'sales'
        },
        {
            'code': 'sales.refund',
            'name': 'Rembourser les ventes',
            'description': 'Effectuer des remboursements',
            'category': 'sales'
        },
        {
            'code': 'sales.discount',
            'name': 'Appliquer des remises',
            'description': 'Accorder des remises sur les ventes',
            'category': 'sales'
        }
    ]
    
    created_count = 0
    for perm_data in sales_permissions:
        try:
            permission = Permission.objects.create(
                code=perm_data['code'],
                name=perm_data['name'],
                description=perm_data['description'],
                category=perm_data['category']
            )
            print(f"   ✅ Créée: {permission.code} - {permission.name}")
            created_count += 1
        except Exception as e:
            print(f"   ❌ Erreur pour {perm_data['code']}: {str(e)}")
    
    print(f"\n📊 RÉSULTAT: {created_count} permissions Sales créées")
    return created_count

def verify_sales_in_database():
    """Vérifier que Sales est bien en base"""
    print(f"\n🔍 VÉRIFICATION EN BASE DE DONNÉES")
    print("=" * 45)
    
    # Vérifier toutes les permissions
    all_permissions = Permission.objects.all().order_by('category', 'code')
    
    # Grouper par catégorie
    categories = {}
    for perm in all_permissions:
        if perm.category not in categories:
            categories[perm.category] = []
        categories[perm.category].append(perm)
    
    print(f"📊 Total permissions: {all_permissions.count()}")
    print(f"📁 Catégories: {len(categories)}")
    
    # Afficher toutes les catégories
    for category, perms in sorted(categories.items()):
        print(f"\n📁 {category.upper()}")
        for perm in perms:
            print(f"   • {perm.name}")
    
    # Vérifier spécifiquement Sales
    if 'sales' in categories:
        print(f"\n✅ SALES CONFIRMÉ!")
        print(f"   Nombre de permissions: {len(categories['sales'])}")
        return True
    else:
        print(f"\n❌ SALES TOUJOURS MANQUANT!")
        return False

def test_api_response():
    """Tester la réponse API simulée"""
    print(f"\n🌐 TEST DE LA RÉPONSE API")
    print("=" * 45)
    
    # Simuler la réponse de l'API comme dans use-api.ts
    permissions = Permission.objects.all()
    
    api_response = []
    for perm in permissions:
        api_response.append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'description': perm.description,
            'category': perm.category
        })
    
    # Grouper comme le fait le frontend
    grouped = {}
    for perm in api_response:
        category = perm['category'] or 'Autre'
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(perm)
    
    print(f"📋 Réponse API simulée:")
    for category, perms in sorted(grouped.items()):
        print(f"   📁 {category}: {len(perms)} permissions")
    
    return 'sales' in grouped

def assign_sales_to_testuser():
    """Assigner les permissions Sales à testuser_sales"""
    print(f"\n👤 ATTRIBUTION À testuser_sales")
    print("=" * 45)
    
    try:
        from accounts.models import User, UserPermission
        
        user = User.objects.get(username="testuser_sales")
        sales_permissions = Permission.objects.filter(category='sales')
        
        assigned_count = 0
        for permission in sales_permissions:
            user_permission, created = UserPermission.objects.get_or_create(
                user=user,
                permission=permission,
                defaults={'is_active': True}
            )
            
            if created or not user_permission.is_active:
                user_permission.is_active = True
                user_permission.save()
                assigned_count += 1
                print(f"   ✅ {permission.code}")
        
        print(f"\n📊 Permissions Sales assignées: {assigned_count}")
        return True
        
    except User.DoesNotExist:
        print("   ❌ Utilisateur testuser_sales non trouvé")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 CORRECTION DÉFINITIVE - AJOUT DE SALES")
    print()
    
    # 1. Forcer l'ajout des permissions Sales
    created_count = force_add_sales_permissions()
    
    # 2. Vérifier en base de données
    has_sales_db = verify_sales_in_database()
    
    # 3. Tester la réponse API
    has_sales_api = test_api_response()
    
    # 4. Assigner à l'utilisateur test
    user_assigned = assign_sales_to_testuser()
    
    # 5. Résumé final
    print(f"\n" + "=" * 45)
    print(f"📋 RÉSUMÉ FINAL:")
    
    print(f"   • Permissions créées: {created_count}")
    print(f"   • Sales en base: {'✅ OUI' if has_sales_db else '❌ NON'}")
    print(f"   • Sales dans API: {'✅ OUI' if has_sales_api else '❌ NON'}")
    print(f"   • Utilisateur configuré: {'✅ OUI' if user_assigned else '❌ NON'}")
    
    if created_count > 0 and has_sales_db and has_sales_api:
        print(f"\n🎉 SALES AJOUTÉ AVEC SUCCÈS!")
        print(f"✅ {created_count} permissions Sales créées")
        print(f"✅ Catégorie Sales confirmée en base")
        print(f"✅ API prête à retourner Sales")
        
        print(f"\n🔄 REDÉMARREZ MAINTENANT:")
        print(f"1. Arrêtez le serveur Django (Ctrl+C)")
        print(f"2. Redémarrez: python manage.py runserver")
        print(f"3. Actualisez le navigateur (Ctrl+Shift+R)")
        print(f"4. Vérifiez le formulaire de permissions")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        print(f"Vérifiez les erreurs ci-dessus")

if __name__ == '__main__':
    main()
