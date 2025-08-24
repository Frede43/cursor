#!/usr/bin/env python
"""
Script pour créer les permissions basées sur les pages réellement utilisées dans App.tsx
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def create_permissions_for_actual_pages():
    """Créer les permissions basées sur les pages réellement définies dans App.tsx"""
    print("🚀 CRÉATION PERMISSIONS BASÉES SUR LES PAGES RÉELLES")
    print("=" * 60)
    
    # Pages réellement définies dans App.tsx avec leurs permissions
    actual_pages_permissions = {
        "dashboard": [
            ("dashboard.view", "Voir le tableau de bord", "Accéder à la page d'accueil et vue d'ensemble"),
        ],
        
        "users": [
            ("users.view", "Voir les utilisateurs", "Consulter la liste des utilisateurs"),
            ("users.create", "Créer des utilisateurs", "Ajouter de nouveaux utilisateurs"),
            ("users.update", "Modifier les utilisateurs", "Modifier les informations utilisateur"),
            ("users.delete", "Supprimer les utilisateurs", "Supprimer des comptes utilisateur"),
            ("users.assign_permissions", "Attribuer permissions", "Gérer les permissions utilisateur"),
            ("users.reset_password", "Réinitialiser mot de passe", "Réinitialiser les mots de passe"),
        ],
        
        "profile": [
            ("profile.view", "Voir profil", "Consulter son profil personnel"),
            ("profile.update", "Modifier profil", "Modifier ses informations personnelles"),
        ],
        
        "products": [
            ("products.view", "Voir les produits", "Consulter le catalogue produits"),
            ("products.create", "Créer produits", "Ajouter de nouveaux produits"),
            ("products.update", "Modifier produits", "Modifier les produits existants"),
            ("products.delete", "Supprimer produits", "Retirer des produits du catalogue"),
            ("products.pricing", "Gérer prix", "Modifier les prix et tarifications"),
        ],
        
        "sales": [
            ("sales.view", "Voir les ventes", "Consulter les ventes et transactions"),
            ("sales.create", "Créer des ventes", "Effectuer des ventes"),
            ("sales.update", "Modifier les ventes", "Modifier des ventes existantes"),
            ("sales.delete", "Supprimer les ventes", "Annuler/supprimer des ventes"),
            ("sales.refund", "Rembourser", "Effectuer des remboursements"),
        ],
        
        "stocks": [
            ("stocks.view", "Voir les stocks", "Consulter l'état des stocks"),
            ("stocks.update", "Modifier stocks", "Ajuster les quantités en stock"),
            ("stocks.adjust", "Ajuster stocks", "Corriger les niveaux de stock"),
            ("stocks.alerts", "Alertes stock", "Gérer les alertes de stock bas"),
        ],
        
        "supplies": [
            ("supplies.view", "Voir fournitures", "Consulter les fournitures"),
            ("supplies.create", "Ajouter fournitures", "Ajouter de nouvelles fournitures"),
            ("supplies.update", "Modifier fournitures", "Modifier les fournitures"),
            ("supplies.order", "Commander", "Passer des commandes fournisseurs"),
        ],
        
        "suppliers": [
            ("suppliers.view", "Voir fournisseurs", "Consulter les fournisseurs"),
            ("suppliers.create", "Créer fournisseurs", "Ajouter de nouveaux fournisseurs"),
            ("suppliers.update", "Modifier fournisseurs", "Modifier les fournisseurs"),
            ("suppliers.manage", "Gérer relations", "Gérer les relations fournisseurs"),
        ],
        
        "kitchen": [
            ("kitchen.view", "Voir cuisine", "Accéder à l'interface cuisine"),
            ("kitchen.orders", "Gérer commandes", "Traiter les commandes cuisine"),
            ("kitchen.prep", "Gestion préparation", "Organiser la préparation"),
        ],
        
        "tables": [
            ("tables.view", "Voir les tables", "Consulter l'état des tables"),
            ("tables.manage", "Gérer tables", "Ouvrir/fermer des tables"),
            ("tables.reservations", "Réservations", "Gérer les réservations"),
        ],
        
        "orders": [
            ("orders.view", "Voir les commandes", "Consulter les commandes"),
            ("orders.create", "Créer commandes", "Passer de nouvelles commandes"),
            ("orders.update", "Modifier commandes", "Modifier des commandes existantes"),
            ("orders.fulfill", "Traiter commandes", "Marquer comme traitées"),
        ],
        
        "finances": [
            ("finances.view", "Voir les finances", "Consulter les données financières"),
            ("finances.history", "Historique des ventes", "Consulter l'historique des transactions"),
            ("finances.reports", "Rapports financiers", "Générer des rapports financiers"),
            ("finances.expenses", "Gérer dépenses", "Gérer les dépenses et frais"),
            ("finances.daily_report", "Rapport quotidien", "Consulter le rapport quotidien"),
        ],
        
        "reports": [
            ("reports.view", "Voir rapports", "Consulter les rapports"),
            ("reports.create", "Créer rapports", "Générer de nouveaux rapports"),
            ("reports.export", "Exporter rapports", "Exporter les rapports"),
            ("reports.daily", "Rapport quotidien", "Générer le rapport quotidien"),
        ],
        
        "analytics": [
            ("analytics.view", "Voir analyses", "Consulter les analyses"),
            ("analytics.sales", "Analyses ventes", "Analyser les performances de vente"),
            ("analytics.financial", "Analyses financières", "Analyser la santé financière"),
        ],
        
        "settings": [
            ("settings.view", "Voir paramètres", "Consulter la configuration"),
            ("settings.update", "Modifier paramètres", "Modifier la configuration système"),
            ("settings.security", "Sécurité", "Gérer les paramètres de sécurité"),
        ],
        
        "alerts": [
            ("alerts.view", "Voir alertes", "Consulter les alertes"),
            ("alerts.create", "Créer alertes", "Configurer de nouvelles alertes"),
            ("alerts.acknowledge", "Acquitter", "Marquer les alertes comme vues"),
        ],
        
        "monitoring": [
            ("monitoring.view", "Voir monitoring", "Consulter les métriques système"),
            ("monitoring.logs", "Voir logs", "Accéder aux journaux système"),
            ("monitoring.alerts", "Alertes système", "Configurer les alertes"),
        ],
        
        "help": [
            ("help.view", "Voir aide", "Accéder à la documentation"),
            ("help.support", "Support", "Contacter le support technique"),
        ]
    }
    
    # Statistiques
    total_permissions = sum(len(perms) for perms in actual_pages_permissions.values())
    print(f"📊 CRÉATION DE {total_permissions} PERMISSIONS POUR {len(actual_pages_permissions)} PAGES RÉELLES")
    
    # Supprimer toutes les permissions existantes
    print(f"\n🗑️  NETTOYAGE DES PERMISSIONS EXISTANTES...")
    deleted_count = Permission.objects.all().delete()[0]
    print(f"   ✅ {deleted_count} permissions supprimées")
    
    # Créer les nouvelles permissions
    print(f"\n➕ CRÉATION DES PERMISSIONS POUR LES PAGES RÉELLES...")
    created_count = 0
    
    for category, permissions in actual_pages_permissions.items():
        print(f"\n🔹 {category.upper()} ({len(permissions)} permissions)")
        
        for code, name, description in permissions:
            try:
                Permission.objects.create(
                    code=code,
                    name=name,
                    description=description,
                    category=category,
                    is_active=True
                )
                print(f"   ✅ {code} - {name}")
                created_count += 1
            except Exception as e:
                print(f"   ❌ Erreur {code}: {str(e)}")
    
    print(f"\n📈 RÉSUMÉ CRÉATION:")
    print(f"   • Permissions créées: {created_count}")
    print(f"   • Pages couvertes: {len(actual_pages_permissions)}")
    
    return created_count == total_permissions

def verify_permissions_match_routes():
    """Vérifier que les permissions correspondent aux routes définies"""
    print(f"\n✅ VÉRIFICATION CORRESPONDANCE ROUTES → PERMISSIONS")
    print("=" * 60)
    
    # Routes définies dans App.tsx
    actual_routes = [
        "/", "/dashboard",  # Index/Dashboard
        "/profile",         # Profile
        "/products",        # Products
        "/sales",           # Sales
        "/stocks",          # Stocks
        "/stock-sync",      # StockSync (stocks)
        "/supplies",        # Supplies
        "/kitchen",         # Kitchen
        "/sales-history",   # SalesHistory (finances)
        "/daily-report",    # DailyReport (finances)
        "/reports",         # Reports
        "/analytics",       # Analytics
        "/tables",          # Tables
        "/orders",          # Orders
        "/users",           # Users
        "/suppliers",       # Suppliers
        "/expenses",        # Expenses (finances)
        "/settings",        # Settings
        "/alerts",          # Alerts
        "/monitoring",      # Monitoring
        "/help"             # Help
    ]
    
    # Permissions créées par catégorie
    permission_categories = Permission.objects.values_list('category', flat=True).distinct()
    
    print(f"📊 CORRESPONDANCE:")
    print(f"   • Routes définies: {len(actual_routes)}")
    print(f"   • Catégories permissions: {len(permission_categories)}")
    
    print(f"\n📋 ROUTES ET LEURS PERMISSIONS:")
    route_permission_mapping = {
        "/": "dashboard",
        "/dashboard": "dashboard",
        "/profile": "profile",
        "/products": "products",
        "/sales": "sales",
        "/stocks": "stocks",
        "/stock-sync": "stocks",
        "/supplies": "supplies",
        "/kitchen": "kitchen",
        "/sales-history": "finances",
        "/daily-report": "finances",
        "/reports": "reports",
        "/analytics": "analytics",
        "/tables": "tables",
        "/orders": "orders",
        "/users": "users",
        "/suppliers": "suppliers",
        "/expenses": "finances",
        "/settings": "settings",
        "/alerts": "alerts",
        "/monitoring": "monitoring",
        "/help": "help"
    }
    
    for route, category in route_permission_mapping.items():
        perms_count = Permission.objects.filter(category=category).count()
        print(f"   🔗 {route} → {category} ({perms_count} permissions)")
    
    return True

def test_api_with_actual_permissions():
    """Tester l'API avec les permissions réelles"""
    print(f"\n🌐 TEST API AVEC PERMISSIONS RÉELLES")
    print("=" * 60)
    
    import requests
    
    try:
        # Login admin
        login_url = "http://127.0.0.1:8000/api/auth/login/"
        login_data = {"username": "admin", "password": "admin"}
        
        login_response = requests.post(login_url, json=login_data, timeout=10)
        if login_response.status_code != 200:
            print(f"❌ Échec login: {login_response.status_code}")
            return False
        
        token_data = login_response.json()
        token = token_data.get('access_token') or token_data.get('access')
        
        # Test API permissions
        permissions_url = "http://127.0.0.1:8000/accounts/permissions/list/"
        headers = {"Authorization": f"Bearer {token}"}
        
        response = requests.get(permissions_url, headers=headers, timeout=10)
        print(f"📡 Status API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            permissions = data.get('results', data) if isinstance(data, dict) else data
            
            # Grouper par catégorie
            api_categories = {}
            for perm in permissions:
                cat = perm.get('category', 'Autre')
                if cat not in api_categories:
                    api_categories[cat] = []
                api_categories[cat].append(perm)
            
            print(f"📊 RÉPONSE API:")
            print(f"   • Permissions: {len(permissions)}")
            print(f"   • Catégories: {len(api_categories)}")
            
            print(f"\n📁 CATÉGORIES DISPONIBLES POUR LE FRONTEND:")
            for cat, perms in sorted(api_categories.items()):
                print(f"   🔹 {cat.upper()}: {len(perms)} permissions")
                # Montrer quelques permissions
                for perm in perms[:2]:
                    print(f"      • {perm.get('name')}")
                if len(perms) > 2:
                    print(f"      ... et {len(perms) - 2} autres")
            
            return len(api_categories) >= 15
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 CRÉATION PERMISSIONS BASÉES SUR LES PAGES RÉELLES")
    print("Analyse de App.tsx pour créer uniquement les permissions nécessaires")
    print()
    
    # 1. Créer les permissions pour les pages réelles
    success = create_permissions_for_actual_pages()
    
    if success:
        # 2. Vérifier la correspondance routes → permissions
        mapping_ok = verify_permissions_match_routes()
        
        # 3. Tester l'API
        api_ok = test_api_with_actual_permissions()
        
        # 4. Résumé final
        print(f"\n" + "=" * 60)
        print(f"📋 RÉSUMÉ FINAL:")
        print(f"   • Création permissions: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
        print(f"   • Mapping routes: {'✅ OK' if mapping_ok else '❌ PROBLÈME'}")
        print(f"   • API fonctionnelle: {'✅ OK' if api_ok else '❌ PROBLÈME'}")
        
        if success and mapping_ok and api_ok:
            print(f"\n🎉 PERMISSIONS OPTIMISÉES CRÉÉES!")
            print(f"✅ Basées sur les {len(Permission.objects.values('category').distinct())} pages réelles de App.tsx")
            print(f"✅ {Permission.objects.count()} permissions au total")
            print(f"✅ Système allégé et optimisé pour votre application")
            print(f"\n💡 PROCHAINE ÉTAPE:")
            print(f"   Actualisez le frontend pour voir les permissions organisées")
        else:
            print(f"\n❌ PROBLÈMES DÉTECTÉS - Vérifiez les logs ci-dessus")
    else:
        print(f"\n❌ ÉCHEC DE LA CRÉATION DES PERMISSIONS")

if __name__ == '__main__':
    main()
