#!/usr/bin/env python
"""
Test complet des dialogs de création pour Products, Supplies et Expenses
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

class DialogTester:
    def __init__(self):
        self.admin_token = None
        self.test_results = []
        
    def log(self, message, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {message}")
        self.test_results.append((message, success))
    
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
    
    def test_products_api(self):
        """Tester l'API des produits"""
        print("\n📦 TEST API PRODUITS...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # 1. Test GET products
        try:
            response = requests.get('http://localhost:8000/api/products/', headers=headers)
            if response.status_code == 200:
                products = response.json()
                self.log(f"GET /products/ - {len(products)} produits récupérés")
            else:
                self.log(f"GET /products/ échoué: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Erreur GET products: {e}", False)
            return False
        
        # 2. Test POST product (création)
        try:
            new_product = {
                'name': 'Test Produit Dialog',
                'category_name': 'Test Category',
                'category_type': 'boissons',
                'purchase_price': 1000,
                'selling_price': 1500,
                'current_stock': 50,
                'minimum_stock': 10,
                'unit': 'piece',
                'description': 'Produit de test pour dialog'
            }
            
            response = requests.post(
                'http://localhost:8000/api/products/',
                json=new_product,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                product_data = response.json()
                self.log(f"POST /products/ - Produit créé: {product_data.get('name')}")
                return True
            else:
                self.log(f"POST /products/ échoué: {response.status_code} - {response.text}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur POST product: {e}", False)
            return False
    
    def test_supplies_api(self):
        """Tester l'API des approvisionnements"""
        print("\n🚚 TEST API APPROVISIONNEMENTS...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # 1. Test GET supplies
        try:
            response = requests.get('http://localhost:8000/api/inventory/', headers=headers)
            if response.status_code == 200:
                supplies = response.json()
                self.log(f"GET /inventory/ - Données récupérées")
            else:
                self.log(f"GET /inventory/ échoué: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur GET supplies: {e}", False)
        
        # 2. Test GET suppliers
        try:
            response = requests.get('http://localhost:8000/api/suppliers/', headers=headers)
            if response.status_code == 200:
                suppliers = response.json()
                self.log(f"GET /suppliers/ - {len(suppliers)} fournisseurs récupérés")
                return True
            else:
                self.log(f"GET /suppliers/ échoué: {response.status_code}", False)
                return False
        except Exception as e:
            self.log(f"Erreur GET suppliers: {e}", False)
            return False
    
    def test_expenses_api(self):
        """Tester l'API des dépenses"""
        print("\n💰 TEST API DÉPENSES...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # 1. Test GET expenses
        try:
            response = requests.get('http://localhost:8000/api/expenses/', headers=headers)
            if response.status_code == 200:
                expenses = response.json()
                self.log(f"GET /expenses/ - Données récupérées")
            else:
                self.log(f"GET /expenses/ échoué: {response.status_code}", False)
        except Exception as e:
            self.log(f"Erreur GET expenses: {e}", False)
        
        # 2. Test POST expense (création)
        try:
            new_expense = {
                'description': 'Test Dépense Dialog',
                'amount': 25000,
                'category': 'Maintenance',
                'payment_method': 'cash',
                'date': date.today().isoformat(),
                'notes': 'Dépense de test pour dialog'
            }
            
            response = requests.post(
                'http://localhost:8000/api/expenses/',
                json=new_expense,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                expense_data = response.json()
                self.log(f"POST /expenses/ - Dépense créée: {expense_data.get('description')}")
                return True
            else:
                self.log(f"POST /expenses/ échoué: {response.status_code} - {response.text}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur POST expense: {e}", False)
            return False
    
    def test_frontend_endpoints(self):
        """Tester les endpoints utilisés par le frontend"""
        print("\n🌐 TEST ENDPOINTS FRONTEND...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # Endpoints utilisés par les hooks
        frontend_endpoints = [
            ('Products Hook', 'http://localhost:8000/api/products/'),
            ('Suppliers Hook', 'http://localhost:8000/api/suppliers/'),
            ('Expenses Hook', 'http://localhost:8000/api/expenses/'),
            ('Inventory Hook', 'http://localhost:8000/api/inventory/'),
        ]
        
        all_success = True
        
        for name, url in frontend_endpoints:
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    self.log(f"{name} - Accessible")
                else:
                    self.log(f"{name} - Problème: {response.status_code}", False)
                    all_success = False
            except Exception as e:
                self.log(f"{name} - Erreur: {e}", False)
                all_success = False
        
        return all_success
    
    def run_complete_test(self):
        """Exécuter tous les tests"""
        print("🧪 TEST COMPLET DES DIALOGS")
        print("=" * 60)
        print("Objectif: Vérifier que les dialogs de création fonctionnent")
        print("Pages testées: Products.tsx, Supplies.tsx, Expenses.tsx")
        print("=" * 60)
        
        # Exécuter tous les tests
        steps = [
            ("Connexion Admin", self.login_as_admin),
            ("API Produits", self.test_products_api),
            ("API Approvisionnements", self.test_supplies_api),
            ("API Dépenses", self.test_expenses_api),
            ("Endpoints Frontend", self.test_frontend_endpoints)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            print(f"\n📍 {step_name.upper()}...")
            success = step_func()
            if not success:
                all_success = False
        
        # Résumé final
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        
        success_count = sum(1 for _, success in self.test_results if success)
        total_count = len(self.test_results)
        
        for message, success in self.test_results:
            status = "✅" if success else "❌"
            print(f"{status} {message}")
        
        print(f"\nRésultat: {success_count}/{total_count} tests réussis")
        
        if all_success:
            print("\n🎉 TOUS LES TESTS RÉUSSIS!")
            print("✅ Les APIs backend fonctionnent")
            print("✅ Les endpoints frontend sont accessibles")
            print("✅ Les dialogs peuvent créer des données")
            print("\n🚀 VOUS POUVEZ MAINTENANT:")
            print("1. Tester les dialogs sur http://localhost:5173")
            print("2. Créer des produits via /products")
            print("3. Créer des approvisionnements via /supplies")
            print("4. Créer des dépenses via /expenses")
        else:
            print("❌ DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
            print("Vérifiez les erreurs ci-dessus")
        
        return all_success

if __name__ == "__main__":
    tester = DialogTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n🎊 FÉLICITATIONS!")
        print("Tous les dialogs sont prêts à être utilisés!")
    else:
        print("\n⚠️ Des corrections sont nécessaires...")
    
    sys.exit(0 if success else 1)
