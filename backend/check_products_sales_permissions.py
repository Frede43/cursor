#!/usr/bin/env python
"""
Script pour vérifier et corriger l'absence des catégories products et sales
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def check_products_sales_permissions():
    """Vérifier si les permissions products et sales existent"""
    print("🔍 VÉRIFICATION PERMISSIONS PRODUCTS ET SALES")
    print("=" * 50)
    
    # Vérifier products
    products_perms = Permission.objects.filter(category='products')
    print(f"📦 Permissions PRODUCTS: {products_perms.count()}")
    
    if products_perms.exists():
        for perm in products_perms:
            status = "✅" if perm.is_active else "❌"
            print(f"   {status} {perm.code} - {perm.name}")
    else:
        print("   ❌ Aucune permission PRODUCTS trouvée")
    
    # Vérifier sales
    sales_perms = Permission.objects.filter(category='sales')
    print(f"\n💰 Permissions SALES: {sales_perms.count()}")
    
    if sales_perms.exists():
        for perm in sales_perms:
            status = "✅" if perm.is_active else "❌"
            print(f"   {status} {perm.code} - {perm.name}")
    else:
        print("   ❌ Aucune permission SALES trouvée")
    
    return products_perms.exists(), sales_perms.exists()

def recreate_missing_permissions():
    """Recréer les permissions manquantes"""
    print(f"\n🔧 RECRÉATION DES PERMISSIONS MANQUANTES")
    print("=" * 50)
    
    # Permissions PRODUCTS
    products_permissions = [
        ("products.view", "Voir les produits", "Consulter le catalogue produits"),
        ("products.create", "Créer produits", "Ajouter de nouveaux produits"),
        ("products.update", "Modifier produits", "Modifier les produits existants"),
        ("products.delete", "Supprimer produits", "Retirer des produits du catalogue"),
        ("products.pricing", "Gérer prix", "Modifier les prix et tarifications"),
    ]
    
    # Permissions SALES
    sales_permissions = [
        ("sales.view", "Voir les ventes", "Consulter les ventes et transactions"),
        ("sales.create", "Créer des ventes", "Effectuer des ventes"),
        ("sales.update", "Modifier les ventes", "Modifier des ventes existantes"),
        ("sales.delete", "Supprimer les ventes", "Annuler/supprimer des ventes"),
        ("sales.refund", "Rembourser", "Effectuer des remboursements"),
    ]
    
    created_count = 0
    
    # Créer PRODUCTS
    print("📦 Création permissions PRODUCTS:")
    for code, name, description in products_permissions:
        if not Permission.objects.filter(code=code).exists():
            Permission.objects.create(
                code=code,
                name=name,
                description=description,
                category='products',
                is_active=True
            )
            print(f"   ✅ {code} - {name}")
            created_count += 1
        else:
            print(f"   ⚠️  Existe déjà: {code}")
    
    # Créer SALES
    print(f"\n💰 Création permissions SALES:")
    for code, name, description in sales_permissions:
        if not Permission.objects.filter(code=code).exists():
            Permission.objects.create(
                code=code,
                name=name,
                description=description,
                category='sales',
                is_active=True
            )
            print(f"   ✅ {code} - {name}")
            created_count += 1
        else:
            print(f"   ⚠️  Existe déjà: {code}")
    
    print(f"\n📊 {created_count} nouvelles permissions créées")
    return created_count > 0

def test_api_products_sales():
    """Tester que l'API retourne products et sales"""
    print(f"\n🌐 TEST API PRODUCTS ET SALES")
    print("=" * 50)
    
    import requests
    
    try:
        # Login admin
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin"}
        
        login_response = requests.post(login_url, json=login_data, timeout=10)
        if login_response.status_code != 200:
            print(f"❌ Échec login: {login_response.status_code}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token') or token_data.get('access')
        
        # Test API permissions
        permissions_url = "http://127.0.0.1:8000/accounts/permissions/list/"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(permissions_url, headers=headers, timeout=10)
        print(f"📡 Status API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('results', data) if isinstance(data, dict) else data
            
            # Chercher products et sales
            products_found = False
            sales_found = False
            
            for perm in permissions:
                if perm.get('category') == 'products':
                    products_found = True
                elif perm.get('category') == 'sales':
                    sales_found = True
            
            print(f"📊 Résultats API:")
            print(f"   • PRODUCTS dans API: {'✅ TROUVÉ' if products_found else '❌ ABSENT'}")
            print(f"   • SALES dans API: {'✅ TROUVÉ' if sales_found else '❌ ABSENT'}")
            
            if products_found and sales_found:
                print(f"\n🎉 PRODUCTS ET SALES DISPONIBLES DANS L'API!")
                
                # Compter les permissions
                products_count = len([p for p in permissions if p.get('category') == 'products'])
                sales_count = len([p for p in permissions if p.get('category') == 'sales'])
                
                print(f"   📦 PRODUCTS: {products_count} permissions")
                print(f"   💰 SALES: {sales_count} permissions")
                
                return True
            else:
                print(f"\n❌ PRODUCTS ou SALES manquant dans l'API")
                return False
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def show_all_categories():
    """Afficher toutes les catégories disponibles"""
    print(f"\n📁 TOUTES LES CATÉGORIES DISPONIBLES")
    print("=" * 50)
    
    categories = Permission.objects.values('category').distinct().order_by('category')
    
    print(f"📊 Total catégories: {len(categories)}")
    
    for cat in categories:
        category_name = cat['category']
        count = Permission.objects.filter(category=category_name).count()
        active_count = Permission.objects.filter(category=category_name, is_active=True).count()
        
        print(f"   🔹 {category_name}: {count} permissions ({active_count} actives)")

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC PRODUCTS ET SALES")
    print("Vérification de l'absence des catégories dans le frontend")
    print()
    
    # 1. Vérifier l'état actuel
    has_products, has_sales = check_products_sales_permissions()
    
    # 2. Afficher toutes les catégories
    show_all_categories()
    
    # 3. Recréer si manquant
    if not has_products or not has_sales:
        print(f"\n⚠️  PERMISSIONS MANQUANTES DÉTECTÉES")
        recreated = recreate_missing_permissions()
        
        if recreated:
            # Re-vérifier après recréation
            has_products, has_sales = check_products_sales_permissions()
    
    # 4. Tester l'API
    api_ok = test_api_products_sales()
    
    # 5. Résumé final
    print(f"\n" + "=" * 50)
    print(f"📋 DIAGNOSTIC FINAL:")
    print(f"   • PRODUCTS en base: {'✅ OUI' if has_products else '❌ NON'}")
    print(f"   • SALES en base: {'✅ OUI' if has_sales else '❌ NON'}")
    print(f"   • API fonctionnelle: {'✅ OUI' if api_ok else '❌ NON'}")
    
    if has_products and has_sales and api_ok:
        print(f"\n🎉 PRODUCTS ET SALES FONCTIONNELS!")
        print(f"✅ Les deux catégories devraient apparaître dans le frontend")
        print(f"✅ Actualisez le navigateur (Ctrl+Shift+R)")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        if not has_products:
            print(f"   • PRODUCTS manquant en base de données")
        if not has_sales:
            print(f"   • SALES manquant en base de données")
        if not api_ok:
            print(f"   • API ne retourne pas les catégories")

if __name__ == '__main__':
    main()
