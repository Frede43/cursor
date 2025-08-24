#!/usr/bin/env python
"""
Script pour comparer Sales avec les autres catégories qui s'affichent
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

def analyze_all_categories():
    """Analyser toutes les catégories de permissions"""
    print("🔍 ANALYSE COMPARATIVE DES CATÉGORIES")
    print("=" * 50)
    
    # Récupérer toutes les permissions
    all_permissions = Permission.objects.all()
    print(f"📊 Total permissions en base: {all_permissions.count()}")
    
    # Grouper par catégorie
    categories = {}
    for perm in all_permissions:
        cat = perm.category or 'Autre'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(perm)
    
    print(f"\n📁 TOUTES LES CATÉGORIES EN BASE:")
    for cat, perms in sorted(categories.items()):
        active_count = len([p for p in perms if p.is_active])
        inactive_count = len([p for p in perms if not p.is_active])
        
        status = "✅" if active_count > 0 else "❌"
        print(f"   {status} {cat}: {len(perms)} total ({active_count} actives, {inactive_count} inactives)")
        
        # Détails pour Sales
        if cat == 'sales':
            print(f"      🔍 DÉTAILS SALES:")
            for perm in perms:
                active_status = "✅" if perm.is_active else "❌"
                print(f"         {active_status} {perm.code} - {perm.name}")
    
    return categories

def test_api_response():
    """Tester la réponse API et voir quelles catégories sont retournées"""
    print(f"\n🌐 TEST RÉPONSE API")
    print("=" * 50)
    
    try:
        # Login admin
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin"}
        
        login_response = requests.post(login_url, json=login_data, timeout=10)
        if login_response.status_code != 200:
            print(f"❌ Échec login: {login_response.status_code}")
            return {}
        
        token_data = login_response.json()
        token = token_data.get('access_token') or token_data.get('access')
        
        # Appel API permissions
        permissions_url = "http://127.0.0.1:8000/accounts/permissions/list/"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(permissions_url, headers=headers, timeout=10)
        print(f"📡 Status API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Analyser les permissions retournées
            if isinstance(data, dict) and 'results' in data:
                permissions = data['results']
            elif isinstance(data, list):
                permissions = data
            else:
                print(f"❌ Format inattendu: {type(data)}")
                return {}
            
            print(f"📊 Permissions retournées par l'API: {len(permissions)}")
            
            # Grouper par catégorie
            api_categories = {}
            for perm in permissions:
                cat = perm.get('category', 'Autre')
                if cat not in api_categories:
                    api_categories[cat] = []
                api_categories[cat].append(perm)
            
            print(f"\n📁 CATÉGORIES DANS LA RÉPONSE API:")
            for cat, perms in sorted(api_categories.items()):
                status = "🎯" if cat == 'sales' else "📁"
                print(f"   {status} {cat}: {len(perms)} permissions")
                
                # Détails pour chaque catégorie
                for perm in perms[:2]:  # Montrer 2 premiers
                    print(f"      • {perm.get('name')} ({perm.get('code')})")
                if len(perms) > 2:
                    print(f"      ... et {len(perms) - 2} autres")
            
            return api_categories
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return {}
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return {}

def compare_sales_with_others(db_categories, api_categories):
    """Comparer Sales avec d'autres catégories"""
    print(f"\n🔄 COMPARAISON SALES VS AUTRES")
    print("=" * 50)
    
    # Trouver une catégorie qui fonctionne
    working_categories = [cat for cat in api_categories.keys() if cat != 'sales']
    
    if working_categories:
        working_cat = working_categories[0]
        print(f"📊 Comparaison: SALES vs {working_cat.upper()}")
        
        # Comparer en base
        print(f"\n🗄️  EN BASE DE DONNÉES:")
        if 'sales' in db_categories:
            sales_perms = db_categories['sales']
            sales_active = [p for p in sales_perms if p.is_active]
            print(f"   Sales: {len(sales_perms)} total, {len(sales_active)} actives")
            
            # Montrer les détails Sales
            for perm in sales_active:
                print(f"      ✅ {perm.code} - {perm.name}")
        else:
            print(f"   Sales: ABSENT")
        
        if working_cat in db_categories:
            other_perms = db_categories[working_cat]
            other_active = [p for p in other_perms if p.is_active]
            print(f"   {working_cat}: {len(other_perms)} total, {len(other_active)} actives")
            
            # Montrer quelques détails
            for perm in other_active[:2]:
                print(f"      ✅ {perm.code} - {perm.name}")
        
        # Comparer dans l'API
        print(f"\n🌐 DANS LA RÉPONSE API:")
        sales_in_api = 'sales' in api_categories
        other_in_api = working_cat in api_categories
        
        print(f"   Sales dans API: {'✅ OUI' if sales_in_api else '❌ NON'}")
        print(f"   {working_cat} dans API: {'✅ OUI' if other_in_api else '❌ NON'}")
        
        # Identifier la différence
        if not sales_in_api and other_in_api:
            print(f"\n🔍 DIFFÉRENCE IDENTIFIÉE:")
            print(f"   {working_cat} apparaît dans l'API mais pas Sales")
            print(f"   Même si Sales a des permissions actives en base")
            
            # Vérifier les détails techniques
            if 'sales' in db_categories:
                sales_perms = db_categories['sales']
                print(f"\n🔧 ANALYSE TECHNIQUE SALES:")
                for perm in sales_perms:
                    print(f"      ID: {perm.id}")
                    print(f"      Code: {perm.code}")
                    print(f"      Category: '{perm.category}'")
                    print(f"      Is_active: {perm.is_active}")
                    print(f"      Created: {perm.created_at if hasattr(perm, 'created_at') else 'N/A'}")
                    print()

