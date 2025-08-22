#!/usr/bin/env python3
"""
Script pour créer un utilisateur directement via Django ORM
Contourne l'interface web pour créer un utilisateur de test
"""

import os
import sys
import django
from datetime import datetime

# Ajouter le chemin du backend Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

# Imports Django après setup
from accounts.models import User, Permission, UserPermission

def create_test_user():
    """Créer un utilisateur de test directement en base"""
    print("🚀 Création d'utilisateur de test via Django ORM")
    print("=" * 50)
    
    try:
        # Vérifier si l'utilisateur existe déjà
        email = "jean.testeur@barstockwise.com"
        if User.objects.filter(email=email).exists():
            print(f"⚠️ L'utilisateur {email} existe déjà")
            user = User.objects.get(email=email)
            print(f"   ID: {user.id}")
            print(f"   Nom: {user.get_full_name()}")
            print(f"   Actif: {user.is_active}")
            return user
        
        # Créer l'utilisateur
        print("👤 Création du nouvel utilisateur...")
        user = User.objects.create_user(
            email=email,
            password="temp123456",
            first_name="Jean",
            last_name="Testeur",
            phone="123456789",
            role="staff"
        )
        
        print(f"✅ Utilisateur créé avec succès!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Nom: {user.get_full_name()}")
        print(f"   Rôle: {user.role}")
        print(f"   Mot de passe: temp123456")
        
        # Attribuer quelques permissions
        print("\n📋 Attribution des permissions...")
        permissions = Permission.objects.all()[:3]  # Prendre les 3 premières
        
        for perm in permissions:
            UserPermission.objects.create(user=user, permission=perm)
            print(f"   ✅ Permission ajoutée: {perm.name}")
        
        print(f"\n🎯 UTILISATEUR TEST CRÉÉ:")
        print(f"   Email: {email}")
        print(f"   Mot de passe: temp123456")
        print(f"   Permissions: {permissions.count()}")
        
        return user
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        return None

def create_admin_user():
    """Créer un utilisateur admin si nécessaire"""
    print("\n🔐 Vérification utilisateur admin...")
    
    admin_email = "admin@barstockwise.com"
    
    try:
        if User.objects.filter(email=admin_email).exists():
            admin = User.objects.get(email=admin_email)
            print(f"✅ Admin existe: {admin.get_full_name()}")
            return admin
        else:
            print("👑 Création de l'utilisateur admin...")
            admin = User.objects.create_user(
                email=admin_email,
                password="admin123",
                first_name="Admin",
                last_name="BarStockWise",
                phone="000000000",
                role="admin",
                is_admin=True,
                is_staff=True,
                is_superuser=True
            )
            print(f"✅ Admin créé: {admin.get_full_name()}")
            print(f"   Email: {admin_email}")
            print(f"   Mot de passe: admin123")
            return admin
            
    except Exception as e:
        print(f"❌ Erreur création admin: {e}")
        return None

def list_users():
    """Lister tous les utilisateurs"""
    print("\n📋 Liste des utilisateurs:")
    print("-" * 30)
    
    users = User.objects.all()
    for user in users:
        permissions_count = UserPermission.objects.filter(user=user).count()
        status = "✅ Actif" if user.is_active else "❌ Inactif"
        role_emoji = {"admin": "👑", "manager": "👔", "staff": "👤"}.get(user.role, "👤")
        
        print(f"{role_emoji} {user.get_full_name()}")
        print(f"   Email: {user.email}")
        print(f"   Rôle: {user.role}")
        print(f"   Statut: {status}")
        print(f"   Permissions: {permissions_count}")
        print()

def test_login():
    """Tester la connexion avec les utilisateurs créés"""
    print("\n🔑 Test de connexion...")
    
    # Test admin
    admin_email = "admin@barstockwise.com"
    if User.objects.filter(email=admin_email).exists():
        admin = User.objects.get(email=admin_email)
        if admin.check_password("admin123"):
            print("✅ Connexion admin OK")
        else:
            print("❌ Connexion admin échouée")
    
    # Test utilisateur
    user_email = "jean.testeur@barstockwise.com"
    if User.objects.filter(email=user_email).exists():
        user = User.objects.get(email=user_email)
        if user.check_password("temp123456"):
            print("✅ Connexion utilisateur OK")
        else:
            print("❌ Connexion utilisateur échouée")

def main():
    """Point d'entrée principal"""
    print("BarStockWise - Création d'utilisateurs via Django ORM")
    print("=" * 60)
    
    # Créer admin si nécessaire
    admin = create_admin_user()
    
    # Créer utilisateur de test
    user = create_test_user()
    
    # Lister les utilisateurs
    list_users()
    
    # Tester les connexions
    test_login()
    
    print("\n🎉 Création terminée!")
    print("\nVous pouvez maintenant:")
    print("1. Démarrer le serveur Django: python manage.py runserver")
    print("2. Démarrer le frontend: npm run dev")
    print("3. Se connecter avec:")
    print("   - Admin: admin@barstockwise.com / admin123")
    print("   - Utilisateur: jean.testeur@barstockwise.com / temp123456")

if __name__ == "__main__":
    main()
