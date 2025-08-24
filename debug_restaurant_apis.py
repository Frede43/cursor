#!/usr/bin/env python
"""
Debug des APIs restaurant pour comprendre la structure des données
"""

import requests
import json

def debug_restaurant_apis():
    """Debug toutes les APIs restaurant"""
    print("🔍 DEBUG APIS RESTAURANT")
    print("=" * 50)
    
    # Connexion
    response = requests.post('http://localhost:8000/api/accounts/login/', {
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code != 200:
        print("❌ Connexion échouée")
        return
    
    token = response.json()['tokens']['access']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("✅ Connecté")
    
    # 1. DEBUG TABLES
    print("\n🪑 DEBUG TABLES API...")
    tables_response = requests.get('http://localhost:8000/api/sales/tables/', headers=headers)
    print(f"Status: {tables_response.status_code}")
    
    if tables_response.status_code == 200:
        try:
            tables_data = tables_response.json()
            print(f"Type: {type(tables_data)}")
            print(f"Longueur: {len(tables_data) if isinstance(tables_data, list) else 'N/A'}")
            
            if isinstance(tables_data, list) and tables_data:
                print("Premier élément:")
                print(json.dumps(tables_data[0], indent=2, default=str))
            elif isinstance(tables_data, dict):
                print("Structure dict:")
                print(json.dumps(tables_data, indent=2, default=str))
        except Exception as e:
            print(f"Erreur parsing: {e}")
            print(f"Contenu brut: {tables_response.text[:500]}")
    else:
        print(f"Erreur: {tables_response.text}")
    
    # 2. DEBUG ORDERS
    print("\n📝 DEBUG ORDERS API...")
    orders_response = requests.get('http://localhost:8000/api/orders/', headers=headers)
    print(f"Status: {orders_response.status_code}")
    
    if orders_response.status_code == 200:
        try:
            orders_data = orders_response.json()
            print(f"Type: {type(orders_data)}")
            if isinstance(orders_data, dict) and 'results' in orders_data:
                print(f"Commandes: {len(orders_data['results'])}")
                if orders_data['results']:
                    print("Première commande:")
                    print(json.dumps(orders_data['results'][0], indent=2, default=str))
            elif isinstance(orders_data, list):
                print(f"Commandes: {len(orders_data)}")
                if orders_data:
                    print("Première commande:")
                    print(json.dumps(orders_data[0], indent=2, default=str))
        except Exception as e:
            print(f"Erreur parsing orders: {e}")
    else:
        print(f"Erreur orders: {orders_response.text}")
    
    # 3. DEBUG SALES
    print("\n💰 DEBUG SALES API...")
    sales_response = requests.get('http://localhost:8000/api/sales/', headers=headers)
    print(f"Status: {sales_response.status_code}")
    
    if sales_response.status_code == 200:
        try:
            sales_data = sales_response.json()
            print(f"Type: {type(sales_data)}")
            if isinstance(sales_data, list):
                print(f"Ventes: {len(sales_data)}")
                if sales_data:
                    print("Première vente:")
                    print(json.dumps(sales_data[0], indent=2, default=str))
        except Exception as e:
            print(f"Erreur parsing sales: {e}")
    else:
        print(f"Erreur sales: {sales_response.text}")
    
    # 4. TEST CRÉATION SIMPLE
    print("\n🧪 TEST CRÉATION SIMPLE...")
    
    # Test création table si nécessaire
    if tables_response.status_code == 200:
        tables_data = tables_response.json()
        if isinstance(tables_data, list) and len(tables_data) == 0:
            print("Création table test...")
            table_data = {
                'number': 'T1',
                'capacity': 4,
                'status': 'available',
                'location': 'Salle principale'
            }
            
            create_table_response = requests.post(
                'http://localhost:8000/api/sales/tables/',
                json=table_data,
                headers=headers
            )
            
            print(f"Création table - Status: {create_table_response.status_code}")
            if create_table_response.status_code in [200, 201]:
                print("✅ Table créée")
                created_table = create_table_response.json()
                print(json.dumps(created_table, indent=2, default=str))
            else:
                print(f"❌ Erreur création table: {create_table_response.text}")
    
    # 5. TEST ENDPOINTS SPÉCIAUX
    print("\n🎯 TEST ENDPOINTS SPÉCIAUX...")
    
    # Test endpoint occupation table
    if tables_response.status_code == 200:
        tables_data = tables_response.json()
        if isinstance(tables_data, list) and tables_data:
            table_id = tables_data[0].get('id') if isinstance(tables_data[0], dict) else None
            if table_id:
                print(f"Test occupation table ID: {table_id}")
                occupy_response = requests.post(
                    f'http://localhost:8000/api/sales/tables/{table_id}/occupy/',
                    json={'customer_name': 'Test Client', 'party_size': 2},
                    headers=headers
                )
                print(f"Occupation - Status: {occupy_response.status_code}")
                if occupy_response.status_code == 200:
                    print("✅ Occupation réussie")
                else:
                    print(f"❌ Erreur occupation: {occupy_response.text}")

if __name__ == "__main__":
    debug_restaurant_apis()
