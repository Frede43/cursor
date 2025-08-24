#!/usr/bin/env python
"""
Script de diagnostic pour résoudre le problème de connexion
Vérifie la normalisation des noms d'utilisateur et les mots de passe
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

def diagnose_user_login():
    """Diagnostiquer le problème de connexion"""
    username = "testuser_sales"
    password = "temp123456"
    
    print("🔍 DIAGNOSTIC DU PROBLÈME DE CONNEXION")
    print("=" * 50)
    
    # 1. Vérifier si l'utilisateur existe
    print("1️⃣ Vérification de l'existence de l'utilisateur:")
    
    try:
        user = User.objects.get(username=username)
        print(f"   ✅ Utilisateur trouvé: {user.username}")
        print(f"   • ID: {user.id}")
        print(f"   • Nom: {user.get_full_name()}")
        print(f"   • Email: {user.email}")
        print(f"   • Actif: {user.is_active}")
        print(f"   • Username stocké: '{user.username}'")
        print(f"   • Longueur username: {len(user.username)}")
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur '{username}' non trouvé")
        
        # Chercher des variations
        print("\n   🔍 Recherche de variations:")
        variations = [
            username.lower(),
            username.upper(),
            username.capitalize(),
            "TestUser_sales",
            "testUser_sales"
        ]
        
        for var in variations:
            try:
                user = User.objects.get(username=var)
                print(f"   ✅ Trouvé avec: '{var}'")
                username = var  # Utiliser cette variation
                break
            except User.DoesNotExist:
                print(f"   ❌ Pas trouvé: '{var}'")
        else:
            print("   ❌ Aucune variation trouvée")
            return
    
    # 2. Vérifier le mot de passe
    print(f"\n2️⃣ Vérification du mot de passe:")
    print(f"   Password fourni: '{password}'")
    print(f"   Hash stocké: {user.password[:50]}...")
    
    # Test direct du hash
    password_valid = check_password(password, user.password)
    print(f"   Test direct du hash: {'✅ Valide' if password_valid else '❌ Invalide'}")
    
    # 3. Test d'authentification Django
    print(f"\n3️⃣ Test d'authentification Django:")
    auth_user = authenticate(username=username, password=password)
    
    if auth_user:
        print(f"   ✅ Authentification réussie")
        print(f"   • User ID: {auth_user.id}")
        print(f"   • Username: {auth_user.username}")
    else:
        print(f"   ❌ Authentification échouée")
        
        # Tests avec différentes variations
        print(f"\n   🔍 Test avec variations:")
        test_variations = [
            (username.lower(), password),
            (username.upper(), password),
            (username, password.lower()),
            (username, password.upper()),
        ]
        
        for test_user, test_pass in test_variations:
            test_auth = authenticate(username=test_user, password=test_pass)
            status = "✅ Succès" if test_auth else "❌ Échec"
            print(f"      {status}: '{test_user}' / '{test_pass}'")
    
    # 4. Vérifier les problèmes connus
    print(f"\n4️⃣ Vérification des problèmes connus:")
    
    # Problème de normalisation frontend/backend
    frontend_username = username.lower()  # Le frontend convertit en minuscules
    backend_username = user.username
    
    print(f"   Frontend envoie: '{frontend_username}'")
    print(f"   Backend stocke: '{backend_username}'")
    
    if frontend_username != backend_username:
        print(f"   ⚠️  PROBLÈME DÉTECTÉ: Incohérence de casse")
        print(f"   💡 Solution: Normaliser le username en base")
        return "username_case_mismatch"
    else:
        print(f"   ✅ Cohérence de casse OK")
    
    # Vérifier si l'utilisateur est actif
    if not user.is_active:
        print(f"   ⚠️  PROBLÈME: Utilisateur inactif")
        return "user_inactive"
    
    # Vérifier le mot de passe
    if not password_valid:
        print(f"   ⚠️  PROBLÈME: Mot de passe invalide")
        return "invalid_password"
    
    return "unknown_issue"

def fix_username_normalization():
    """Corriger la normalisation du nom d'utilisateur"""
    print(f"\n🔧 CORRECTION DE LA NORMALISATION:")
    
    try:
        # Chercher l'utilisateur avec différentes casses
        user = None
        original_username = None
        
        for test_username in ["testuser_sales", "TestUser_sales", "TESTUSER_SALES"]:
            try:
                user = User.objects.get(username=test_username)
                original_username = test_username
                break
            except User.DoesNotExist:
                continue
        
        if not user:
            print("   ❌ Utilisateur non trouvé pour correction")
            return False
        
        print(f"   📝 Utilisateur trouvé: '{original_username}'")
        
        # Normaliser en minuscules
        normalized_username = original_username.lower()
        
        if original_username != normalized_username:
            print(f"   🔄 Normalisation: '{original_username}' → '{normalized_username}'")
            user.username = normalized_username
            user.save()
            print(f"   ✅ Username normalisé et sauvegardé")
        else:
            print(f"   ℹ️  Username déjà normalisé")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la correction: {str(e)}")
        return False

