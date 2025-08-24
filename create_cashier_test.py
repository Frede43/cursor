#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from accounts.models import User

def create_cashier_test():
    """Créer un utilisateur caissier de test"""
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username='caissier_test').exists():
        print("EXISTE L'utilisateur caissier_test existe deja")
        user = User.objects.get(username='caissier_test')
        print(f"OK Utilisateur existant: {user.username} - Role: {user.role}")
        return user
    
    try:
        # Créer l'utilisateur caissier
        user = User.objects.create_user(
            username='caissier_test',
            email='caissier.test@barstock.com',
            password='test123',
            first_name='Test',
            last_name='Caissier',
            role='cashier'
        )
        
        print("OK Utilisateur cree avec succes:")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - Role: {user.role}")
        print(f"   - Mot de passe: test123")
        
        # Vérifier les permissions
        permissions = user.get_permissions()
        print(f"   - Permissions: {[p.code for p in permissions]}")
        
        return user
        
    except Exception as e:
        print(f"ERREUR lors de la creation: {e}")
        return None

if __name__ == '__main__':
    create_cashier_test()
