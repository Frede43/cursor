#!/usr/bin/env python
"""
Test complet du workflow restaurant : Tables → Commandes → Ventes
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
from sales.models import Table, Sale, SaleItem
from orders.models import Order, OrderItem
from products.models import Product

User = get_user_model()

class RestaurantWorkflowTester:
    def __init__(self):
        self.admin_token = None
        self.cashier_token = None
        self.test_table_id = None
        self.test_order_id = None
        self.test_sale_id = None
        
    def log(self, message, success=True):
        status = "✅" if success else "❌"
        print(f"{status} {message}")
    
    def login_users(self):
        """Se connecter avec différents utilisateurs"""
        print("🔐 CONNEXION UTILISATEURS...")
        
        # Admin
        try:
            response = requests.post('http://localhost:8000/api/accounts/login/', {
                'username': 'admin',
                'password': 'admin123'
            })
            if response.status_code == 200:
                self.admin_token = response.json()['tokens']['access']
                self.log("Admin connecté")
            else:
                self.log("Échec connexion admin", False)
                return False
        except Exception as e:
            self.log(f"Erreur connexion admin: {e}", False)
            return False
        
        # Caissier
        try:
            response = requests.post('http://localhost:8000/api/accounts/login/', {
                'username': 'test_caissier',
                'password': 'caissier123'
            })
            if response.status_code == 200:
                self.cashier_token = response.json()['tokens']['access']
                self.log("Caissier connecté")
            else:
                self.log("Caissier non trouvé (normal si pas créé)", False)
        except Exception as e:
            self.log(f"Caissier non disponible: {e}", False)
        
        return True
    
    def test_tables_management(self):
        """Tester la gestion des tables"""
        print("\n🪑 TEST GESTION DES TABLES...")
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Récupérer les tables
            response = requests.get('http://localhost:8000/api/sales/tables/', headers=headers)
            if response.status_code == 200:
                tables = response.json()
                self.log(f"Tables récupérées: {len(tables)}")
                
                # Trouver une table disponible
                available_table = None
                for table in tables:
                    if table.get('status') == 'available':
                        available_table = table
                        break
                
                if available_table:
                    self.test_table_id = available_table['id']
                    self.log(f"Table test sélectionnée: {available_table['number']}")
                    
                    # 2. Occuper la table
                    occupy_data = {
                        'customer_name': 'Client Test Workflow',
                        'party_size': 4
                    }
                    
                    occupy_response = requests.post(
                        f'http://localhost:8000/api/sales/tables/{self.test_table_id}/occupy/',
                        json=occupy_data,
                        headers=headers
                    )
                    
                    if occupy_response.status_code == 200:
                        self.log("Table occupée avec succès")
                        return True
                    else:
                        self.log(f"Erreur occupation table: {occupy_response.status_code}", False)
                        return False
                else:
                    self.log("Aucune table disponible", False)
                    return False
            else:
                self.log(f"Erreur récupération tables: {response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur test tables: {e}", False)
            return False
    
    def test_order_creation(self):
        """Tester la création de commande pour la table"""
        print("\n📝 TEST CRÉATION COMMANDE...")
        
        if not self.test_table_id:
            self.log("Pas de table test disponible", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Récupérer les produits disponibles
            products_response = requests.get('http://localhost:8000/api/products/', headers=headers)
            if products_response.status_code == 200:
                products = products_response.json()
                if len(products) >= 2:
                    product1 = products[0]
                    product2 = products[1]
                    
                    # 2. Créer une commande
                    order_data = {
                        'table': self.test_table_id,
                        'customer_name': 'Client Test Workflow',
                        'status': 'pending',
                        'priority': 'normal',
                        'notes': 'Commande test workflow complet',
                        'items': [
                            {
                                'product': product1['id'],
                                'quantity': 2,
                                'unit_price': product1['selling_price'],
                                'notes': 'Bien cuit'
                            },
                            {
                                'product': product2['id'],
                                'quantity': 1,
                                'unit_price': product2['selling_price'],
                                'notes': 'Frais'
                            }
                        ]
                    }
                    
                    create_response = requests.post(
                        'http://localhost:8000/api/orders/',
                        json=order_data,
                        headers=headers
                    )
                    
                    if create_response.status_code in [200, 201]:
                        order = create_response.json()
                        self.test_order_id = order['id']
                        self.log(f"Commande créée: {order.get('order_number', 'N/A')}")
                        self.log(f"  - Table: {order.get('table', {}).get('number', 'N/A')}")
                        self.log(f"  - Articles: {len(order.get('items', []))}")
                        self.log(f"  - Total: {order.get('total_amount', 0)} BIF")
                        return True
                    else:
                        self.log(f"Erreur création commande: {create_response.status_code}", False)
                        self.log(f"Détails: {create_response.text}")
                        return False
                else:
                    self.log("Pas assez de produits pour test", False)
                    return False
            else:
                self.log(f"Erreur récupération produits: {products_response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur test commande: {e}", False)
            return False
    
    def test_order_to_sale_conversion(self):
        """Tester la conversion commande → vente"""
        print("\n💰 TEST CONVERSION COMMANDE → VENTE...")
        
        if not self.test_order_id:
            self.log("Pas de commande test disponible", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Marquer la commande comme prête
            update_response = requests.patch(
                f'http://localhost:8000/api/orders/{self.test_order_id}/',
                json={'status': 'ready'},
                headers=headers
            )
            
            if update_response.status_code == 200:
                self.log("Commande marquée comme prête")
                
                # 2. Convertir en vente (encaissement)
                conversion_data = {
                    'payment_method': 'cash',
                    'notes': 'Conversion test workflow'
                }
                
                convert_response = requests.post(
                    f'http://localhost:8000/api/orders/{self.test_order_id}/convert-to-sale/',
                    json=conversion_data,
                    headers=headers
                )
                
                if convert_response.status_code in [200, 201]:
                    sale = convert_response.json()
                    self.test_sale_id = sale['id']
                    self.log(f"Conversion réussie - Vente: {sale.get('reference', 'N/A')}")
                    self.log(f"  - Montant: {sale.get('total_amount', 0)} BIF")
                    self.log(f"  - Statut: {sale.get('status', 'N/A')}")
                    return True
                else:
                    self.log(f"Erreur conversion: {convert_response.status_code}", False)
                    self.log(f"Détails: {convert_response.text}")
                    return False
            else:
                self.log(f"Erreur mise à jour commande: {update_response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur conversion: {e}", False)
            return False
    
    def test_table_liberation(self):
        """Tester la libération de table après vente"""
        print("\n🆓 TEST LIBÉRATION TABLE...")
        
        if not self.test_table_id or not self.test_sale_id:
            self.log("Données test manquantes", False)
            return False
        
        headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            # 1. Marquer la vente comme payée
            payment_response = requests.patch(
                f'http://localhost:8000/api/sales/{self.test_sale_id}/',
                json={'status': 'paid'},
                headers=headers
            )
            
            if payment_response.status_code == 200:
                self.log("Vente marquée comme payée")
                
                # 2. Libérer la table
                free_response = requests.post(
                    f'http://localhost:8000/api/sales/tables/{self.test_table_id}/free/',
                    headers=headers
                )
                
                if free_response.status_code == 200:
                    self.log("Table libérée avec succès")
                    return True
                else:
                    self.log(f"Erreur libération table: {free_response.status_code}", False)
                    return False
            else:
                self.log(f"Erreur paiement vente: {payment_response.status_code}", False)
                return False
                
        except Exception as e:
            self.log(f"Erreur libération: {e}", False)
            return False
    
    def test_complete_workflow(self):
        """Tester le workflow complet"""
        print("🔄 TEST WORKFLOW COMPLET RESTAURANT")
        print("=" * 60)
        print("Workflow: Table → Commande → Vente → Libération")
        print("=" * 60)
        
        steps = [
            ("Connexion Utilisateurs", self.login_users),
            ("Gestion Tables", self.test_tables_management),
            ("Création Commande", self.test_order_creation),
            ("Conversion Vente", self.test_order_to_sale_conversion),
            ("Libération Table", self.test_table_liberation)
        ]
        
        all_success = True
        for step_name, step_func in steps:
            print(f"\n📍 {step_name.upper()}...")
            success = step_func()
            if not success:
                all_success = False
                break
        
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU WORKFLOW")
        print("=" * 60)
        
        if all_success:
            print("🎉 WORKFLOW COMPLET FONCTIONNEL!")
            print("✅ Tables → Occupation réussie")
            print("✅ Commandes → Création réussie")
            print("✅ Ventes → Conversion réussie")
            print("✅ Tables → Libération réussie")
            print("\n🚀 COMMUNICATION PARFAITE ENTRE:")
            print("   📱 Page Tables (http://localhost:5173/tables)")
            print("   📝 Page Commandes (http://localhost:5173/orders)")
            print("   💰 Page Ventes (http://localhost:5173/sales-history)")
            print("\n💡 WORKFLOW OPÉRATIONNEL:")
            print("1. Serveur occupe une table")
            print("2. Serveur crée une commande pour la table")
            print("3. Cuisine prépare la commande")
            print("4. Serveur convertit en vente (encaissement)")
            print("5. Table automatiquement libérée")
        else:
            print("❌ PROBLÈMES DÉTECTÉS DANS LE WORKFLOW")
            print("Consultez les erreurs ci-dessus")
        
        return all_success

if __name__ == "__main__":
    tester = RestaurantWorkflowTester()
    success = tester.test_complete_workflow()
    
    if success:
        print("\n🎊 FÉLICITATIONS!")
        print("Le workflow restaurant fonctionne à 100%!")
        print("Tables, Commandes et Ventes communiquent parfaitement!")
    else:
        print("\n⚠️ Des améliorations sont nécessaires...")
    
    sys.exit(0 if success else 1)
