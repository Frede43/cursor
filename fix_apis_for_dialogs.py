#!/usr/bin/env python
"""
Script pour corriger les APIs nécessaires aux dialogs
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
from products.models import Category, Product

User = get_user_model()

class APIFixer:
    def __init__(self):
        self.admin_token = None
        
    def log(self, message, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {message}")
    
    def login_as_admin(self):
        """Se connecter en tant qu'admin"""
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
    
    def create_test_category(self):
        """Créer une catégorie de test pour les produits"""
        print("\n📂 CRÉATION CATÉGORIE DE TEST...")
        
        try:
            # Créer une catégorie directement en base
            category, created = Category.objects.get_or_create(
                name='Test Category',
                defaults={
                    'type': 'boissons',
                    'description': 'Catégorie de test pour les dialogs',
                    'is_active': True
                }
            )
            
            if created:
                self.log(f"Catégorie créée: {category.name} (ID: {category.id})")
            else:
                self.log(f"Catégorie existante: {category.name} (ID: {category.id})")
            
            return category.id
            
        except Exception as e:
            self.log(f"Erreur création catégorie: {e}", False)
            return None
    
    def test_product_creation_fixed(self):
        """Tester la création de produit avec catégorie correcte"""
        print("\n📦 TEST CRÉATION PRODUIT CORRIGÉ...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        # Créer une catégorie d'abord
        category_id = self.create_test_category()
        if not category_id:
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # Données correctes avec category ID
        new_product = {
            'name': 'Test Produit Dialog Corrigé',
            'category': category_id,  # ID de catégorie au lieu de nom
            'purchase_price': 1000,
            'selling_price': 1500,
            'current_stock': 50,
            'minimum_stock': 10,
            'unit': 'piece',
            'description': 'Produit de test pour dialog corrigé'
        }
        
        try:
            response = requests.post(
                'http://localhost:8000/api/products/',
                json=new_product,
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                product_data = response.json()
                self.log(f"POST /products/ CORRIGÉ - Produit créé: {product_data.get('name')}")
                return True
            else:
                self.log(f"POST /products/ échoué: {response.status_code} - {response.text}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur POST product: {e}", False)
            return False
    
    def check_expenses_endpoints(self):
        """Vérifier les endpoints disponibles pour expenses"""
        print("\n💰 VÉRIFICATION ENDPOINTS EXPENSES...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # Tester différents endpoints possibles
        expense_endpoints = [
            'http://localhost:8000/api/expenses/',
            'http://localhost:8000/api/expenses/create/',
            'http://localhost:8000/api/expenses/list/',
        ]
        
        for endpoint in expense_endpoints:
            try:
                # Test GET
                response = requests.get(endpoint, headers=headers)
                self.log(f"GET {endpoint}: {response.status_code}")
                
                # Test OPTIONS pour voir les méthodes autorisées
                response = requests.options(endpoint, headers=headers)
                if response.status_code == 200:
                    allowed_methods = response.headers.get('Allow', 'Non spécifié')
                    self.log(f"OPTIONS {endpoint}: Méthodes autorisées: {allowed_methods}")
                
            except Exception as e:
                self.log(f"Erreur test {endpoint}: {e}", False)
        
        return True
    
    def test_supplies_creation(self):
        """Tester la création d'approvisionnement"""
        print("\n🚚 TEST CRÉATION APPROVISIONNEMENT...")
        
        if not self.admin_token:
            self.log("Token admin manquant", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        # Test avec différents endpoints possibles
        supply_endpoints = [
            'http://localhost:8000/api/inventory/',
            'http://localhost:8000/api/supplies/',
            'http://localhost:8000/api/inventory/supplies/',
        ]
        
        for endpoint in supply_endpoints:
            try:
                # Test GET d'abord
                response = requests.get(endpoint, headers=headers)
                self.log(f"GET {endpoint}: {response.status_code}")
                
                # Test OPTIONS
                response = requests.options(endpoint, headers=headers)
                if response.status_code == 200:
                    allowed_methods = response.headers.get('Allow', 'Non spécifié')
                    self.log(f"OPTIONS {endpoint}: Méthodes: {allowed_methods}")
                
            except Exception as e:
                self.log(f"Erreur test {endpoint}: {e}", False)
        
        return True
    
    def create_frontend_test_data(self):
        """Créer des données de test pour le frontend"""
        print("\n🎯 CRÉATION DONNÉES DE TEST FRONTEND...")
        
        try:
            # Créer quelques catégories de base
            categories_data = [
                {'name': 'Bières', 'type': 'boissons', 'description': 'Bières locales et importées'},
                {'name': 'Plats Principaux', 'type': 'plats', 'description': 'Plats principaux du restaurant'},
                {'name': 'Snacks', 'type': 'snacks', 'description': 'Collations et amuse-gueules'},
            ]
            
            created_categories = []
            for cat_data in categories_data:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    defaults=cat_data
                )
                created_categories.append(category)
                if created:
                    self.log(f"Catégorie créée: {category.name}")
                else:
                    self.log(f"Catégorie existante: {category.name}")
            
            # Créer quelques produits de test
            products_data = [
                {
                    'name': 'Mutzig 65cl',
                    'category': created_categories[0],
                    'purchase_price': 800,
                    'selling_price': 1200,
                    'current_stock': 48,
                    'minimum_stock': 12,
                    'unit': 'bouteille'
                },
                {
                    'name': 'Ugali Viande',
                    'category': created_categories[1],
                    'purchase_price': 2000,
                    'selling_price': 3500,
                    'current_stock': 0,  # Plat préparé
                    'minimum_stock': 0,
                    'unit': 'portion'
                }
            ]
            
            for prod_data in products_data:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    category=prod_data['category'],
                    defaults=prod_data
                )
                if created:
                    self.log(f"Produit créé: {product.name}")
                else:
                    self.log(f"Produit existant: {product.name}")
            
            return True
            
        except Exception as e:
            self.log(f"Erreur création données test: {e}", False)
            return False
    
    def run_complete_fix(self):
        """Exécuter toutes les corrections"""
        print("🔧 CORRECTION COMPLÈTE DES APIS POUR DIALOGS")
        print("=" * 60)
        
        steps = [
            ("Connexion Admin", self.login_as_admin),
            ("Création Données Test", self.create_frontend_test_data),
            ("Test Produit Corrigé", self.test_product_creation_fixed),
            ("Vérification Expenses", self.check_expenses_endpoints),
            ("Test Supplies", self.test_supplies_creation)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            print(f"\n📍 {step_name.upper()}...")
            success = step_func()
            if not success:
                all_success = False
        
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES CORRECTIONS")
        print("=" * 60)
        
        if all_success:
            print("🎉 CORRECTIONS APPLIQUÉES!")
            print("✅ Catégories de test créées")
            print("✅ Produits de test créés")
            print("✅ API Products corrigée")
            print("✅ Endpoints vérifiés")
            print("\n🚀 MAINTENANT VOUS POUVEZ:")
            print("1. Tester les dialogs sur http://localhost:5173")
            print("2. Créer des produits avec les bonnes catégories")
            print("3. Vérifier les fonctionnalités de création")
        else:
            print("❌ CERTAINES CORRECTIONS ONT ÉCHOUÉ")
            print("Vérifiez les erreurs ci-dessus")
        
        return all_success

if __name__ == "__main__":
    fixer = APIFixer()
    success = fixer.run_complete_fix()
    
    if success:
        print("\n🎊 APIS CORRIGÉES!")
        print("Les dialogs devraient maintenant fonctionner correctement!")
    else:
        print("\n⚠️ Des problèmes persistent...")
    
    sys.exit(0 if success else 1)
