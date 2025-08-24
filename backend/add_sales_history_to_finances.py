#!/usr/bin/env python
"""
Script pour ajouter sales.history dans la catégorie Finances
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def check_current_finances_permissions():
    """Vérifier les permissions actuelles dans Finances"""
    print("📊 PERMISSIONS ACTUELLES DANS FINANCES")
    print("=" * 45)
    
    finances_perms = Permission.objects.filter(category='finances')
    print(f"💰 Total permissions Finances: {finances_perms.count()}")
    
    if finances_perms.exists():
        for perm in finances_perms:
            status = "✅" if perm.is_active else "❌"
            print(f"   {status} {perm.code} - {perm.name}")
    else:
        print("   ❌ Aucune permission Finances trouvée")
    
    return finances_perms.exists()

def check_sales_history_current_location():
    """Vérifier où se trouve actuellement sales.history"""
    print(f"\n🔍 LOCALISATION ACTUELLE DE sales.history")
    print("=" * 45)
    
    sales_history = Permission.objects.filter(code='sales.history')
    
    if sales_history.exists():
        perm = sales_history.first()
        print(f"📍 Trouvé dans catégorie: '{perm.category}'")
        print(f"   Code: {perm.code}")
        print(f"   Nom: {perm.name}")
        print(f"   Actif: {perm.is_active}")
        return perm
    else:
        print("❌ sales.history non trouvé")
        return None

def move_sales_history_to_finances():
    """Déplacer sales.history vers la catégorie Finances"""
    print(f"\n🔄 DÉPLACEMENT VERS FINANCES")
    print("=" * 45)
    
    # Trouver sales.history
    sales_history = Permission.objects.filter(code='sales.history').first()
    
    if sales_history:
        old_category = sales_history.category
        print(f"📦 Déplacement de '{old_category}' vers 'finances'")
        
        # Changer la catégorie
        sales_history.category = 'finances'
        sales_history.save()
        
        print(f"✅ sales.history déplacé vers Finances")
        return True
    else:
        print("❌ sales.history non trouvé pour déplacement")
        return False

def create_additional_finance_permissions():
    """Créer des permissions financières supplémentaires si nécessaire"""
    print(f"\n➕ CRÉATION PERMISSIONS FINANCES SUPPLÉMENTAIRES")
    print("=" * 45)
    
    # Permissions financières recommandées
    finance_permissions = [
        {
            'code': 'finances.view',
            'name': 'Voir les finances',
            'description': 'Consulter les données financières',
            'category': 'finances'
        },
        {
            'code': 'finances.reports',
            'name': 'Rapports financiers',
            'description': 'Générer des rapports financiers',
            'category': 'finances'
        },
        {
            'code': 'finances.export',
            'name': 'Exporter les données',
            'description': 'Exporter les données financières',
            'category': 'finances'
        }
    ]
    
    created_count = 0
    for perm_data in finance_permissions:
        # Vérifier si existe déjà
        if not Permission.objects.filter(code=perm_data['code']).exists():
            Permission.objects.create(**perm_data, is_active=True)
            print(f"   ✅ Créé: {perm_data['code']}")
            created_count += 1
        else:
            print(f"   ⚠️  Existe déjà: {perm_data['code']}")
    
    print(f"\n📊 {created_count} nouvelles permissions créées")
    return created_count

def verify_finances_category():
    """Vérifier la catégorie Finances après modifications"""
    print(f"\n✅ VÉRIFICATION FINALE FINANCES")
    print("=" * 45)
    
    finances_perms = Permission.objects.filter(category='finances', is_active=True)
    print(f"💰 Permissions Finances actives: {finances_perms.count()}")
    
    if finances_perms.exists():
        print(f"\n📋 LISTE COMPLÈTE:")
        for perm in finances_perms:
            print(f"   ✅ {perm.code} - {perm.name}")
        
        # Vérifier spécifiquement sales.history
        sales_history_in_finances = finances_perms.filter(code='sales.history').exists()
        if sales_history_in_finances:
            print(f"\n🎯 sales.history CONFIRMÉ dans Finances!")
            return True
        else:
            print(f"\n❌ sales.history ABSENT de Finances")
            return False
    else:
        print("❌ Aucune permission Finances active")
        return False

def test_api_finances_category():
    """Tester que Finances apparaît dans l'API"""
    print(f"\n🌐 TEST API CATÉGORIE FINANCES")
    print("=" * 45)
    
    import requests
    
    try:
        # Login
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin"}
        
        login_response = requests.post(login_url, json=login_data, timeout=10)
        if login_response.status_code != 200:
            print(f"❌ Échec login")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token') or token_data.get('access')
        
        # Test API
        permissions_url = "http://127.0.0.1:8000/accounts/permissions/list/"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(permissions_url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"❌ Erreur API: {response.status_code}")
            return False
        
        data = response.json()
        permissions = data.get('results', data) if isinstance(data, dict) else data
        
        # Chercher Finances
        finances_found = False
        sales_history_found = False
        
        for perm in permissions:
            if perm.get('category') == 'finances':
                finances_found = True
                if perm.get('code') == 'sales.history':
                    sales_history_found = True
        
        print(f"📊 Résultats API:")
        print(f"   • Catégorie Finances: {'✅ Trouvée' if finances_found else '❌ Absente'}")
        print(f"   • sales.history dans Finances: {'✅ Trouvé' if sales_history_found else '❌ Absent'}")
        
        return finances_found and sales_history_found
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 AJOUT DE sales.history DANS FINANCES")
    print()
    
    # 1. Vérifier l'état actuel
    has_finances = check_current_finances_permissions()
    current_location = check_sales_history_current_location()
    
    # 2. Déplacer sales.history vers Finances
    if current_location:
        moved = move_sales_history_to_finances()
        if not moved:
            print("❌ Échec du déplacement")
            return
    else:
        # Créer sales.history dans Finances si n'existe pas
        print("📝 Création de sales.history dans Finances...")
        Permission.objects.create(
            code='sales.history',
            name='Historique des ventes',
            description='Consulter l\'historique des ventes et transactions',
            category='finances',
            is_active=True
        )
        print("✅ sales.history créé dans Finances")
    
    # 3. Créer des permissions Finances supplémentaires
    created_count = create_additional_finance_permissions()
    
    # 4. Vérifier le résultat
    success = verify_finances_category()
    
    # 5. Tester l'API
    api_success = test_api_finances_category()
    
    # 6. Résumé
    print(f"\n" + "=" * 45)
    print(f"📋 RÉSUMÉ:")
    print(f"   • sales.history dans Finances: {'✅ OUI' if success else '❌ NON'}")
    print(f"   • API Finances fonctionnelle: {'✅ OUI' if api_success else '❌ NON'}")
    
    if success and api_success:
        print(f"\n🎉 SUCCÈS!")
        print(f"✅ L'historique des ventes est maintenant dans Finances")
        print(f"✅ Actualisez le frontend pour voir les changements")
    else:
        print(f"\n❌ Problème persistant")

if __name__ == '__main__':
    main()
