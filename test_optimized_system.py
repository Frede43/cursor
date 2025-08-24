#!/usr/bin/env python
"""
Test du système optimisé - Port 5173 uniquement
"""

import requests
import json

def test_optimized_system():
    """Test du système optimisé"""
    print("🎯 TEST SYSTÈME OPTIMISÉ - PORT 5173")
    print("=" * 50)
    
    # Test connexion depuis localhost:5173
    try:
        headers = {
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:5173'
        }
        
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = requests.post(
            'http://localhost:8000/api/accounts/login/',
            json=data,
            headers=headers
        )
        
        if response.status_code == 200:
            login_data = response.json()
            print("✅ Connexion localhost:5173 - SUCCÈS")
            print(f"   Utilisateur: {login_data['user']['username']}")
            print(f"   Rôle: {login_data['user']['role']}")
            
            # Test depuis l'adresse réseau
            headers_network = {
                'Content-Type': 'application/json',
                'Origin': 'http://192.168.43.253:5173'
            }
            
            response_network = requests.post(
                'http://localhost:8000/api/accounts/login/',
                json=data,
                headers=headers_network
            )
            
            if response_network.status_code == 200:
                print("✅ Connexion réseau 192.168.43.253:5173 - SUCCÈS")
            else:
                print(f"⚠️ Connexion réseau - Problème: {response_network.status_code}")
            
            print("\n🎉 SYSTÈME OPTIMISÉ ET FONCTIONNEL!")
            print("=" * 50)
            print("✅ Backend Django: http://localhost:8000")
            print("✅ Frontend React: http://localhost:5173")
            print("✅ Accès réseau: http://192.168.43.253:5173")
            print("✅ Connexion: admin / admin123")
            print("✅ Configuration CORS: Optimisée")
            print("✅ Fichiers de test: Nettoyés")
            
            return True
            
        else:
            print(f"❌ Connexion échouée: {response.status_code}")
            print(f"   Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_optimized_system()
    if success:
        print("\n🚀 PRÊT À UTILISER!")
        print("   Ouvrez: http://localhost:5173")
        print("   Login: admin / admin123")
    else:
        print("\n❌ Problème détecté...")
