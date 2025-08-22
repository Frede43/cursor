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

def check_usernames():
    print("🔍 Vérification des USERNAMES dans la base de données")
    print("=" * 60)
    
    # Lister tous les utilisateurs avec leurs usernames
    users = User.objects.all()
    print(f"📊 Nombre total d'utilisateurs: {users.count()}")
    print()
    
    for user in users:
        print(f"👤 ID: {user.id}")
        print(f"   📧 Email: {user.email}")
        print(f"   🏷️  Username: {user.username}")
        print(f"   🎭 Rôle: {user.role}")
        print(f"   ✅ Actif: {user.is_active}")
        print("-" * 40)
    
    print("\n🧪 Test de connexion avec USERNAMES:")
    
    # Récupérer les usernames réels
    usernames = [(user.username, 'admin123' if user.role == 'admin' else 'temp123456') 
                for user in users]
    
    for username, password in usernames:
        auth_user = authenticate(username=username, password=password)
        status = '✅ SUCCESS' if auth_user else '❌ FAILED'
        print(f"   {username} / {password}: {status}")

if __name__ == "__main__":
    check_usernames()
