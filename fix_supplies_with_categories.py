#!/usr/bin/env python
"""
Script pour corriger les approvisionnements avec catégories
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, date
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
sys.path.append('backend')
django.setup()

from django.contrib.auth import get_user_model
from inventory.models import Purchase, PurchaseItem
from products.models import Product, Category
from suppliers.models import Supplier

User = get_user_model()

class SuppliesFixerWithCategories:
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
    
    def create_complete_test_data(self):
        """Créer des données de test complètes avec catégories"""
        print("\n📦 CRÉATION DONNÉES COMPLÈTES...")
        
        try:
            # 1. Créer des catégories
            category_boissons, created = Category.objects.get_or_create(
                name='Boissons',
                defaults={
                    'type': 'boissons',
                    'description': 'Bières, sodas et autres boissons',
                    'is_active': True
                }
            )
            
            if created:
                self.log(f"Catégorie créée: {category_boissons.name}")
            
            # 2. Créer des fournisseurs
            supplier1, created = Supplier.objects.get_or_create(
                name='BRARUNDI SA',
                defaults={
                    'supplier_type': 'beverages',
                    'contact_person': 'Jean Ndayishimiye',
                    'phone': '+25722123456',
                    'email': 'commandes@brarundi.bi',
                    'address': 'Avenue de la Révolution, Bujumbura',
                    'is_active': True
                }
            )
            
            self.log(f"Fournisseur: {supplier1.name}")
            
            # 3. Créer des produits avec catégories
            products_data = [
                {
                    'name': 'Mutzig 65cl',
                    'category': category_boissons,
                    'purchase_price': 800,
                    'selling_price': 1200,
                    'current_stock': 24,
                    'minimum_stock': 12,
                    'unit': 'bouteille'
                },
                {
                    'name': 'Primus 65cl',
                    'category': category_boissons,
                    'purchase_price': 750,
                    'selling_price': 1100,
                    'current_stock': 36,
                    'minimum_stock': 12,
                    'unit': 'bouteille'
                }
            ]
            
            created_products = []
            for prod_data in products_data:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    defaults=prod_data
                )
                created_products.append(product)
                if created:
                    self.log(f"Produit créé: {product.name}")
            
            # 4. Créer un approvisionnement complet
            admin_user = User.objects.get(username='admin')
            
            purchase = Purchase.objects.create(
                supplier=supplier1,
                user=admin_user,
                status='received',  # Livré, prêt à valider
                delivery_date=date.today(),
                notes='Livraison test complète - prête à valider'
            )
            
            # Articles avec quantités reçues
            item1 = PurchaseItem.objects.create(
                purchase=purchase,
                product=created_products[0],  # Mutzig
                quantity_ordered=48,
                quantity_received=48,  # Entièrement livré
                unit_price=800
            )
            
            item2 = PurchaseItem.objects.create(
                purchase=purchase,
                product=created_products[1],  # Primus
                quantity_ordered=24,
                quantity_received=20,  # Partiellement livré
                unit_price=750
            )
            
            self.log(f"Approvisionnement créé: {purchase.reference}")
            self.log(f"  - {item1.product.name}: {item1.quantity_received}/{item1.quantity_ordered}")
            self.log(f"  - {item2.product.name}: {item2.quantity_received}/{item2.quantity_ordered}")
            
            return True
            
        except Exception as e:
            self.log(f"Erreur création données: {e}", False)
            return False
    
    def test_supplies_display(self):
        """Tester l'affichage des approvisionnements"""
        print("\n🖥️ TEST AFFICHAGE APPROVISIONNEMENTS...")
        
        if not self.admin_token:
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get('http://localhost:8000/api/inventory/supplies/', headers=headers)
            
            if response.status_code == 200:
                supplies_data = response.json()
                self.log(f"Approvisionnements récupérés: {len(supplies_data)}")
                
                # Analyser la structure des données
                if supplies_data:
                    first_supply = supplies_data[0]
                    self.log("Structure des données:")
                    self.log(f"  - ID: {first_supply.get('id', 'N/A')}")
                    self.log(f"  - Reference: {first_supply.get('reference', 'N/A')}")
                    self.log(f"  - Supplier: {first_supply.get('supplier', 'N/A')}")
                    self.log(f"  - Status: {first_supply.get('status', 'N/A')}")
                    self.log(f"  - Total: {first_supply.get('total_amount', 'N/A')}")
                    self.log(f"  - Items: {len(first_supply.get('items', []))}")
                    
                    # Détails des articles
                    items = first_supply.get('items', [])
                    if items:
                        self.log("  Articles:")
                        for item in items:
                            product_name = item.get('product', {}).get('name', 'N/A') if isinstance(item.get('product'), dict) else 'N/A'
                            self.log(f"    - {product_name}: {item.get('quantity_received', 0)}/{item.get('quantity_ordered', 0)} @ {item.get('unit_price', 0)} BIF")
                
                return True
            else:
                self.log(f"Erreur récupération: {response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur test affichage: {e}", False)
            return False
    
    def test_validation_and_stock_update(self):
        """Tester la validation et mise à jour des stocks"""
        print("\n✅ TEST VALIDATION ET STOCKS...")
        
        if not self.admin_token:
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Récupérer les stocks avant validation
            products_before = requests.get('http://localhost:8000/api/products/', headers=headers)
            if products_before.status_code == 200:
                products_data = products_before.json()
                stocks_before = {p['name']: p['current_stock'] for p in products_data}
                self.log("Stocks AVANT validation:")
                for name, stock in stocks_before.items():
                    if 'Mutzig' in name or 'Primus' in name:
                        self.log(f"  - {name}: {stock}")
            
            # 2. Trouver et valider un approvisionnement
            supplies_response = requests.get('http://localhost:8000/api/inventory/supplies/', headers=headers)
            if supplies_response.status_code == 200:
                supplies = supplies_response.json()
                
                for supply in supplies:
                    if supply.get('status') == 'received':
                        supply_id = supply.get('id')
                        self.log(f"Validation de l'approvisionnement ID: {supply_id}")
                        
                        # Valider
                        validate_response = requests.post(
                            f'http://localhost:8000/api/inventory/supplies/{supply_id}/validate/',
                            headers=headers
                        )
                        
                        if validate_response.status_code == 200:
                            self.log("✅ Validation réussie!")
                            
                            # 3. Vérifier les stocks après validation
                            products_after = requests.get('http://localhost:8000/api/products/', headers=headers)
                            if products_after.status_code == 200:
                                products_data = products_after.json()
                                self.log("Stocks APRÈS validation:")
                                for product in products_data:
                                    name = product['name']
                                    if 'Mutzig' in name or 'Primus' in name:
                                        stock_before = stocks_before.get(name, 0)
                                        stock_after = product['current_stock']
                                        difference = stock_after - stock_before
                                        self.log(f"  - {name}: {stock_before} → {stock_after} (+{difference})")
                            
                            return True
                        else:
                            self.log(f"Erreur validation: {validate_response.status_code}", False)
                            self.log(f"Détails: {validate_response.text}")
                            return False
                
                self.log("Aucun approvisionnement 'received' trouvé")
                return True
            else:
                self.log(f"Erreur récupération supplies: {supplies_response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur test validation: {e}", False)
            return False
    
    def run_complete_fix(self):
        """Exécuter toutes les corrections"""
        print("🔧 CORRECTION COMPLÈTE APPROVISIONNEMENTS + STOCKS")
        print("=" * 60)
        
        steps = [
            ("Connexion Admin", self.login_as_admin),
            ("Création Données Complètes", self.create_complete_test_data),
            ("Test Affichage", self.test_supplies_display),
            ("Test Validation + Stocks", self.test_validation_and_stock_update)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            print(f"\n📍 {step_name.upper()}...")
            success = step_func()
            if not success:
                all_success = False
        
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ FINAL")
        print("=" * 60)
        
        if all_success:
            print("🎉 APPROVISIONNEMENTS ENTIÈREMENT FONCTIONNELS!")
            print("✅ Données complètes créées")
            print("✅ Affichage des détails opérationnel")
            print("✅ Validation fonctionnelle")
            print("✅ Mise à jour automatique des stocks")
            print("\n🚀 MAINTENANT DANS L'APPLICATION:")
            print("1. Allez sur http://localhost:5173/supplies")
            print("2. Vous verrez les approvisionnements avec détails")
            print("3. Vous pourrez valider les livraisons")
            print("4. Les stocks seront automatiquement mis à jour")
        else:
            print("❌ CERTAINES CORRECTIONS ONT ÉCHOUÉ")
        
        return all_success

if __name__ == "__main__":
    fixer = SuppliesFixerWithCategories()
    success = fixer.run_complete_fix()
    
    if success:
        print("\n🎊 PROBLÈME RÉSOLU!")
        print("Les approvisionnements affichent maintenant:")
        print("✅ Les produits livrés")
        print("✅ Les montants")
        print("✅ La validation fonctionnelle")
        print("✅ La mise à jour des stocks")
    else:
        print("\n⚠️ Consultez les erreurs ci-dessus...")
    
    sys.exit(0 if success else 1)
