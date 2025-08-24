#!/usr/bin/env python
"""
Script simplifié pour créer facilement des utilisateurs
"""

import os
import sys
import django
import requests
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_user_easy():
    """Interface simple pour créer un utilisateur"""
    print("👤 CRÉATION FACILE D'UTILISATEUR")
    print("=" * 40)
    
    # Connexion admin
    print("🔐 Connexion admin...")
    try:
        response = requests.post('http://localhost:8000/api/accounts/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        
        if response.status_code != 200:
            print("❌ Impossible de se connecter en tant qu'admin")
            return False
        
        admin_token = response.json()['tokens']['access']
        print("✅ Admin connecté")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    # Saisie des informations utilisateur
    print("\n📝 Informations utilisateur:")
    username = input("Username: ").strip()
    first_name = input("Prénom: ").strip()
    last_name = input("Nom: ").strip()
    email = input("Email: ").strip()
    phone = input("Téléphone: ").strip()
    password = input("Mot de passe: ").strip()
    
    print("\n🎭 Rôles disponibles:")
    print("1. admin - Accès complet")
    print("2. manager - Gestion avancée")
    print("3. cashier - Caissier (ventes, tables, produits lecture)")
    print("4. server - Serveur")
    
    role_choice = input("Choisir le rôle (1-4): ").strip()
    role_map = {
        '1': 'admin',
        '2': 'manager', 
        '3': 'cashier',
        '4': 'server'
    }
    
    role = role_map.get(role_choice, 'cashier')
    
    # Permissions selon le rôle
    permissions_map = {
        'admin': [],  # Admin a toutes les permissions
        'manager': ['sales_manage', 'sales_history_view', 'tables_manage', 'products_view', 'products_manage', 'suppliers_view'],
        'cashier': ['sales_manage', 'sales_history_view', 'tables_manage', 'products_view'],
        'server': ['sales_view', 'tables_manage', 'products_view']
    }
    
    permissions = permissions_map.get(role, [])
    
    # Création de l'utilisateur
    print(f"\n🚀 Création de l'utilisateur {username}...")
    
    try:
        headers = {
            'Authorization': f'Bearer {admin_token}',
            'Content-Type': 'application/json'
        }
        
        user_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'role': role,
            'password': password,
            'permissions': permissions
        }
        
        response = requests.post(
            'http://localhost:8000/api/accounts/users/',
            json=user_data,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            user_info = response.json()
            print("✅ Utilisateur créé avec succès!")
            print(f"   Username: {username}")
            print(f"   Nom: {first_name} {last_name}")
            print(f"   Email: {email}")
            print(f"   Rôle: {role}")
            print(f"   Permissions: {len(permissions)} assignées")
            
            print(f"\n🔑 INFORMATIONS DE CONNEXION:")
            print(f"   URL: http://localhost:5173")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            
            return True
        else:
            print(f"❌ Erreur création: {response.status_code}")
            print(f"   Détails: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🎯 CRÉATEUR D'UTILISATEURS SIMPLIFIÉ")
    print("Assurez-vous que le serveur Django fonctionne sur localhost:8000")
    print()
    
    success = create_user_easy()
    
    if success:
        print("\n🎊 Utilisateur créé avec succès!")
        print("Vous pouvez maintenant vous connecter avec ces identifiants.")
    else:
        print("\n❌ Échec de la création d'utilisateur.")
    
    input("\nAppuyez sur Entrée pour quitter...")
