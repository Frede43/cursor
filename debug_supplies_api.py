#!/usr/bin/env python
"""
Debug simple de l'API supplies
"""

import requests
import json

def debug_supplies_api():
    """Debug simple de l'API"""
    print("🔍 DEBUG API SUPPLIES")
    print("=" * 40)
    
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
    
    # Test API supplies
    print("\n📦 Test API Supplies...")
    response = requests.get('http://localhost:8000/api/inventory/supplies/', headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Type de données: {type(data)}")
            print(f"Nombre d'éléments: {len(data) if isinstance(data, list) else 'N/A'}")
            
            if isinstance(data, list) and data:
                print("\nPremier élément:")
                print(json.dumps(data[0], indent=2, default=str))
            elif isinstance(data, dict):
                print("\nStructure des données:")
                print(json.dumps(data, indent=2, default=str))
            else:
                print("Données vides ou format inattendu")
                
        except Exception as e:
            print(f"Erreur parsing JSON: {e}")
            print(f"Contenu brut: {response.text[:500]}")
    else:
        print(f"Erreur: {response.text}")
    
    # Test création simple
    print("\n🚀 Test création simple...")
    
    # D'abord, récupérer les fournisseurs
    suppliers_response = requests.get('http://localhost:8000/api/suppliers/', headers=headers)
    if suppliers_response.status_code == 200:
        suppliers = suppliers_response.json()
        print(f"Fournisseurs disponibles: {len(suppliers)}")
        
        if suppliers:
            supplier_id = suppliers[0]['id']
            print(f"Utilisation fournisseur ID: {supplier_id}")
            
            # Récupérer les produits
            products_response = requests.get('http://localhost:8000/api/products/', headers=headers)
            if products_response.status_code == 200:
                products = products_response.json()
                print(f"Produits disponibles: {len(products)}")
                
                if products:
                    product_id = products[0]['id']
                    print(f"Utilisation produit ID: {product_id}")
                    
                    # Créer un approvisionnement simple
                    supply_data = {
                        'supplier': supplier_id,
                        'delivery_date': '2025-08-24',
                        'status': 'pending',
                        'notes': 'Test debug simple',
                        'items': [
                            {
                                'product': product_id,
                                'quantity_ordered': 10,
                                'quantity_received': 0,
                                'unit_price': 1000
                            }
                        ]
                    }
                    
                    print(f"\nDonnées à envoyer:")
                    print(json.dumps(supply_data, indent=2))
                    
                    create_response = requests.post(
                        'http://localhost:8000/api/inventory/supplies/',
                        json=supply_data,
                        headers=headers
                    )
                    
                    print(f"\nCréation - Status: {create_response.status_code}")
                    if create_response.status_code in [200, 201]:
                        print("✅ Création réussie!")
                        created_data = create_response.json()
                        print(json.dumps(created_data, indent=2, default=str))
                    else:
                        print(f"❌ Erreur création: {create_response.text}")
                else:
                    print("Aucun produit disponible")
            else:
                print(f"Erreur récupération produits: {products_response.status_code}")
        else:
            print("Aucun fournisseur disponible")
    else:
        print(f"Erreur récupération fournisseurs: {suppliers_response.status_code}")

if __name__ == "__main__":
    debug_supplies_api()
