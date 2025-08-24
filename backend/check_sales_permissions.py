#!/usr/bin/env python
"""
Script pour vérifier et ajouter les permissions Sales manquantes
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def check_sales_permissions():
    """Vérifier les permissions Sales existantes"""
    print("🔍 VÉRIFICATION DES PERMISSIONS SALES")
    print("=" * 45)
    
    # Rechercher toutes les permissions liées aux ventes
    sales_permissions = Permission.objects.filter(category='sales').order_by('code')
    
    print(f"📋 Permissions Sales existantes ({sales_permissions.count()}):")
    for perm in sales_permissions:
        print(f"   • {perm.code} - {perm.name}")
        print(f"     └─ {perm.description}")
    
    return sales_permissions

def add_missing_sales_permissions():
    """Ajouter les permissions Sales manquantes"""
    print(f"\n🔧 AJOUT DES PERMISSIONS SALES MANQUANTES:")
    
    # Permissions Sales complètes
    sales_permissions_data = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Accès à la page des ventes et consultation des ventes',
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
        },
        {
            'code': 'sales.approve',
            'name': 'Approuver les ventes',
            'description': 'Pouvoir approuver les ventes en attente',
            'category': 'sales'
        },
        {
            'code': 'sales.refund',
            'name': 'Rembourser les ventes',
            'description': 'Pouvoir effectuer des remboursements',
            'category': 'sales'
        },
        {
            'code': 'sales.reports',
            'name': 'Rapports de ventes',
            'description': 'Accès aux rapports détaillés de ventes',
            'category': 'sales'
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for perm_data in sales_permissions_data:
        permission, created = Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults={
                'name': perm_data['name'],
                'description': perm_data['description'],
                'category': perm_data['category']
            }
        )
        
        if created:
            print(f"   ✅ Créée: {perm_data['code']} - {perm_data['name']}")
            created_count += 1
        else:
            # Mettre à jour si nécessaire
            updated = False
            if permission.name != perm_data['name']:
                permission.name = perm_data['name']
                updated = True
            if permission.description != perm_data['description']:
                permission.description = perm_data['description']
                updated = True
            if permission.category != perm_data['category']:
                permission.category = perm_data['category']
                updated = True
            
            if updated:
                permission.save()
                print(f"   🔄 Mise à jour: {perm_data['code']} - {perm_data['name']}")
                updated_count += 1
            else:
                print(f"   ℹ️  Existe déjà: {perm_data['code']} - {perm_data['name']}")
    
    print(f"\n📊 RÉSULTAT:")
    print(f"   • Permissions créées: {created_count}")
    print(f"   • Permissions mises à jour: {updated_count}")
    print(f"   • Total permissions Sales: {Permission.objects.filter(category='sales').count()}")
    
    return created_count > 0 or updated_count > 0

def verify_permissions_in_categories():
    """Vérifier les permissions par catégorie"""
    print(f"\n📁 PERMISSIONS PAR CATÉGORIE:")
    
    categories = Permission.objects.values_list('category', flat=True).distinct().order_by('category')
    
    for category in categories:
        perms = Permission.objects.filter(category=category)
        print(f"\n📁 {category.upper()} ({perms.count()} permissions)")
        for perm in perms:
            print(f"   • {perm.code} - {perm.name}")

def test_user_sales_permissions():
    """Tester les permissions de l'utilisateur testuser_sales"""
    print(f"\n👤 PERMISSIONS DE L'UTILISATEUR testuser_sales:")
    
    try:
        from accounts.models import User, UserPermission
        
        user = User.objects.get(username="testuser_sales")
        user_permissions = UserPermission.objects.filter(user=user, is_active=True)
        
        print(f"   • Utilisateur: {user.get_full_name()}")
        print(f"   • Permissions actives: {user_permissions.count()}")
        
        # Grouper par catégorie
        sales_perms = user_permissions.filter(permission__category='sales')
        print(f"\n🔑 Permissions Sales ({sales_perms.count()}):")
        for user_perm in sales_perms:
            perm = user_perm.permission
            print(f"   ✅ {perm.code} - {perm.name}")
        
        # Vérifier les permissions manquantes
        all_sales_perms = Permission.objects.filter(category='sales')
        missing_perms = []
        
        for sales_perm in all_sales_perms:
            if not user_permissions.filter(permission=sales_perm).exists():
                missing_perms.append(sales_perm)
        
        if missing_perms:
            print(f"\n⚠️  Permissions Sales manquantes ({len(missing_perms)}):")
            for perm in missing_perms:
                print(f"   ❌ {perm.code} - {perm.name}")
        else:
            print(f"\n✅ Toutes les permissions Sales sont assignées")
        
        return len(missing_perms) == 0
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def assign_all_sales_permissions():
    """Assigner toutes les permissions Sales à testuser_sales"""
    print(f"\n🔧 ATTRIBUTION DES PERMISSIONS SALES:")
    
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
            
            if created:
                print(f"   ✅ Assignée: {permission.code}")
                assigned_count += 1
            elif not user_permission.is_active:
                user_permission.is_active = True
                user_permission.save()
                print(f"   🔄 Activée: {permission.code}")
                assigned_count += 1
            else:
                print(f"   ℹ️  Déjà active: {permission.code}")
        
        print(f"\n📊 RÉSULTAT:")
        print(f"   • Permissions assignées/activées: {assigned_count}")
        print(f"   • Total permissions Sales: {sales_permissions.count()}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 GESTION DES PERMISSIONS SALES")
    print("Ajout et vérification des permissions Sales")
    print()
    
    # 1. Vérifier les permissions existantes
    existing_permissions = check_sales_permissions()
    
    # 2. Ajouter les permissions manquantes
    changes_made = add_missing_sales_permissions()
    
    # 3. Vérifier toutes les catégories
    verify_permissions_in_categories()
    
    # 4. Tester les permissions utilisateur
    user_has_all_perms = test_user_sales_permissions()
    
    # 5. Assigner les permissions manquantes
    if not user_has_all_perms:
        print(f"\n🔧 CORRECTION DES PERMISSIONS UTILISATEUR...")
        if assign_all_sales_permissions():
            print(f"✅ Permissions utilisateur corrigées")
        else:
            print(f"❌ Erreur lors de la correction")
    
    # 6. Résumé final
    print(f"\n" + "=" * 45)
    print(f"📋 RÉSUMÉ FINAL:")
    
    final_sales_count = Permission.objects.filter(category='sales').count()
    print(f"✅ Permissions Sales disponibles: {final_sales_count}")
    
    if changes_made:
        print(f"✅ Permissions ajoutées/mises à jour")
    else:
        print(f"ℹ️  Aucune modification nécessaire")
    
    print(f"\n💡 PROCHAINES ÉTAPES:")
    print(f"1. Redémarrer le serveur Django")
    print(f"2. Actualiser l'interface frontend")
    print(f"3. Vérifier que 'Sales' apparaît dans le formulaire de permissions")
    print(f"4. Tester la création d'utilisateur avec permissions Sales")

if __name__ == '__main__':
    main()
