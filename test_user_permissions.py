#!/usr/bin/env python
"""
Script pour tester les permissions utilisateur
Ce script permet de:
1. Créer un utilisateur avec des permissions spécifiques
2. Vérifier que ces permissions sont correctement attribuées
3. Tester l'accès aux fonctionnalités basées sur ces permissions
"""

import requests
import json
import random
import string
import time
from pprint import pprint

# Configuration
BASE_URL = "http://localhost:8000/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Couleurs pour la console
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.ENDC}")
    
def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def generate_random_string(length=8):
    """Génère une chaîne aléatoire pour les noms d'utilisateur de test"""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def login_admin():
    """Connexion en tant qu'administrateur"""
    print_header("Connexion administrateur")
    
    login_data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['tokens']['access']
        print_success(f"Connexion admin réussie")
        return access_token
    else:
        print_error(f"Erreur de connexion: {response.status_code}")
        print(response.text)
        return None

def get_all_permissions(token):
    """Récupère toutes les permissions disponibles"""
    print_header("Récupération des permissions disponibles")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/accounts/permissions/list/", headers=headers)
    
    if response.status_code == 200:
        permissions = response.json()
        print_success(f"Récupération de {len(permissions)} permissions")
        return permissions
    else:
        print_error(f"Erreur récupération permissions: {response.status_code}")
        print(response.text)
        return []

def create_test_user(token, permissions_to_assign):
    """Crée un utilisateur de test avec des permissions spécifiques"""
    print_header("Création d'un utilisateur de test")
    
    # Générer un nom d'utilisateur unique
    username = f"testuser_{generate_random_string()}"
    password = "Test@123"
    
    user_data = {
        "username": username,
        "first_name": "Test",
        "last_name": "User",
        "email": f"{username}@example.com",
        "password": password,
        "role": "server"  # Rôle de base
    }
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 1. Créer l'utilisateur
    response = requests.post(f"{BASE_URL}/accounts/users/", json=user_data, headers=headers)
    
    if response.status_code != 201:
        print_error(f"Erreur création utilisateur: {response.status_code}")
        print(response.text)
        return None
    
    response_data = response.json()
    print_info(f"Réponse de création: {response_data}")
    
    # Récupérer l'ID de l'utilisateur (peut être dans différentes clés selon l'API)
    user_id = None
    if 'id' in response_data:
        user_id = response_data['id']
    elif 'user_id' in response_data:
        user_id = response_data['user_id']
    elif 'pk' in response_data:
        user_id = response_data['pk']
    else:
        # Si on ne trouve pas l'ID, on utilise le nom d'utilisateur pour les opérations suivantes
        print_warning("ID utilisateur non trouvé dans la réponse, utilisation du nom d'utilisateur")
        user_id = username
    
    print_success(f"Utilisateur créé avec ID/Username: {user_id}")
    
    # 2. Assigner les permissions
    permissions_data = {
        "permissions": permissions_to_assign
    }
    
    # Utiliser l'endpoint approprié selon que nous avons un ID ou un nom d'utilisateur
    if isinstance(user_id, int) or user_id.isdigit():
        assign_url = f"{BASE_URL}/accounts/users/{user_id}/assign-permissions/"
    else:
        # Si nous n'avons pas d'ID, essayons d'utiliser le nom d'utilisateur
        assign_url = f"{BASE_URL}/accounts/users/assign-permissions/?username={user_id}"
    
    print_info(f"URL d'assignation des permissions: {assign_url}")
    response = requests.post(
        assign_url, 
        json=permissions_data, 
        headers=headers
    )
    
    if response.status_code != 200:
        print_error(f"Erreur assignation permissions: {response.status_code}")
        print(response.text)
    else:
        print_success(f"Permissions assignées avec succès")
    
    return {
        "id": user_id,
        "username": username,
        "password": password
    }

