#!/usr/bin/env python
"""
Script pour créer un caissier avec permissions spécifiques et configurer l'accès dashboard pour admin uniquement
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission
from django.contrib.auth.hashers import make_password

def create_cashier_user():
    """Créer un utilisateur caissier"""
    print("👤 CRÉATION UTILISATEUR CAISSIER")
    print("=" * 40)
    
    # Données du caissier
    cashier_data = {
        'username': 'caissier',
        'email': 'caissier@barstock.com',
        'first_name': 'Jean',
        'last_name': 'Caissier',
        'password': make_password('caissier123'),
        'is_active': True,
        'role': 'cashier',
        'is_staff': False
    }
    
    # Créer ou récupérer le caissier
    cashier, created = User.objects.get_or_create(
        username='caissier',
        defaults=cashier_data
    )
    
    if created:
        print(f"✅ Caissier créé: {cashier.username}")
    else:
        print(f"✅ Caissier existant: {cashier.username}")
        # Mettre à jour les informations si nécessaire
        for key, value in cashier_data.items():
            if key != 'username':
                setattr(cashier, key, value)
        cashier.save()
        print(f"   📝 Informations mises à jour")
    
    print(f"   📧 Email: {cashier.email}")
    print(f"   👤 Nom: {cashier.first_name} {cashier.last_name}")
    print(f"   🔑 Mot de passe: caissier123")
    
    return cashier

def assign_cashier_permissions(cashier):
    """Attribuer les permissions spécifiques au caissier"""
    print(f"\n🔑 ATTRIBUTION PERMISSIONS CAISSIER")
    print("=" * 40)
    
    # Permissions pour le caissier
    cashier_permissions = [
        'sales.view',           # Voir les ventes
        'sales.create',         # Créer des ventes
        'finances.history',     # Voir historique des ventes
        'products.view',        # Voir les produits (nécessaire pour vendre)
        'profile.view',         # Voir son profil
        'profile.update',       # Modifier son profil
        'help.view'             # Accéder à l'aide
    ]
    
    # Supprimer les anciennes permissions du caissier
    UserPermission.objects.filter(user=cashier).delete()
    print(f"   🗑️  Anciennes permissions supprimées")
    
    # Attribuer les nouvelles permissions
    assigned_count = 0
    for perm_code in cashier_permissions:
        try:
            permission = Permission.objects.get(code=perm_code)
            UserPermission.objects.create(user=cashier, permission=permission)
            print(f"   ✅ {perm_code} - {permission.name}")
            assigned_count += 1
        except Permission.DoesNotExist:
            print(f"   ❌ Permission non trouvée: {perm_code}")
    
    print(f"\n📊 {assigned_count} permissions attribuées au caissier")
    return assigned_count > 0

def configure_admin_dashboard_access():
    """Configurer l'accès dashboard uniquement pour les admins"""
    print(f"\n🔐 CONFIGURATION ACCÈS DASHBOARD ADMIN UNIQUEMENT")
    print("=" * 40)
    
    # Récupérer l'utilisateur admin
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Admin trouvé: {admin_user.username}")
    except User.DoesNotExist:
        print(f"❌ Utilisateur admin non trouvé")
        return False
    
    # Vérifier si admin a la permission dashboard.view
    dashboard_perm = Permission.objects.get(code='dashboard.view')
    admin_has_dashboard = UserPermission.objects.filter(
        user=admin_user, 
        permission=dashboard_perm
    ).exists()
    
    if not admin_has_dashboard:
        UserPermission.objects.create(user=admin_user, permission=dashboard_perm)
        print(f"   ✅ Permission dashboard.view attribuée à admin")
    else:
        print(f"   ✅ Admin a déjà accès au dashboard")
    
    # Vérifier que le caissier n'a PAS accès au dashboard
    cashier = User.objects.get(username='caissier')
    cashier_has_dashboard = UserPermission.objects.filter(
        user=cashier, 
        permission=dashboard_perm
    ).exists()
    
    if cashier_has_dashboard:
        UserPermission.objects.filter(user=cashier, permission=dashboard_perm).delete()
        print(f"   🚫 Permission dashboard.view retirée du caissier")
    else:
        print(f"   ✅ Caissier n'a pas accès au dashboard (correct)")
    
    return True

def create_test_scenario():
    """Créer un scénario de test complet"""
    print(f"\n🧪 CRÉATION SCÉNARIO DE TEST")
    print("=" * 40)
    
    # Créer quelques permissions supplémentaires pour tester
    test_permissions = [
        ('users.view', 'Voir les utilisateurs', 'users'),
        ('settings.view', 'Voir paramètres', 'settings'),
        ('reports.view', 'Voir rapports', 'reports')
    ]
    
    for code, name, category in test_permissions:
        if not Permission.objects.filter(code=code).exists():
            Permission.objects.create(
                code=code,
                name=name,
                description=f"Permission de test: {name}",
                category=category,
                is_active=True
            )
            print(f"   ✅ Permission test créée: {code}")
    
    # Attribuer toutes les permissions à l'admin
    admin_user = User.objects.get(username='admin')
    admin_permissions = Permission.objects.all()
    
    # Supprimer les anciennes permissions admin
    UserPermission.objects.filter(user=admin_user).delete()
    
    # Attribuer toutes les permissions à l'admin
    for perm in admin_permissions:
        UserPermission.objects.create(user=admin_user, permission=perm)
    
    print(f"   ✅ {admin_permissions.count()} permissions attribuées à admin")
    
    return True

