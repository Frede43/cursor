#!/usr/bin/env python
"""
Script pour mettre à jour les permissions du caissier et lui donner accès au dashboard
"""

import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Permission, UserPermission

User = get_user_model()

def update_cashier_permissions():
    """Mettre à jour les permissions du caissier pour inclure l'accès au dashboard"""
    
    try:
        # Récupérer l'utilisateur caissier
        caissier = User.objects.get(username='caissier')
        print(f"✅ Caissier trouvé: {caissier.username}")
        
        # Permissions à ajouter pour le caissier
        permissions_to_add = [
            'dashboard.view',      # Accès au dashboard
            'sales.view',          # Voir les ventes
            'sales.create',        # Créer des ventes
            'finances.history',    # Voir l'historique des ventes
            'products.view',       # Voir les produits (nécessaire pour vendre)
        ]
        
        print(f"\n🔧 Mise à jour des permissions pour {caissier.username}...")
        
        for perm_code in permissions_to_add:
            try:
                # Récupérer ou créer la permission
                permission, created = Permission.objects.get_or_create(
                    code=perm_code,
                    defaults={
                        'name': perm_code.replace('.', ' ').title(),
                        'description': f'Permission {perm_code}',
                        'category': perm_code.split('.')[0],
                        'is_active': True
                    }
                )
                
                if created:
                    print(f"   📝 Permission {perm_code} créée")
                
                # Assigner la permission au caissier
                user_perm, assigned = UserPermission.objects.get_or_create(
                    user=caissier,
                    permission=permission,
                    defaults={'is_active': True}
                )
                
                if assigned:
                    print(f"   ✅ Permission {perm_code} assignée au caissier")
                else:
                    # S'assurer que la permission est active
                    if not user_perm.is_active:
                        user_perm.is_active = True
                        user_perm.save()
                        print(f"   🔄 Permission {perm_code} réactivée")
                    else:
                        print(f"   ℹ️  Permission {perm_code} déjà assignée")
                        
            except Exception as e:
                print(f"   ❌ Erreur avec permission {perm_code}: {e}")
        
        # Vérifier les permissions finales
        print(f"\n📊 Permissions finales du caissier:")
        user_permissions = caissier.get_permissions()
        for perm in user_permissions:
            print(f"   ✓ {perm.code} - {perm.name}")
        
        print(f"\n🎯 Le caissier a maintenant accès au dashboard et aux ventes!")
        
        return True
        
    except User.DoesNotExist:
        print("❌ Utilisateur 'caissier' non trouvé. Créer d'abord le caissier.")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des permissions: {e}")
        return False

def verify_permissions():
    """Vérifier que les permissions sont correctement configurées"""
    try:
        caissier = User.objects.get(username='caissier')
        
        # Permissions requises
        required_permissions = [
            'dashboard.view',
            'sales.view', 
            'sales.create',
            'finances.history',
            'products.view'
        ]
        
        print(f"\n🔍 Vérification des permissions pour {caissier.username}:")
        
        user_permissions = caissier.get_permissions()
        user_perm_codes = [perm.code for perm in user_permissions]
        
        all_good = True
        for perm_code in required_permissions:
            if perm_code in user_perm_codes:
                print(f"   ✅ {perm_code}")
            else:
                print(f"   ❌ {perm_code} MANQUANTE")
                all_good = False
        
        if all_good:
            print(f"\n🎉 Toutes les permissions sont correctement configurées!")
        else:
            print(f"\n⚠️  Certaines permissions sont manquantes.")
            
        return all_good
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Mise à jour des permissions du caissier...")
    
    if update_cashier_permissions():
        print("\n" + "="*50)
        verify_permissions()
    else:
        print("❌ Échec de la mise à jour des permissions")
