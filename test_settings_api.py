#!/usr/bin/env python3
"""
Test script pour vérifier le fonctionnement de l'API Settings
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_settings_api():
    """Test complet de l'API Settings"""
    
    print("🧪 Test de l'API Settings - BarStockWise")
    print("=" * 50)
    
    # 1. Test de récupération des paramètres système
    print("\n1. 📥 Test de récupération des paramètres système")
    try:
        response = requests.get(f"{API_BASE}/settings/system/")
        if response.status_code == 200:
            settings = response.json()
            print("✅ Paramètres récupérés avec succès")
            print(f"   Restaurant: {settings.get('restaurant', {}).get('name', 'N/A')}")
            print(f"   Devise: {settings.get('restaurant', {}).get('currency', 'N/A')}")
            print(f"   Langue: {settings.get('system', {}).get('language', 'N/A')}")
            print(f"   Notifications email: {settings.get('notifications', {}).get('email_enabled', 'N/A')}")
        else:
            print(f"❌ Erreur récupération: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
    
    # 2. Test de mise à jour des paramètres
    print("\n2. 💾 Test de mise à jour des paramètres")
    try:
        update_data = {
            "restaurant": {
                "name": "BarStockWise Test",
                "currency": "BIF",
                "tax_rate": 18.0
            },
            "notifications": {
                "email_enabled": True,
                "low_stock_alerts": True,
                "daily_reports": False
            },
            "system": {
                "language": "fr",
                "timezone": "Africa/Bujumbura"
            }
        }
        
        response = requests.patch(
            f"{API_BASE}/settings/system/",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("✅ Paramètres mis à jour avec succès")
            updated_settings = response.json()
            print(f"   Nouveau nom: {updated_settings.get('restaurant', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Erreur mise à jour: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur mise à jour: {e}")
    
    # 3. Test des informations système
    print("\n3. 📊 Test des informations système")
    try:
        response = requests.get(f"{API_BASE}/settings/system-info/")
        if response.status_code == 200:
            info = response.json()
            print("✅ Informations système récupérées")
            print(f"   Version: {info.get('version', 'N/A')}")
            print(f"   Uptime: {info.get('uptime', 'N/A')}")
            print(f"   Dernière sauvegarde: {info.get('last_backup', 'N/A')}")
        else:
            print(f"❌ Erreur info système: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur info système: {e}")
    
    # 4. Test de création de sauvegarde
    print("\n4. 💾 Test de création de sauvegarde")
    try:
        response = requests.post(f"{API_BASE}/settings/backup/create/")
        if response.status_code == 200:
            backup_info = response.json()
            print("✅ Sauvegarde créée avec succès")
            print(f"   Fichier: {backup_info.get('filename', 'N/A')}")
        else:
            print(f"❌ Erreur sauvegarde: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
    
    # 5. Test de réinitialisation (optionnel - commenté pour éviter la perte de données)
    print("\n5. 🔄 Test de réinitialisation (simulé)")
    print("   ⚠️  Test de réinitialisation désactivé pour préserver les données")
    print("   ℹ️  Endpoint disponible: POST /api/settings/reset/")
    
    print("\n" + "=" * 50)
    print("🎯 Tests terminés!")

def test_frontend_connection():
    """Test de la connexion frontend"""
    print("\n🌐 Test de connexion frontend")
    try:
        response = requests.get(f"{BASE_URL}")
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print(f"❌ Frontend inaccessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur frontend: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests Settings API")
    
    # Test de la connexion de base
    test_frontend_connection()
    
    # Test de l'API Settings
    test_settings_api()
    
    print("\n✨ Tests terminés!")
