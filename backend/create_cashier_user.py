#!/usr/bin/env python
"""
Script pour créer l'utilisateur caissier avec les bonnes permissions
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Permission, UserPermission

User = get_user_model()

def create_cashier_user():
    """Créer l'utilisateur caissier avec toutes les permissions nécessaires"""
    
    try:
        # Supprimer l'utilisateur existant s'il existe
        try:
            existing_user = User.objects.get(username='caissier')
            existing_user.delete()
            print("🗑️ Ancien utilisateur caissier supprimé")
        except User.DoesNotExist:
            pass
        
        # Créer le nouvel utilisateur caissier
        caissier = User.objects.create_user(
            username='caissier',
            email='caissier@barstock.com',
            password='caissier123',
            first_name='Jean',
            last_name='Caissier',
            role='cashier',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        
        print(f"✅ Utilisateur créé: {caissier.username}")
        print(f"   Email: {caissier.email}")
        print(f"   Nom: {caissier.first_name} {caissier.last_name}")
        print(f"   Rôle: {caissier.role}")
        print(f"   Actif: {caissier.is_active}")
        
        # Permissions à ajouter
        permissions_to_add = [
            ('dashboard.view', 'dashboard', 'Voir le dashboard'),
            ('sales.view', 'sales', 'Voir les ventes'),
            ('sales.create', 'sales', 'Créer des ventes'),
            ('finances.history', 'finances', 'Voir l\'historique des ventes'),
            ('products.view', 'products', 'Voir les produits'),
            ('tables.view', 'tables', 'Voir les tables'),
            ('orders.view', 'orders', 'Voir les commandes')
        ]
        
        for perm_code, category, description in permissions_to_add:
            # Créer ou récupérer la permission
            permission, created = Permission.objects.get_or_create(
                code=perm_code,
                defaults={
                    'name': perm_code.replace('.', ' ').title(),
                    'description': description,
                    'category': category,
                    'is_active': True
                }
            )
            
            if created:
                print(f"📝 Permission créée: {perm_code}")
            
            # Assigner la permission à l'utilisateur
            user_perm, assigned = UserPermission.objects.get_or_create(
                user=caissier,
                permission=permission,
                defaults={'is_active': True}
            )
            
            if assigned:
                print(f"✅ Permission assignée: {perm_code}")
            else:
                # S'assurer que la permission est active
                if not user_perm.is_active:
                    user_perm.is_active = True
                    user_perm.save()
                    print(f"🔄 Permission réactivée: {perm_code}")
                else:
                    print(f"ℹ️ Permission déjà assignée: {perm_code}")
        
        # Vérifier l'authentification
        from django.contrib.auth import authenticate
        auth_user = authenticate(username='caissier', password='caissier123')
        
        if auth_user:
            print("\n✅ Test d'authentification réussi")
        else:
            print("\n❌ Échec du test d'authentification")
            return False
        
        # Afficher les permissions finales
        print(f"\n--- Permissions finales pour {caissier.username} ---")
        user_permissions = caissier.get_permissions()
        for perm in user_permissions:
            print(f"  ✓ {perm.code} ({perm.category})")
        
        print(f"\n🎉 Utilisateur caissier créé avec succès!")
        print(f"Connexion: caissier / caissier123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

if __name__ == '__main__':
    success = create_cashier_user()
    sys.exit(0 if success else 1)