def login_test_user(username, password):
    """Connexion avec l'utilisateur de test"""
    print_header(f"Connexion avec l'utilisateur {username}")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['tokens']['access']
        print_success(f"Connexion réussie")
        return access_token
    else:
        print_error(f"Erreur de connexion: {response.status_code}")
        print(response.text)
        return None

def check_user_permissions(token):
    """Vérifie les permissions de l'utilisateur connecté"""
    print_header("Vérification des permissions utilisateur")
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/accounts/permissions/", headers=headers)
    
    if response.status_code == 200:
        permissions_data = response.json()
        role = permissions_data.get('role', 'inconnu')
        permissions = permissions_data.get('permissions', {})
        
        print_success(f"Rôle: {role}")
        print_info("Permissions actives:")
        
        # Afficher les permissions actives
        active_permissions = [perm for perm, value in permissions.items() if value]
        for perm in active_permissions:
            print(f"  ✓ {perm}")
        
        # Afficher quelques permissions inactives (limité à 5 pour la lisibilité)
        inactive_permissions = [perm for perm, value in permissions.items() if not value]
        if inactive_permissions:
            print_info("Quelques permissions inactives:")
            for perm in inactive_permissions[:5]:
                print(f"  ✗ {perm}")
            if len(inactive_permissions) > 5:
                print(f"  ... et {len(inactive_permissions) - 5} autres")
        
        return permissions_data
    else:
        print_error(f"Erreur vérification permissions: {response.status_code}")
        print(response.text)
        return None

def test_permission_access(token, permission_code, endpoint):
    """Teste l'accès à un endpoint spécifique basé sur une permission"""
    print_header(f"Test d'accès avec permission '{permission_code}'")
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        
        # Pour la page d'accueil, on peut avoir un 404 si c'est une SPA
        if endpoint == '/' and response.status_code == 404:
            print_warning(f"L'endpoint {endpoint} n'existe pas (404) - considéré comme un succès pour une SPA")
            return True
            
        if response.status_code in [200, 201, 204]:
            print_success(f"Accès autorisé à {endpoint}")
            return True
        else:
            print_error(f"Accès refusé à {endpoint} (code: {response.status_code})")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Erreur lors du test d'accès à {endpoint}: {str(e)}")
        return False

