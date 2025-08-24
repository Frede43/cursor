#!/usr/bin/env python
"""
Test simple des dialogs avec diagnostic détaillé
"""

import requests
import json
from datetime import datetime, date, time, timedelta

def simple_dialog_test():
    """Test simple et diagnostic"""
    print("🔍 DIAGNOSTIC SIMPLE DIALOGS")
    print("=" * 50)
    
    # Connexion
    try:
        response = requests.post('http://localhost:8000/api/accounts/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        
        if response.status_code != 200:
            print(f"❌ Connexion échouée: {response.status_code}")
            return False
        
        token = response.json()['tokens']['access']
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        print("✅ Connecté")
        
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    # Test 1: Réservations
    print("\n📅 TEST RÉSERVATIONS...")
    try:
        # GET réservations
        reservations_response = requests.get('http://localhost:8000/api/sales/reservations/', headers=headers)
        print(f"GET réservations: {reservations_response.status_code}")
        
        if reservations_response.status_code == 200:
            reservations = reservations_response.json()
            print(f"✅ Réservations récupérées: {len(reservations.get('results', []))}")
            
            # Test création réservation simple
            tables_response = requests.get('http://localhost:8000/api/sales/tables/', headers=headers)
            if tables_response.status_code == 200:
                tables = tables_response.json().get('results', [])
                if tables:
                    table_id = tables[0]['id']
                    
                    # Données réservation minimales
                    reservation_data = {
                        'table': table_id,
                        'customer_name': 'Test Client',
                        'party_size': 2,
                        'reservation_date': (date.today() + timedelta(days=1)).isoformat(),
                        'reservation_time': '19:00:00'
                    }
                    
                    print(f"Création réservation avec données: {reservation_data}")
                    
                    create_response = requests.post(
                        'http://localhost:8000/api/sales/reservations/',
                        json=reservation_data,
                        headers=headers
                    )
                    
                    print(f"Création réservation: {create_response.status_code}")
                    if create_response.status_code in [200, 201]:
                        print("✅ Réservation créée avec succès")
                        reservation = create_response.json()
                        print(f"   ID: {reservation.get('id')}")
                        print(f"   Client: {reservation.get('customer_name')}")
                    else:
                        print(f"❌ Erreur création: {create_response.text}")
                else:
                    print("❌ Aucune table disponible")
            else:
                print(f"❌ Erreur tables: {tables_response.status_code}")
        else:
            print(f"❌ Erreur GET réservations: {reservations_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur test réservations: {e}")
    
    # Test 2: Commandes
    print("\n📝 TEST COMMANDES...")
    try:
        # GET commandes
        orders_response = requests.get('http://localhost:8000/api/orders/', headers=headers)
        print(f"GET commandes: {orders_response.status_code}")
        
        if orders_response.status_code == 200:
            orders = orders_response.json()
            print(f"✅ Commandes récupérées: {len(orders.get('results', []))}")
            
            # Test création commande simple
            tables_response = requests.get('http://localhost:8000/api/sales/tables/', headers=headers)
            products_response = requests.get('http://localhost:8000/api/products/', headers=headers)
            
            if tables_response.status_code == 200 and products_response.status_code == 200:
                tables = tables_response.json().get('results', [])
                products = products_response.json()
                
                if tables and products:
                    table_id = tables[0]['id']
                    product_id = products[0]['id']
                    
                    # Données commande minimales
                    order_data = {
                        'table': table_id,
                        'customer_name': 'Test Client Commande',
                        'status': 'pending',
                        'items': [
                            {
                                'product': product_id,
                                'quantity': 1,
                                'unit_price': float(products[0]['selling_price'])
                            }
                        ]
                    }
                    
                    print(f"Création commande avec données: {json.dumps(order_data, indent=2)}")
                    
                    create_response = requests.post(
                        'http://localhost:8000/api/orders/',
                        json=order_data,
                        headers=headers
                    )
                    
                    print(f"Création commande: {create_response.status_code}")
                    if create_response.status_code in [200, 201]:
                        print("✅ Commande créée avec succès")
                        order = create_response.json()
                        print(f"   Numéro: {order.get('order_number')}")
                        print(f"   Total: {order.get('total_amount')} BIF")
                    else:
                        print(f"❌ Erreur création commande: {create_response.text}")
                else:
                    print("❌ Données insuffisantes (tables ou produits)")
            else:
                print(f"❌ Erreur récupération données")
        else:
            print(f"❌ Erreur GET commandes: {orders_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur test commandes: {e}")
    
    # Test 3: Endpoints disponibles
    print("\n🔗 TEST ENDPOINTS...")
    endpoints = [
        '/api/sales/tables/',
        '/api/sales/reservations/',
        '/api/orders/',
        '/api/products/'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur {e}")
    
    print("\n📊 RÉSUMÉ:")
    print("1. ✅ Connexion API fonctionnelle")
    print("2. 🧪 Tests réservations et commandes effectués")
    print("3. 🔗 Endpoints principaux testés")
    print("\n💡 PROCHAINES ÉTAPES:")
    print("1. Corriger les erreurs 500 dans les APIs")
    print("2. Connecter le frontend aux APIs")
    print("3. Remplacer les fonctions mock")
    
    return True

if __name__ == "__main__":
    simple_dialog_test()
