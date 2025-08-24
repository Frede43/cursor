#!/usr/bin/env python
"""
Script pour tester la connexion après correction
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def test_login():
    """Tester la connexion avec les identifiants corrigés"""
    print("🔐 TEST DE CONNEXION APRÈS CORRECTION")
    print("=" * 40)
    
    username = "testuser_sales"
    password = "temp123456"
    
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    # 1. Vérifier l'utilisateur en base
    try:
        user = User.objects.get(username=username)
        print(f"\n✅ Utilisateur trouvé:")
        print(f"   • Nom: {user.get_full_name()}")
        print(f"   • Email: {user.email}")
        print(f"   • Username: '{user.username}'")
        print(f"   • Actif: {user.is_active}")
    except User.DoesNotExist:
        print(f"\n❌ Utilisateur non trouvé")
        return False
    
    # 2. Test d'authentification Django
    print(f"\n🔑 Test d'authentification:")
    auth_user = authenticate(username=username, password=password)
    
    if auth_user:
        print(f"   ✅ SUCCÈS - Connexion réussie!")
        print(f"   • User ID: {auth_user.id}")
        print(f"   • Nom: {auth_user.get_full_name()}")
        
        # 3. Vérifier les permissions
        from accounts.models import UserPermission
        permissions = UserPermission.objects.filter(user=auth_user, is_active=True)
        print(f"\n🔑 Permissions ({permissions.count()}):")
        for perm in permissions:
            print(f"   • {perm.permission.name} ({perm.permission.code})")
        
        return True
    else:
        print(f"   ❌ ÉCHEC - Connexion échouée")
        return False

def main():
    """Test principal"""
    success = test_login()
    
    print(f"\n" + "=" * 40)
    if success:
        print("🎉 CONNEXION FONCTIONNELLE!")
        print("Vous pouvez maintenant vous connecter avec:")
        print("   Username: testuser_sales")
        print("   Password: temp123456")
    else:
        print("❌ PROBLÈME PERSISTANT")

if __name__ == '__main__':
    main()
