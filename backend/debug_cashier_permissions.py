#!/usr/bin/env python
"""
Script pour diagnostiquer et corriger les problèmes de permissions du caissier
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission

def check_cashier_permissions():
    """Vérifier les permissions actuelles du caissier"""
    print("🔍 DIAGNOSTIC PERMISSIONS CAISSIER")
    print("=" * 40)
    
    try:
        caissier = User.objects.get(username='caissier')
        print(f"👤 Caissier trouvé: {caissier.username} ({caissier.role})")
        
        # Permissions actuelles
        user_perms = UserPermission.objects.filter(user=caissier)
        print(f"🔑 Permissions actuelles: {user_perms.count()}")
        
        for up in user_perms:
            print(f"   ✅ {up.permission.code} - {up.permission.name}")
        
        return caissier
    except User.DoesNotExist:
        print("❌ Caissier non trouvé")
        return None

def check_sales_history_permission():
    """Vérifier la permission historique des ventes"""
    print(f"\n📊 VÉRIFICATION HISTORIQUE VENTES")
    print("=" * 40)
    
    # Chercher toutes les permissions liées à l'historique
    history_perms = Permission.objects.filter(
        code__icontains='history'
    )
    
    print(f"🔍 Permissions contenant 'history': {history_perms.count()}")
    for perm in history_perms:
        print(f"   📋 {perm.code} - {perm.name} (catégorie: {perm.category})")
    
    # Chercher dans finances
    finances_perms = Permission.objects.filter(category='finances')
    print(f"\n💰 Permissions finances: {finances_perms.count()}")
    for perm in finances_perms:
        print(f"   💰 {perm.code} - {perm.name}")
    
    # Chercher dans sales
    sales_perms = Permission.objects.filter(category='sales')
    print(f"\n🛒 Permissions sales: {sales_perms.count()}")
    for perm in sales_perms:
        print(f"   🛒 {perm.code} - {perm.name}")

def check_dashboard_access():
    """Vérifier l'accès au dashboard"""
    print(f"\n🏠 VÉRIFICATION ACCÈS DASHBOARD")
    print("=" * 40)
    
    try:
        dashboard_perm = Permission.objects.get(code='dashboard.view')
        print(f"📋 Permission dashboard trouvée: {dashboard_perm.name}")
        
        # Vérifier qui a cette permission
        users_with_dashboard = UserPermission.objects.filter(permission=dashboard_perm)
        print(f"👥 Utilisateurs avec accès dashboard: {users_with_dashboard.count()}")
        
        for up in users_with_dashboard:
            print(f"   👤 {up.user.username} ({up.user.role})")
        
        return dashboard_perm
    except Permission.DoesNotExist:
        print("❌ Permission dashboard.view non trouvée")
        return None