def reset_user_password():
    """Réinitialiser le mot de passe de l'utilisateur"""
    print(f"\n🔑 RÉINITIALISATION DU MOT DE PASSE:")
    
    try:
        user = User.objects.get(username="testuser_sales")
        new_password = "temp123456"
        
        user.set_password(new_password)
        user.save()
        
        print(f"   ✅ Mot de passe réinitialisé")
        print(f"   • Nouveau hash: {user.password[:50]}...")
        
        # Test immédiat
        test_auth = authenticate(username="testuser_sales", password=new_password)
        if test_auth:
            print(f"   ✅ Test d'authentification: Succès")
        else:
            print(f"   ❌ Test d'authentification: Échec")
        
        return True
        
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur non trouvé")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def test_final_login():
    """Test final de connexion"""
    print(f"\n🎯 TEST FINAL DE CONNEXION:")
    
    username = "testuser_sales"
    password = "temp123456"
    
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    # Test d'authentification
    user = authenticate(username=username, password=password)
    
    if user:
        print(f"   ✅ SUCCÈS: Connexion réussie!")
        print(f"   • User: {user.get_full_name()}")
        print(f"   • ID: {user.id}")
        print(f"   • Actif: {user.is_active}")
        return True
    else:
        print(f"   ❌ ÉCHEC: Connexion échouée")
        return False

def main():
    """Fonction principale de diagnostic et correction"""
    print("🚀 RÉSOLUTION DU PROBLÈME DE CONNEXION")
    print("Username: testuser_sales")
    print("Password: temp123456")
    print()
    
    # 1. Diagnostic
    issue = diagnose_user_login()
    
    # 2. Correction selon le problème détecté
    if issue == "username_case_mismatch":
        print(f"\n🔧 CORRECTION EN COURS...")
        if fix_username_normalization():
            print(f"✅ Correction appliquée")
        else:
            print(f"❌ Correction échouée")
    
    elif issue == "invalid_password":
        print(f"\n🔧 RÉINITIALISATION DU MOT DE PASSE...")
        if reset_user_password():
            print(f"✅ Mot de passe réinitialisé")
        else:
            print(f"❌ Réinitialisation échouée")
    
    elif issue == "user_inactive":
        print(f"\n🔧 ACTIVATION DE L'UTILISATEUR...")
        try:
            user = User.objects.get(username__iexact="testuser_sales")
            user.is_active = True
            user.save()
            print(f"✅ Utilisateur activé")
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
    
    # 3. Test final
    print(f"\n" + "=" * 50)
    success = test_final_login()
    
    if success:
        print(f"\n🎉 PROBLÈME RÉSOLU!")
        print(f"Vous pouvez maintenant vous connecter avec:")
        print(f"   Username: testuser_sales")
        print(f"   Password: temp123456")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        print(f"Vérifiez que le serveur Django est démarré")
        print(f"et que l'utilisateur existe en base")

if __name__ == '__main__':
    main()
