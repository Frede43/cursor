#!/usr/bin/env python
"""
Test des menus visibles pour le caissier
"""

import requests
import json

def test_cashier_menus():
    """Tester les menus visibles pour le caissier"""
    print("🎯 TEST DES MENUS CAISSIER")
    print("=" * 50)
    
    # 1. Connexion caissier
    print("🔐 Connexion caissier...")
    try:
        response = requests.post('http://localhost:8000/api/accounts/login/', {
            'username': 'test_caissier',
            'password': 'caissier123'
        })
        
        if response.status_code != 200:
            print("❌ Impossible de se connecter en tant que caissier")
            return False
        
        data = response.json()
        token = data['tokens']['access']
        user_info = data['user']
        
        print(f"✅ Caissier connecté: {user_info['username']} ({user_info['role']})")
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
    
    # 2. Récupérer les permissions
    print("\n🛡️ Vérification des permissions...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            'http://localhost:8000/api/accounts/check-permissions/',
            headers=headers
        )
        
        if response.status_code == 200:
            permissions_data = response.json()
            print(f"✅ Permissions récupérées pour rôle: {permissions_data['role']}")
            
            # Afficher les permissions
            permissions = permissions_data.get('permissions', {})
            print(f"📋 Permissions accordées ({len(permissions)}):")
            for perm_code, perm_info in permissions.items():
                if isinstance(perm_info, dict):
                    print(f"   ✅ {perm_code}: {perm_info.get('name', perm_code)}")
                else:
                    print(f"   ✅ {perm_code}")
            
            # Analyser quels menus devraient être visibles
            print(f"\n📱 MENUS QUI DEVRAIENT ÊTRE VISIBLES:")
            
            # Menus toujours visibles
            always_visible = [
                "Accueil (Dashboard)",
                "Mon Profil"
            ]
            
            # Menus selon permissions
            menu_mapping = {
                'sales_manage': "Ventes",
                'sales_history_view': "Historique des Ventes", 
                'tables_manage': "Tables",
                'products_view': "Produits (lecture seule)"
            }
            
            print("   🏠 Toujours visibles:")
            for menu in always_visible:
                print(f"      ✅ {menu}")
            
            print("   🔐 Selon permissions:")
            for perm_code, menu_name in menu_mapping.items():
                if perm_code in permissions:
                    print(f"      ✅ {menu_name} (permission: {perm_code})")
                else:
                    print(f"      ❌ {menu_name} (permission manquante: {perm_code})")
            
            # Menus qui NE devraient PAS être visibles
            print(f"\n🚫 MENUS QUI NE DEVRAIENT PAS ÊTRE VISIBLES:")
            forbidden_menus = [
                "Utilisateurs (admin seulement)",
                "Fournisseurs (admin/manager seulement)", 
                "Ajout de Produits (pas de permission products_manage)",
                "Paramètres Système",
                "Surveillance"
            ]
            
            for menu in forbidden_menus:
                print(f"      ❌ {menu}")
            
            return True
        else:
            print(f"❌ Erreur récupération permissions: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_menu_access():
    """Tester l'accès aux différentes pages"""
    print("\n🌐 TEST D'ACCÈS AUX PAGES")
    print("=" * 50)
    
    # Connexion caissier
    response = requests.post('http://localhost:8000/api/accounts/login/', {
        'username': 'test_caissier',
        'password': 'caissier123'
    })
    
    if response.status_code != 200:
        print("❌ Impossible de se connecter")
        return False
    
    token = response.json()['tokens']['access']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Tests d'accès
    access_tests = [
        {
            'name': 'Ventes',
            'url': 'http://localhost:8000/api/sales/',
            'should_work': True
        },
        {
            'name': 'Tables', 
            'url': 'http://localhost:8000/api/sales/tables/',
            'should_work': True
        },
        {
            'name': 'Produits',
            'url': 'http://localhost:8000/api/products/',
            'should_work': True
        },
        {
            'name': 'Utilisateurs (interdit)',
            'url': 'http://localhost:8000/api/accounts/users/',
            'should_work': False
        },
        {
            'name': 'Fournisseurs (interdit)',
            'url': 'http://localhost:8000/api/suppliers/',
            'should_work': False
        }
    ]
    
    all_passed = True
    
    for test in access_tests:
        try:
            response = requests.get(test['url'], headers=headers)
            
            if test['should_work']:
                if response.status_code == 200:
                    print(f"✅ {test['name']}: Accès autorisé (comme attendu)")
                else:
                    print(f"❌ {test['name']}: Accès refusé (HTTP {response.status_code}) - PROBLÈME!")
                    all_passed = False
            else:
                if response.status_code == 403:
                    print(f"✅ {test['name']}: Accès refusé (comme attendu)")
                else:
                    print(f"❌ {test['name']}: Accès autorisé (HTTP {response.status_code}) - PROBLÈME!")
                    all_passed = False
                    
        except Exception as e:
            print(f"❌ {test['name']}: Erreur - {e}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🧪 TEST COMPLET DES MENUS CAISSIER")
    print("=" * 60)
    print("Objectif: Vérifier que les menus correspondent aux permissions")
    print("=" * 60)
    
    success1 = test_cashier_menus()
    success2 = test_menu_access()
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    if success1 and success2:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Les permissions sont correctement configurées")
        print("✅ Les accès fonctionnent comme attendu")
        print("\n🚀 INSTRUCTIONS:")
        print("1. Connectez-vous sur http://localhost:5173")
        print("2. Utilisez: test_caissier / caissier123")
        print("3. Vérifiez que seuls les menus autorisés sont visibles")
        print("4. Testez que vous ne pouvez pas accéder aux fonctions interdites")
    else:
        print("❌ DES PROBLÈMES ONT ÉTÉ DÉTECTÉS")
        print("Vérifiez la configuration des permissions")
    
    print("\n💡 MENUS ATTENDUS POUR LE CAISSIER:")
    print("   ✅ Accueil")
    print("   ✅ Mon Profil") 
    print("   ✅ Ventes")
    print("   ✅ Historique des Ventes")
    print("   ✅ Tables")
    print("   ✅ Produits (lecture seule)")
    print("   ❌ Utilisateurs")
    print("   ❌ Fournisseurs")
    print("   ❌ Ajout de Produits")