def fix_cashier_permissions():
    """Corriger les permissions du caissier"""
    print(f"\n🔧 CORRECTION PERMISSIONS CAISSIER")
    print("=" * 40)
    
    try:
        caissier = User.objects.get(username='caissier')
        
        # Supprimer toutes les permissions actuelles
        UserPermission.objects.filter(user=caissier).delete()
        print("🗑️  Anciennes permissions supprimées")
        
        # Permissions correctes pour le caissier
        correct_permissions = [
            'sales.view',           # Voir les ventes
            'sales.create',         # Créer des ventes
            'products.view',        # Voir les produits
        ]
        
        # Essayer d'ajouter sales.history ou finances.history
        history_codes = ['sales.history', 'finances.history', 'history.sales', 'sales.reports']
        
        assigned = 0
        for code in correct_permissions:
            try:
                perm = Permission.objects.get(code=code)
                UserPermission.objects.create(user=caissier, permission=perm)
                print(f"   ✅ {code} - {perm.name}")
                assigned += 1
            except Permission.DoesNotExist:
                print(f"   ❌ Permission non trouvée: {code}")
        
        # Essayer les permissions d'historique
        history_assigned = False
        for code in history_codes:
            try:
                perm = Permission.objects.get(code=code)
                UserPermission.objects.create(user=caissier, permission=perm)
                print(f"   ✅ {code} - {perm.name} (HISTORIQUE)")
                history_assigned = True
                assigned += 1
                break
            except Permission.DoesNotExist:
                continue
        
        if not history_assigned:
            print(f"   ❌ Aucune permission d'historique trouvée")
            # Créer la permission si elle n'existe pas
            history_perm = Permission.objects.create(
                code='sales.history',
                name='Historique des ventes',
                description='Consulter l\'historique des ventes',
                category='sales',
                is_active=True
            )
            UserPermission.objects.create(user=caissier, permission=history_perm)
            print(f"   ✅ sales.history créée et attribuée")
            assigned += 1
        
        print(f"\n📊 {assigned} permissions attribuées au caissier")
        return assigned > 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def restrict_dashboard_access():
    """S'assurer que seul l'admin a accès au dashboard"""
    print(f"\n🔒 RESTRICTION ACCÈS DASHBOARD")
    print("=" * 40)
    
    try:
        # Récupérer ou créer la permission dashboard
        dashboard_perm, created = Permission.objects.get_or_create(
            code='dashboard.view',
            defaults={
                'name': 'Accès au tableau de bord',
                'description': 'Accéder au tableau de bord principal',
                'category': 'dashboard',
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Permission dashboard.view créée")
        else:
            print(f"✅ Permission dashboard.view trouvée")
        
        # Supprimer l'accès dashboard pour tous sauf admin
        non_admin_users = User.objects.exclude(role='admin')
        removed_count = 0
        
        for user in non_admin_users:
            removed = UserPermission.objects.filter(
                user=user, 
                permission=dashboard_perm
            ).delete()[0]
            if removed > 0:
                print(f"   🚫 Accès dashboard retiré à {user.username}")
                removed_count += removed
        
        # S'assurer que l'admin a accès
        admin_users = User.objects.filter(role='admin')
        for admin in admin_users:
            up, created = UserPermission.objects.get_or_create(
                user=admin,
                permission=dashboard_perm
            )
            if created:
                print(f"   ✅ Accès dashboard accordé à {admin.username}")
            else:
                print(f"   ✅ {admin.username} a déjà accès au dashboard")
        
        print(f"\n📊 {removed_count} accès dashboard retirés aux non-admins")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_api_permissions():
    """Tester les permissions via l'API"""
    print(f"\n🌐 TEST API PERMISSIONS")
    print("=" * 40)
    
    import requests
    
    try:
        # Test connexion caissier
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "caissier", "password": "caissier123"}
        
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            print(f"✅ Connexion caissier réussie")
            
            token_data = response.json()
            token = token_data.get('access_token') or token_data.get('access')
            
            # Test permissions
            perm_url = "http://127.0.0.1:8000/accounts/permissions/"
            headers = {"Authorization": f"Bearer {token}"}
            
            perm_response = requests.get(perm_url, headers=headers, timeout=10)
            if perm_response.status_code == 200:
                perms = perm_response.json()
                print(f"📊 API retourne {len(perms)} permissions pour le caissier:")
                
                # Analyser les permissions
                has_sales = False
                has_history = False
                has_dashboard = False
                
                for perm in perms:
                    code = perm.get('code', '')
                    name = perm.get('name', '')
                    print(f"   🔑 {code} - {name}")
                    
                    if 'sales' in code:
                        has_sales = True
                    if 'history' in code or 'historique' in name.lower():
                        has_history = True
                    if 'dashboard' in code:
                        has_dashboard = True
                
                print(f"\n📋 Analyse:")
                print(f"   Sales: {'✅ OUI' if has_sales else '❌ NON'}")
                print(f"   Historique: {'✅ OUI' if has_history else '❌ NON'}")
                print(f"   Dashboard: {'❌ OUI (problème)' if has_dashboard else '✅ NON (correct)'}")
                
                return has_sales and has_history and not has_dashboard
            else:
                print(f"❌ Erreur API permissions: {perm_response.status_code}")
                return False
        else:
            print(f"❌ Échec connexion caissier: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC ET CORRECTION PERMISSIONS CAISSIER")
    print("Problèmes: historique ventes manquant + accès dashboard")
    print()
    
    # 1. Diagnostic initial
    caissier = check_cashier_permissions()
    if not caissier:
        return
    
    # 2. Vérifier les permissions d'historique disponibles
    check_sales_history_permission()
    
    # 3. Vérifier l'accès dashboard
    check_dashboard_access()
    
    # 4. Corriger les permissions du caissier
    permissions_fixed = fix_cashier_permissions()
    
    # 5. Restreindre l'accès dashboard
    dashboard_fixed = restrict_dashboard_access()
    
    # 6. Tester l'API
    api_ok = test_api_permissions()
    
    # 7. Résumé final
    print(f"\n" + "=" * 40)
    print(f"📋 RÉSUMÉ CORRECTIONS:")
    print(f"   • Permissions caissier: {'✅ CORRIGÉES' if permissions_fixed else '❌ PROBLÈME'}")
    print(f"   • Accès dashboard: {'✅ RESTREINT' if dashboard_fixed else '❌ PROBLÈME'}")
    print(f"   • API fonctionnelle: {'✅ OUI' if api_ok else '❌ NON'}")
    
    if permissions_fixed and dashboard_fixed:
        print(f"\n🎉 CORRECTIONS APPLIQUÉES!")
        print(f"✅ Le caissier devrait maintenant avoir:")
        print(f"   • Accès aux ventes")
        print(f"   • Accès à l'historique des ventes")
        print(f"   • PAS d'accès au dashboard")
        print(f"\n🔄 Actualisez votre navigateur et reconnectez-vous")
    else:
        print(f"\n❌ PROBLÈMES PERSISTANTS - Vérifiez les logs")

if __name__ == '__main__':
    main()
