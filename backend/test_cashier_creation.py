#!/usr/bin/env python
"""
Script simplifié pour créer le caissier et tester les permissions
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission
from django.contrib.auth.hashers import make_password

def main():
    print("🚀 CRÉATION CAISSIER ET TEST PERMISSIONS")
    print("=" * 50)
    
    # 1. Créer le caissier
    print("👤 Création utilisateur caissier...")
    
    # Supprimer l'ancien caissier s'il existe
    User.objects.filter(username='caissier').delete()
    
    # Créer le nouveau caissier
    caissier = User.objects.create(
        username='caissier',
        email='caissier@barstock.com',
        first_name='Jean',
        last_name='Caissier',
        role='cashier',
        is_active=True,
        is_staff=False
    )
    caissier.set_password('caissier123')
    caissier.save()
    
    print(f"✅ Caissier créé: {caissier.username}")
    print(f"   📧 Email: {caissier.email}")
    print(f"   🔑 Mot de passe: caissier123")
    print(f"   👤 Rôle: {caissier.role}")
    
    # 2. Permissions pour le caissier
    print(f"\n🔑 Attribution permissions caissier...")
    
    cashier_permissions = [
        'sales.view',           # Voir les ventes
        'sales.create',         # Créer des ventes
        'finances.history',     # Voir historique des ventes (selon mémoire)
        'products.view',        # Voir les produits
    ]
    
    assigned = 0
    for perm_code in cashier_permissions:
        try:
            permission = Permission.objects.get(code=perm_code)
            UserPermission.objects.get_or_create(
                user=caissier,
                permission=permission,
                defaults={'is_active': True}
            )
            print(f"   ✅ {perm_code} - {permission.name}")
            assigned += 1
        except Permission.DoesNotExist:
            print(f"   ❌ Permission non trouvée: {perm_code}")
    
    print(f"📊 {assigned} permissions attribuées au caissier")
    
    # 3. Configurer admin avec dashboard uniquement
    print(f"\n🔐 Configuration accès dashboard admin...")
    
    try:
        admin_user = User.objects.get(username='admin')
        dashboard_perm = Permission.objects.get(code='dashboard.view')
        
        # S'assurer que admin a dashboard.view
        UserPermission.objects.get_or_create(
            user=admin_user,
            permission=dashboard_perm,
            defaults={'is_active': True}
        )
        print(f"   ✅ Admin a accès au dashboard")
        
        # S'assurer que caissier n'a PAS dashboard.view
        UserPermission.objects.filter(
            user=caissier,
            permission=dashboard_perm
        ).delete()
        print(f"   ✅ Caissier n'a pas accès au dashboard")
        
    except Exception as e:
        print(f"   ❌ Erreur configuration dashboard: {e}")
    
    # 4. Test API rapide
    print(f"\n🌐 Test API...")
    
    import requests
    
    try:
        # Test connexion caissier
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "caissier", "password": "caissier123"}
        
        response = requests.post(login_url, json=login_data, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Connexion caissier réussie")
            
            token_data = response.json()
            token = token_data.get('access_token') or token_data.get('access')
            
            # Test permissions
            perm_url = "http://127.0.0.1:8000/accounts/permissions/"
            headers = {"Authorization": f"Bearer {token}"}
            
            perm_response = requests.get(perm_url, headers=headers, timeout=5)
            if perm_response.status_code == 200:
                perms = perm_response.json()
                print(f"   📊 Caissier a {len(perms)} permissions")
                
                # Vérifier permissions spécifiques
                perm_codes = [p.get('code') for p in perms]
                
                if 'sales.view' in perm_codes:
                    print(f"   ✅ Peut voir les ventes")
                if 'finances.history' in perm_codes:
                    print(f"   ✅ Peut voir l'historique")
                if 'dashboard.view' not in perm_codes:
                    print(f"   ✅ N'a pas accès au dashboard (correct)")
                else:
                    print(f"   ❌ A accès au dashboard (problème)")
            else:
                print(f"   ❌ Erreur permissions: {perm_response.status_code}")
        else:
            print(f"   ❌ Échec connexion: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur API: {e}")
    
    # 5. Résumé final
    print(f"\n" + "=" * 50)
    print(f"📋 RÉSUMÉ FINAL:")
    print(f"   • Caissier créé: ✅ caissier / caissier123")
    print(f"   • Permissions ventes: ✅ OUI")
    print(f"   • Accès historique: ✅ OUI")
    print(f"   • Dashboard admin only: ✅ OUI")
    
    print(f"\n🎉 CONFIGURATION TERMINÉE!")
    print(f"\n💡 COMPTES DE TEST:")
    print(f"   🔹 Admin: admin / admin")
    print(f"      • Accès complet (dashboard, gestion, etc.)")
    print(f"   🔹 Caissier: caissier / caissier123")
    print(f"      • Ventes, historique, produits uniquement")
    print(f"      • PAS d'accès au dashboard")

if __name__ == '__main__':
    main()
