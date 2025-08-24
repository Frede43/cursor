#!/usr/bin/env python
"""
Script pour créer ou réinitialiser le compte administrateur
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate

def create_admin_user():
    """Créer ou réinitialiser le compte admin"""
    User = get_user_model()
    
    print("🔧 Création du compte administrateur...")
    
    # Supprimer l'admin existant s'il existe
    try:
        existing_admin = User.objects.get(username='admin')
        existing_admin.delete()
        print("🗑️  Ancien compte admin supprimé")
    except User.DoesNotExist:
        print("ℹ️  Aucun compte admin existant")
    
    # Créer le nouveau compte admin
    try:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@barstock.com',
            password='admin123',
            first_name='Admin',
            last_name='System',
            role='admin',
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        
        print("✅ Compte admin créé avec succès!")
        print(f"   Username: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Rôle: {admin_user.role}")
        print(f"   Actif: {admin_user.is_active}")
        print(f"   Staff: {admin_user.is_staff}")
        print(f"   Superuser: {admin_user.is_superuser}")
        
        # Test d'authentification
        print("\n🔍 Test d'authentification...")
        auth_user = authenticate(username='admin', password='admin123')
        
        if auth_user:
            print("✅ Test d'authentification réussi!")
            print("🎉 Connexion possible avec: admin / admin123")
        else:
            print("❌ Échec du test d'authentification")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return False

def list_all_users():
    """Lister tous les utilisateurs"""
    User = get_user_model()
    
    print("\n📋 Liste des utilisateurs:")
    users = User.objects.all()
    
    if users.exists():
        for user in users:
            print(f"   - {user.username} ({user.role}) - Actif: {user.is_active}")
    else:
        print("   Aucun utilisateur trouvé")

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 CRÉATION DU COMPTE ADMINISTRATEUR")
    print("=" * 50)
    
    success = create_admin_user()
    list_all_users()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ COMPTE ADMIN PRÊT!")
        print("🔑 Identifiants: admin / admin123")
        print("=" * 50)
    else:
        print("\n❌ Échec de la création du compte admin")
        sys.exit(1)
