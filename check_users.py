#!/usr/bin/env python
import os
import sys
import django

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def check_users():
    print("🔍 Vérification des utilisateurs dans la base de données")
    print("=" * 60)
    
    # Lister tous les utilisateurs
    users = User.objects.all()
    print(f"📊 Nombre total d'utilisateurs: {users.count()}")
    print()
    
    for user in users:
        print(f"👤 Utilisateur: {user.username}")
        print(f"   📧 Email: {user.email}")
        print(f"   🏷️  Rôle: {user.role}")
        print(f"   ✅ Actif: {user.is_active}")
        print(f"   🔑 Mot de passe défini: {'Oui' if user.password else 'Non'}")
        print(f"   📅 Créé le: {user.date_joined}")
        
        # Test d'authentification avec différents mots de passe
        test_passwords = ['admin123', 'temp123456', 'password123']
        
        for pwd in test_passwords:
            auth_user = authenticate(username=user.username, password=pwd)
            if auth_user:
                print(f"   ✅ Mot de passe '{pwd}': CORRECT")
                break
        else:
            print(f"   ❌ Aucun des mots de passe testés ne fonctionne")
        
        print("-" * 40)
    
    print("\n🧪 Test de connexion avec les credentials courants:")
    
    # Test spécifique admin
    admin_user = authenticate(username='admin@barstockwise.com', password='admin123')
    if admin_user:
        print("✅ Admin login: SUCCESS")
    else:
        print("❌ Admin login: FAILED")
    
    # Test spécifique utilisateur test
    test_user = authenticate(username='jean.testeur@barstockwise.com', password='temp123456')
    if test_user:
        print("✅ Test user login: SUCCESS")
    else:
        print("❌ Test user login: FAILED")

if __name__ == "__main__":
    check_users()