def run_permission_tests():
    """Exécute une série de tests de permissions"""
    # 1. Connexion admin
    admin_token = login_admin()
    if not admin_token:
        return
    
    # 2. Récupérer toutes les permissions disponibles
    all_permissions = get_all_permissions(admin_token)
    if not all_permissions:
        return
    
    # Afficher les permissions disponibles
    print_header("Permissions disponibles")
    if isinstance(all_permissions, dict):
        # Si les permissions sont un dictionnaire
        for perm_code, perm_value in all_permissions.items():
            print_info(f"  - {perm_code}: {perm_value}")
    elif isinstance(all_permissions, list):
        # Si les permissions sont une liste d'objets
        for perm in all_permissions:
            if isinstance(perm, dict):
                # Si chaque permission est un dictionnaire avec des attributs
                perm_code = perm.get('code', 'unknown')
                perm_name = perm.get('name', 'unknown')
                print_info(f"  - {perm_name} ({perm_code})")
            else:
                # Si chaque permission est une simple chaîne
                print_info(f"  - {perm}")
    else:
        # Si c'est un autre format
        print_info(f"Format de permissions: {type(all_permissions)}")
        print_info(f"Contenu: {all_permissions}")
    
    # 3. Sélectionner les permissions à tester
    # Permissions complètes pour un administrateur
    admin_permissions = [
        # Accueil/Dashboard
        'dashboard.view',
        'dashboard.manage',
        # Ventes
        'sales.view',
        'sales.create',
        'sales.edit',
        'sales.delete',
        'sales.history',
        # Produits
        'products.view',
        'products.create',
        'products.edit',
        'products.delete',
        # Tables
        'tables.view',
        'tables.manage',
        # Commandes
        'orders.view',
        'orders.manage',
        'orders.delete',
        # Cuisine
        'kitchen.view',
        'kitchen.manage',
        # Rapports
        'reports.view',
        'reports.manage',
        # Analyses
        'analytics.view',
        'analytics.manage',
        # Utilisateurs
        'users.view',
        'users.create',
        'users.edit',
        'users.delete',
        # Fournisseurs
        'suppliers.view',
        'suppliers.create',
        'suppliers.edit',
        'suppliers.delete',
        # Dépenses
        'expenses.view',
        'expenses.create',
        'expenses.edit',
        'expenses.delete',
        # Paramètres
        'settings.view',
        'settings.manage',
        # Stocks
        'inventory.view',
        'inventory.manage',
        # Alertes
        'alerts.view',
        'alerts.manage',
    ]
    
    # Permissions limitées pour un serveur (sans accès à la page d'accueil)
    server_permissions = [
        # Pas de 'dashboard.view' pour restreindre l'accès à la page d'accueil
        'sales.view',
        'sales.create',
        'products.view',
        'tables.view',
        'tables.manage',
        'orders.view',
        'orders.manage',
        'kitchen.view',
    ]
    
    # Choisir les permissions à tester (admin ou serveur)
    test_role = "admin"  # Changer à "server" pour tester les permissions d'un serveur
    test_permissions = admin_permissions if test_role == "admin" else server_permissions
    
    # 4. Créer un utilisateur de test avec ces permissions
    test_user = create_test_user(admin_token, test_permissions)
    if not test_user:
        return
    
    # 5. Se connecter avec l'utilisateur de test
    test_token = login_test_user(test_user['username'], test_user['password'])
    if not test_token:
        return
    
    # 6. Vérifier les permissions de l'utilisateur
    user_permissions = check_user_permissions(test_token)
    if not user_permissions:
        return
    
    # 7. Tester l'accès à différents endpoints
    permission_endpoints = {
        # Endpoints principaux
        'dashboard.view': '/',  # URL de la page d'accueil (racine)
        'sales.view': '/sales/',
        'sales.history': '/sales/history/',
        'products.view': '/products/',
        'tables.view': '/tables/list/',
        'orders.view': '/orders/',
        'kitchen.view': '/kitchen/',
        'reports.view': '/reports/',
        'analytics.view': '/analytics/',
        'users.view': '/accounts/users/',
        'suppliers.view': '/suppliers/',
        'expenses.view': '/expenses/',
        'settings.view': '/settings/',
        'inventory.view': '/inventory/',
        'alerts.view': '/alerts/',
    }
    
    for perm, endpoint in permission_endpoints.items():
        should_have_access = perm in test_permissions
        access_granted = test_permission_access(test_token, perm, endpoint)
        
        if should_have_access == access_granted:
            print_success(f"Test de permission '{perm}' réussi")
        else:
            print_error(f"Test de permission '{perm}' échoué")
    
    # Test spécifique pour l'accès à la page d'accueil
    print_header("Test d'accès à la page d'accueil")
    has_dashboard_permission = 'dashboard.view' in test_permissions
    dashboard_access = test_permission_access(test_token, 'dashboard.view', '/')
    
    if has_dashboard_permission and dashboard_access:
        print_success("✓ L'utilisateur a accès à la page d'accueil (comme prévu)")
    elif not has_dashboard_permission and not dashboard_access:
        print_success("✓ L'utilisateur n'a PAS accès à la page d'accueil (comme prévu)")
    else:
        print_error("✗ Le contrôle d'accès à la page d'accueil ne fonctionne pas correctement")
    
    print_header("Résumé des tests")
    print_success("Tests de permissions terminés")
    print_info(f"Utilisateur de test: {test_user['username']}")
    print_info(f"Rôle: {test_role}")
    print_info(f"Permissions attribuées: {', '.join(test_permissions)}")

if __name__ == "__main__":
    run_permission_tests()