def fix_sales_category_name():
    """Vérifier et corriger le nom de la catégorie Sales"""
    print(f"\n🔧 VÉRIFICATION NOM CATÉGORIE SALES")
    print("=" * 50)
    
    sales_perms = Permission.objects.filter(category='sales')
    
    if sales_perms.exists():
        print(f"📊 {sales_perms.count()} permissions avec category='sales'")
        
        # Vérifier les caractères invisibles ou espaces
        for perm in sales_perms:
            category_repr = repr(perm.category)
            print(f"   • {perm.code}: category = {category_repr}")
            
            # Nettoyer la catégorie si nécessaire
            clean_category = perm.category.strip().lower()
            if clean_category != 'sales':
                print(f"     ⚠️  Catégorie corrompue détectée!")
                perm.category = 'sales'
                perm.save()
                print(f"     ✅ Corrigée vers 'sales'")
    
    # Vérifier aussi d'autres variantes possibles
    variants = ['Sales', 'SALES', 'sale', 'Sale']
    for variant in variants:
        variant_perms = Permission.objects.filter(category=variant)
        if variant_perms.exists():
            print(f"🔍 Trouvé {variant_perms.count()} permissions avec category='{variant}'")
            print(f"   Correction vers 'sales'...")
            variant_perms.update(category='sales')

def main():
    """Fonction principale"""
    print("🚀 ANALYSE COMPARATIVE - POURQUOI SALES NE S'AFFICHE PAS")
    print()
    
    # 1. Analyser toutes les catégories en base
    db_categories = analyze_all_categories()
    
    # 2. Tester l'API
    api_categories = test_api_response()
    
    # 3. Comparer Sales avec les autres
    if api_categories:
        compare_sales_with_others(db_categories, api_categories)
    
    # 4. Vérifier le nom de catégorie
    fix_sales_category_name()
    
    # 5. Re-tester après correction
    if api_categories and 'sales' not in api_categories:
        print(f"\n🔄 RE-TEST APRÈS CORRECTION...")
        new_api_categories = test_api_response()
        
        if 'sales' in new_api_categories:
            print(f"🎉 SALES MAINTENANT VISIBLE DANS L'API!")
        else:
            print(f"❌ Sales toujours absent malgré les corrections")

if __name__ == '__main__':
    main()
