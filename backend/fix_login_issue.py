#!/usr/bin/env python
"""
Script pour corriger le problème de connexion de testuser_sales
Basé sur le problème de normalisation username frontend/backend
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

def fix_user_login():
    """Corriger le problème de connexion"""
    print("🔧 CORRECTION DU PROBLÈME DE CONNEXION")
    print("=" * 45)
    
    # 1. Chercher l'utilisateur avec différentes casses
    print("1️⃣ Recherche de l'utilisateur...")
    
    user = None
    original_username = None
    
    # Tester différentes variations du nom d'utilisateur
    variations = [
        "testuser_sales",
        "TestUser_sales", 
        "TESTUSER_SALES",
        "Testuser_sales"
    ]
    
    for username_var in variations:
        try:
            user = User.objects.get(username=username_var)
            original_username = username_var
            print(f"   ✅ Trouvé: '{original_username}'")
            break
        except User.DoesNotExist:
            print(f"   ❌ Non trouvé: '{username_var}'")
    
    if not user:
        print("   ❌ Utilisateur non trouvé - Création d'un nouvel utilisateur")
        return create_new_user()
    
    # 2. Normaliser le nom d'utilisateur
    print(f"\n2️⃣ Normalisation du nom d'utilisateur...")
    target_username = "testuser_sales"  # Frontend envoie toujours en minuscules
    
    if original_username != target_username:
        print(f"   🔄 '{original_username}' → '{target_username}'")
        user.username = target_username
        user.save()
        print(f"   ✅ Username normalisé")
    else:
        print(f"   ℹ️  Username déjà correct")
    
    # 3. Réinitialiser le mot de passe
    print(f"\n3️⃣ Réinitialisation du mot de passe...")
    password = "temp123456"
    user.set_password(password)
    user.save()
    print(f"   ✅ Mot de passe réinitialisé")
    
    # 4. Vérifier que l'utilisateur est actif
    print(f"\n4️⃣ Vérification du statut...")
    if not user.is_active:
        user.is_active = True
        user.save()
        print(f"   ✅ Utilisateur activé")
    else:
        print(f"   ✅ Utilisateur déjà actif")
    
    # 5. Test de connexion
    print(f"\n5️⃣ Test de connexion...")
    auth_user = authenticate(username=target_username, password=password)
    
    if auth_user:
        print(f"   ✅ SUCCÈS: Connexion réussie!")
        print(f"   • Nom: {auth_user.get_full_name()}")
        print(f"   • Email: {auth_user.email}")
        return True
    else:
        print(f"   ❌ ÉCHEC: Connexion échouée")
        return False

def create_new_user():
    """Créer un nouvel utilisateur si aucun n'est trouvé"""
    print("\n🆕 CRÉATION D'UN NOUVEL UTILISATEUR")
    
    try:
        user = User.objects.create_user(
            username="testuser_sales",  # Déjà en minuscules
            first_name="Jean",
            last_name="Vendeur",
            email="jean.vendeur@barstock.com",
            phone="+257 79 123 456",
            role="server",
            password="temp123456"
        )
        
        print(f"   ✅ Utilisateur créé: {user.get_full_name()}")
        
        # Assigner les permissions
        from accounts.models import Permission, UserPermission
        
        permission_codes = ['sales.view', 'sales.create', 'sales.history']
        for code in permission_codes:
            try:
                permission = Permission.objects.get(code=code)
                UserPermission.objects.create(
                    user=user,
                    permission=permission,
                    is_active=True
                )
                print(f"   ✅ Permission assignée: {code}")
            except Permission.DoesNotExist:
                print(f"   ⚠️  Permission non trouvée: {code}")
        
        # Test de connexion
        auth_user = authenticate(username="testuser_sales", password="temp123456")
        if auth_user:
            print(f"   ✅ Test de connexion: Succès")
            return True
        else:
            print(f"   ❌ Test de connexion: Échec")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la création: {str(e)}")
        return False

def verify_frontend_backend_consistency():
    """Vérifier la cohérence frontend/backend"""
    print(f"\n🔍 VÉRIFICATION DE LA COHÉRENCE FRONTEND/BACKEND")
    
    # Simuler ce que fait le frontend
    frontend_username = "testuser_sales".lower()  # use-auth.tsx ligne 183
    frontend_password = "temp123456"
    
    print(f"   Frontend envoie: '{frontend_username}' / '{frontend_password}'")
    
    # Vérifier en base
    try:
        user = User.objects.get(username=frontend_username)
        print(f"   ✅ Backend trouve: '{user.username}'")
        
        # Test d'authentification
        auth_user = authenticate(username=frontend_username, password=frontend_password)
        if auth_user:
            print(f"   ✅ Authentification: Succès")
            return True
        else:
            print(f"   ❌ Authentification: Échec")
            return False
            
    except User.DoesNotExist:
        print(f"   ❌ Backend ne trouve pas: '{frontend_username}'")
        return False

def main():
    """Fonction principale"""
    print("🚀 RÉSOLUTION DU PROBLÈME DE CONNEXION")
    print("Utilisateur: testuser_sales")
    print("Mot de passe: temp123456")
    print()
    
    # Correction du problème
    success = fix_user_login()
    
    if success:
        # Vérification finale
        print(f"\n" + "=" * 45)
        consistency_ok = verify_frontend_backend_consistency()
        
        if consistency_ok:
            print(f"\n🎉 PROBLÈME RÉSOLU!")
            print(f"✅ L'utilisateur peut maintenant se connecter")
            print(f"✅ Cohérence frontend/backend assurée")
            print(f"\n📝 Identifiants de connexion:")
            print(f"   Username: testuser_sales")
            print(f"   Password: temp123456")
            print(f"\n🔄 Testez maintenant la connexion dans l'interface")
        else:
            print(f"\n⚠️  Problème de cohérence persistant")
    else:
        print(f"\n❌ Impossible de résoudre le problème")

if __name__ == '__main__':
    main()