def test_permissions_api():
    """Tester l'API des permissions pour les deux utilisateurs"""
    print(f"\n🌐 TEST API PERMISSIONS")
    print("=" * 40)
    
    import requests
    
    # Test pour admin
    print("🔹 Test Admin:")
    try:
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin"}
        
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Connexion admin réussie")
            
            token_data = response.json()
            token = token_data.get('access_token') or token_data.get('access')
            
            # Test permissions admin
            perm_url = "http://127.0.0.1:8000/accounts/permissions/"
            headers = {"Authorization": f"Bearer {token}"}
            
            perm_response = requests.get(perm_url, headers=headers, timeout=10)
            if perm_response.status_code == 200:
                admin_perms = perm_response.json()
                print(f"   📊 Admin a {len(admin_perms)} permissions")
            else:
                print(f"   ❌ Erreur permissions admin: {perm_response.status_code}")
        else:
            print(f"   ❌ Échec connexion admin: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur admin: {str(e)}")
    
    # Test pour caissier
    print("\n🔹 Test Caissier:")
    try:
        login_data = {"username": "caissier", "password": "caissier123"}
        
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Connexion caissier réussie")
            
            token_data = response.json()
            token = token_data.get('access_token') or token_data.get('access')
            
            # Test permissions caissier
            headers = {"Authorization": f"Bearer {token}"}
            
            perm_response = requests.get(perm_url, headers=headers, timeout=10)
            if perm_response.status_code == 200:
                cashier_perms = perm_response.json()
                print(f"   📊 Caissier a {len(cashier_perms)} permissions")
                
                # Vérifier permissions spécifiques
                perm_codes = [p.get('code') for p in cashier_perms]
                
                if 'sales.view' in perm_codes:
                    print(f"   ✅ Peut voir les ventes")
                if 'finances.history' in perm_codes:
                    print(f"   ✅ Peut voir l'historique")
                if 'dashboard.view' in perm_codes:
                    print(f"   ❌ PROBLÈME: A accès au dashboard")
                else:
                    print(f"   ✅ N'a pas accès au dashboard (correct)")
            else:
                print(f"   ❌ Erreur permissions caissier: {perm_response.status_code}")
        else:
            print(f"   ❌ Échec connexion caissier: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur caissier: {str(e)}")

def show_users_summary():
    """Afficher un résumé des utilisateurs et leurs permissions"""
    print(f"\n📋 RÉSUMÉ UTILISATEURS ET PERMISSIONS")
    print("=" * 40)
    
    users = User.objects.filter(username__in=['admin', 'caissier'])
    
    for user in users:
        user_perms = UserPermission.objects.filter(user=user)
        print(f"\n👤 {user.username.upper()}:")
        print(f"   📧 {user.email}")
        print(f"   🔑 {user_perms.count()} permissions")
        
        # Grouper par catégorie
        categories = {}
        for up in user_perms:
            cat = up.permission.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(up.permission.name)
        
        for cat, perms in sorted(categories.items()):
            print(f"   🔹 {cat}: {len(perms)} permissions")

def main():
    """Fonction principale"""
    print("🚀 CRÉATION CAISSIER AVEC PERMISSIONS SPÉCIFIQUES")
    print("Configuration accès dashboard admin uniquement")
    print()
    
    # 1. Créer le caissier
    cashier = create_cashier_user()
    
    # 2. Attribuer les permissions au caissier
    permissions_ok = assign_cashier_permissions(cashier)
    
    # 3. Configurer l'accès dashboard pour admin uniquement
    dashboard_config_ok = configure_admin_dashboard_access()
    
    # 4. Créer le scénario de test
    test_scenario_ok = create_test_scenario()
    
    # 5. Tester l'API
    test_permissions_api()
    
    # 6. Afficher le résumé
    show_users_summary()
    
    # 7. Résumé final
    print(f"\n" + "=" * 40)
    print(f"📋 RÉSUMÉ FINAL:")
    print(f"   • Caissier créé: ✅ OUI")
    print(f"   • Permissions attribuées: {'✅ OUI' if permissions_ok else '❌ NON'}")
    print(f"   • Dashboard admin only: {'✅ OUI' if dashboard_config_ok else '❌ NON'}")
    
    if permissions_ok and dashboard_config_ok:
        print(f"\n🎉 CONFIGURATION TERMINÉE!")
        print(f"\n💡 COMPTES DE TEST:")
        print(f"   🔹 Admin: admin / admin")
        print(f"      • Accès complet (dashboard, gestion, etc.)")
        print(f"   🔹 Caissier: caissier / caissier123")
        print(f"      • Ventes, historique, produits uniquement")
        print(f"      • PAS d'accès au dashboard")
        print(f"\n✅ Testez la connexion avec les deux comptes!")
    else:
        print(f"\n❌ PROBLÈMES DÉTECTÉS - Vérifiez les logs")

if __name__ == '__main__':
    main()
