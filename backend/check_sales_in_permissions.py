#!/usr/bin/env python
"""
Script pour vérifier si Sales est présent dans les permissions créées
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def check_sales_permissions():
    """Vérifier les permissions Sales"""
    print("🔍 VÉRIFICATION DES PERMISSIONS SALES")
    print("=" * 40)
    
    # Rechercher toutes les permissions
    all_permissions = Permission.objects.all()
    print(f"📊 Total permissions: {all_permissions.count()}")
    
    # Rechercher spécifiquement Sales
    sales_permissions = Permission.objects.filter(category='sales')
    print(f"💰 Permissions Sales: {sales_permissions.count()}")
    
    if sales_permissions.exists():
        print(f"\n✅ SALES TROUVÉ!")
        for perm in sales_permissions:
            print(f"   • {perm.code} - {perm.name}")
    else:
        print(f"\n❌ SALES MANQUANT!")
    
    # Afficher toutes les catégories
    categories = Permission.objects.values_list('category', flat=True).distinct()
    print(f"\n📁 TOUTES LES CATÉGORIES:")
    for category in sorted(categories):
        count = Permission.objects.filter(category=category).count()
        print(f"   • {category}: {count} permissions")
    
    return sales_permissions.exists()

def add_missing_sales():
    """Ajouter Sales s'il manque"""
    print(f"\n🔧 AJOUT DES PERMISSIONS SALES")
    print("=" * 40)
    
    # Permissions Sales complètes
    sales_data = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Consulter la liste des ventes et le POS',
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
            'description': 'Modifier les ventes existantes (avant finalisation)',
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
            'description': 'Valider les ventes en attente d\'approbation',
            'category': 'sales'
        },
        {
            'code': 'sales.refund',
            'name': 'Effectuer des remboursements',
            'description': 'Traiter les remboursements et retours',
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
    for perm_data in sales_data:
        permission, created = Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults={
                'name': perm_data['name'],
                'description': perm_data['description'],
                'category': perm_data['category']
            }
        )
        
        if created:
            print(f"   ✅ Créée: {perm_data['code']}")
            created_count += 1
        else:
            print(f"   ℹ️  Existe: {perm_data['code']}")
    
    print(f"\n📊 Permissions Sales créées: {created_count}")
    return created_count

def main():
    """Fonction principale"""
    print("🚀 VÉRIFICATION ET CORRECTION SALES")
    print()
    
    # 1. Vérifier si Sales existe
    has_sales = check_sales_permissions()
    
    # 2. Ajouter Sales s'il manque
    if not has_sales:
        print("\n🔧 AJOUT DE SALES...")
        created = add_missing_sales()
        if created > 0:
            print("✅ Sales ajouté avec succès")
        else:
            print("❌ Erreur lors de l'ajout")
    else:
        # Vérifier si toutes les permissions Sales sont présentes
        print("\n🔧 VÉRIFICATION COMPLÉTUDE...")
        created = add_missing_sales()
        if created > 0:
            print(f"✅ {created} permissions Sales ajoutées")
    
    # 3. Vérification finale
    print(f"\n" + "=" * 40)
    final_check = check_sales_permissions()
    
    if final_check:
        print(f"\n🎉 SALES CONFIRMÉ!")
        print(f"✅ Les permissions Sales sont maintenant présentes")
        print(f"✅ Redémarrez le serveur et actualisez le frontend")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")

if __name__ == '__main__':
    main()
