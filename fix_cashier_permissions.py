#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from accounts.models import User, Permission, UserPermission

def fix_cashier_permissions():
    """Corriger les permissions du caissier"""
    
    try:
        # Trouver l'utilisateur caissier
        cashier = User.objects.get(username='caissier')
        print(f"Utilisateur trouve: {cashier.username} - Role: {cashier.role}")
        
        # Permissions requises pour le caissier
        required_permissions = [
            'sales.view',
            'sales.create', 
            'finances.history',
            'products.view'
        ]
        
        # Créer les permissions si elles n'existent pas
        for perm_code in required_permissions:
            permission, created = Permission.objects.get_or_create(
                code=perm_code,
                defaults={
                    'name': perm_code.replace('.', ' ').title(),
                    'description': f'Permission {perm_code}',
                    'category': perm_code.split('.')[0]
                }
            )
            if created:
                print(f"Permission creee: {perm_code}")
            
            # Assigner la permission au caissier
            user_perm, created = UserPermission.objects.get_or_create(
                user=cashier,
                permission=permission,
                defaults={'is_active': True}
            )
            if created:
                print(f"Permission assignee: {perm_code}")
            else:
                print(f"Permission deja assignee: {perm_code}")
        
        # Vérifier les permissions finales
        permissions = cashier.get_permissions()
        print(f"Permissions finales du caissier: {[p.code for p in permissions]}")
        
        return True
        
    except User.DoesNotExist:
        print("ERREUR: Utilisateur caissier non trouve")
        return False
    except Exception as e:
        print(f"ERREUR: {e}")
        return False

if __name__ == '__main__':
    fix_cashier_permissions()
