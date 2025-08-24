#!/usr/bin/env python
"""
Script automatisé pour tester la création d'un utilisateur caissier
avec des permissions spécifiques
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Permission, UserPermission

User = get_user_model()

class CashierUserTester:
    def __init__(self):
        self.admin_token = None
        self.cashier_token = None
        self.cashier_user_id = None
        
    def log(self, message, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {message}")
    
    def login_as_admin(self):
        """Se connecter en tant qu'admin"""
        print("🔐 CONNEXION ADMIN...")
        try:
            response = requests.post('http://localhost:8000/api/accounts/login/', {
                'username': 'admin',
                'password': 'admin123'
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data['tokens']['access']
                self.log("Admin connecté avec succès")
                return True
            else:
                self.log(f"Échec connexion admin: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Erreur connexion admin: {e}", False)
            return False
    
    def create_cashier_permissions(self):
        """Créer les permissions spécifiques pour le caissier"""
        print("\n🔧 CRÉATION DES PERMISSIONS...")
        
        # Permissions exactes selon vos spécifications
        cashier_permissions = [
            {
                'code': 'sales_manage',
                'name': 'Gérer les ventes',
                'description': 'Peut créer, modifier et gérer les ventes',
                'category': 'sales'
            },
            {
                'code': 'sales_history_view',
                'name': 'Voir l\'historique des ventes',
                'description': 'Peut consulter l\'historique complet des ventes',
                'category': 'sales'
            },
            {
                'code': 'tables_manage',
                'name': 'Gérer les tables',
                'description': 'Peut gérer l\'état et les réservations des tables',
                'category': 'tables'
            },
            {
                'code': 'products_view',
                'name': 'Voir les produits',
                'description': 'Peut consulter le catalogue de produits (lecture seule)',
                'category': 'products'
            }
            # Note: Pas de permission 'products_add' ou 'products_manage'
        ]
        
        try:
            created_count = 0
            for perm_data in cashier_permissions:
                permission, created = Permission.objects.get_or_create(
                    code=perm_data['code'],
                    defaults=perm_data
                )
                if created:
                    created_count += 1
            
            self.log(f"Permissions créées/vérifiées: {len(cashier_permissions)} ({created_count} nouvelles)")
            return True
        except Exception as e:
            self.log(f"Erreur création permissions: {e}", False)
            return False
    
    def create_cashier_user(self):
        """Créer un utilisateur caissier via l'API"""
        print("\n👤 CRÉATION UTILISATEUR CAISSIER...")
        
        try:
            # Supprimer l'ancien utilisateur de test s'il existe
            User.objects.filter(username='test_caissier').delete()
            
            headers = {
                'Authorization': f'Bearer {self.admin_token}',
                'Content-Type': 'application/json'
            }
            
            # Données du caissier selon vos spécifications
            cashier_data = {
                'username': 'test_caissier',
                'first_name': 'Marie',
                'last_name': 'Dupont',
                'email': 'marie.dupont@barstock.com',
                'phone': '+25712345678',
                'role': 'cashier',
                'password': 'caissier123',
                'permissions': [
                    'sales_manage',
                    'sales_history_view', 
                    'tables_manage',
                    'products_view'
                ]
            }
            
            response = requests.post(
                'http://localhost:8000/api/accounts/users/',
                json=cashier_data,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                user_data = response.json()
                self.cashier_user_id = user_data.get('id')
                self.log(f"Caissier créé: {user_data.get('username')} (ID: {self.cashier_user_id})")
                self.log(f"  - Nom: {user_data.get('first_name')} {user_data.get('last_name')}")
                self.log(f"  - Email: {user_data.get('email')}")
                self.log(f"  - Rôle: {user_data.get('role')}")
                return True
            else:
                self.log(f"Échec création caissier: {response.status_code} - {response.text}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur création caissier: {e}", False)
            return False
    
    def test_cashier_login(self):
        """Tester la connexion du caissier"""
        print("\n🔑 TEST CONNEXION CAISSIER...")
        
        try:
            response = requests.post('http://localhost:8000/api/accounts/login/', {
                'username': 'test_caissier',
                'password': 'caissier123'
            })
            
            if response.status_code == 200:
                data = response.json()
                self.cashier_token = data['tokens']['access']
                user_info = data['user']
                
                self.log("Caissier connecté avec succès")
                self.log(f"  - Username: {user_info['username']}")
                self.log(f"  - Rôle: {user_info['role']}")
                return True
            else:
                self.log(f"Échec connexion caissier: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Erreur connexion caissier: {e}", False)
            return False
    
    def test_cashier_permissions(self):
        """Tester les permissions du caissier"""
        print("\n🛡️ TEST DES PERMISSIONS...")
        
        if not self.cashier_token:
            self.log("Token caissier manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.cashier_token}',
            'Content-Type': 'application/json'
        }
        
        # Tests des accès autorisés
        authorized_tests = [
            {
                'name': 'Ventes',
                'url': 'http://localhost:8000/api/sales/',
                'description': 'Doit pouvoir gérer les ventes'
            },
            {
                'name': 'Tables',
                'url': 'http://localhost:8000/api/sales/tables/',
                'description': 'Doit pouvoir gérer les tables'
            },
            {
                'name': 'Produits (lecture)',
                'url': 'http://localhost:8000/api/products/',
                'description': 'Doit pouvoir voir les produits'
            }
        ]
        
        # Tests des accès interdits
        forbidden_tests = [
            {
                'name': 'Gestion utilisateurs',
                'url': 'http://localhost:8000/api/accounts/users/',
                'description': 'Ne doit PAS pouvoir gérer les utilisateurs'
            },
            {
                'name': 'Gestion fournisseurs',
                'url': 'http://localhost:8000/api/suppliers/',
                'description': 'Ne doit PAS pouvoir gérer les fournisseurs'
            }
        ]
        
        all_passed = True
        
        # Test des accès autorisés
        print("  📋 Accès autorisés:")
        for test in authorized_tests:
            try:
                response = requests.get(test['url'], headers=headers)
                if response.status_code == 200:
                    self.log(f"    {test['name']}: Accès OK")
                else:
                    self.log(f"    {test['name']}: Accès refusé (HTTP {response.status_code})", False)
                    all_passed = False
            except Exception as e:
                self.log(f"    {test['name']}: Erreur - {e}", False)
                all_passed = False
        
        # Test des accès interdits
        print("  🚫 Accès interdits:")
        for test in forbidden_tests:
            try:
                response = requests.get(test['url'], headers=headers)
                if response.status_code == 403:
                    self.log(f"    {test['name']}: Correctement bloqué")
                else:
                    self.log(f"    {test['name']}: PROBLÈME - Accès autorisé (HTTP {response.status_code})", False)
                    all_passed = False
            except Exception as e:
                self.log(f"    {test['name']}: Erreur - {e}", False)
                all_passed = False
        
        return all_passed
    
    def run_complete_test(self):
        """Exécuter le test complet"""
        print("🧪 TEST COMPLET - CRÉATION UTILISATEUR CAISSIER")
        print("=" * 60)
        print("Objectif: Créer un caissier avec permissions spécifiques:")
        print("  ✅ Gérer les ventes")
        print("  ✅ Voir l'historique des ventes") 
        print("  ✅ Gérer les tables")
        print("  ✅ Voir les produits (lecture seule)")
        print("  ❌ PAS d'ajout de produits")
        print("=" * 60)
        
        # Exécuter tous les tests
        steps = [
            ("Connexion admin", self.login_as_admin),
            ("Création permissions", self.create_cashier_permissions),
            ("Création caissier", self.create_cashier_user),
            ("Test connexion caissier", self.test_cashier_login),
            ("Test permissions", self.test_cashier_permissions)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            print(f"\n📍 {step_name.upper()}...")
            success = step_func()
            if not success:
                all_success = False
                break
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU TEST")
        print("=" * 60)
        
        if all_success:
            print("🎉 TEST RÉUSSI!")
            print("✅ Utilisateur caissier créé avec succès")
            print("✅ Permissions correctement configurées")
            print("✅ Accès autorisés fonctionnent")
            print("✅ Accès interdits sont bloqués")
            print("\n🚀 INFORMATIONS DE CONNEXION:")
            print("  Username: test_caissier")
            print("  Password: caissier123")
            print("  URL: http://localhost:5173")
            print("\n💡 VOUS POUVEZ MAINTENANT:")
            print("  1. Vous connecter avec ces identifiants")
            print("  2. Tester les fonctionnalités de vente")
            print("  3. Vérifier que l'ajout de produits est bloqué")
        else:
            print("❌ TEST ÉCHOUÉ")
            print("Des problèmes ont été détectés dans la configuration")
        
        return all_success

if __name__ == "__main__":
    tester = CashierUserTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n🎊 FÉLICITATIONS!")
        print("Le système de création d'utilisateurs fonctionne parfaitement!")
    else:
        print("\n⚠️ Des corrections sont nécessaires...")
    
    sys.exit(0 if success else 1)
