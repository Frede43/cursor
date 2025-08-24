#!/usr/bin/env python
"""
Script pour créer un système complet de permissions pour le dialog de création d'utilisateur
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def create_complete_permission_system():
    """Créer toutes les permissions recommandées organisées par catégories"""
    print("🚀 CRÉATION DU SYSTÈME COMPLET DE PERMISSIONS")
    print("=" * 60)
    
    # Définition complète des permissions par catégorie
    permissions_data = {
        "dashboard": [
            ("dashboard.view", "Voir le tableau de bord", "Accéder à la page d'accueil et vue d'ensemble"),
        ],
        
        "users": [
            ("users.view", "Voir les utilisateurs", "Consulter la liste des utilisateurs"),
            ("users.create", "Créer des utilisateurs", "Ajouter de nouveaux utilisateurs"),
            ("users.update", "Modifier les utilisateurs", "Modifier les informations utilisateur"),
            ("users.delete", "Supprimer les utilisateurs", "Supprimer des comptes utilisateur"),
            ("users.activate", "Activer/Désactiver", "Gérer le statut actif des utilisateurs"),
            ("users.reset_password", "Réinitialiser mot de passe", "Réinitialiser les mots de passe"),
            ("users.assign_permissions", "Attribuer permissions", "Gérer les permissions utilisateur"),
            ("users.view_activities", "Voir activités", "Consulter l'historique des activités"),
        ],
        
        "sales": [
            ("sales.view", "Voir les ventes", "Consulter les ventes et transactions"),
            ("sales.create", "Créer des ventes", "Effectuer des ventes"),
            ("sales.update", "Modifier les ventes", "Modifier des ventes existantes"),
            ("sales.delete", "Supprimer les ventes", "Annuler/supprimer des ventes"),
            ("sales.approve", "Approuver les ventes", "Valider des ventes importantes"),
            ("sales.refund", "Rembourser", "Effectuer des remboursements"),
            ("sales.discount", "Appliquer remises", "Gérer les remises et promotions"),
        ],
        
        "finances": [
            ("finances.view", "Voir les finances", "Consulter les données financières"),
            ("finances.reports", "Rapports financiers", "Générer des rapports financiers"),
            ("finances.export", "Exporter données", "Exporter les données financières"),
            ("finances.history", "Historique des ventes", "Consulter l'historique des transactions"),
            ("finances.analytics", "Analyses financières", "Accéder aux analyses avancées"),
            ("finances.budgets", "Gérer budgets", "Configurer et suivre les budgets"),
            ("finances.expenses", "Gérer dépenses", "Gérer les dépenses et frais"),
            ("finances.taxes", "Gestion fiscale", "Gérer les taxes et déclarations"),
        ],
        
        "products": [
            ("products.view", "Voir les produits", "Consulter le catalogue produits"),
            ("products.create", "Créer produits", "Ajouter de nouveaux produits"),
            ("products.update", "Modifier produits", "Modifier les produits existants"),
            ("products.delete", "Supprimer produits", "Retirer des produits du catalogue"),
            ("products.categories", "Gérer catégories", "Organiser les catégories de produits"),
            ("products.pricing", "Gérer prix", "Modifier les prix et tarifications"),
            ("products.import", "Importer produits", "Importer des produits en masse"),
            ("products.export", "Exporter produits", "Exporter le catalogue"),
            ("products.audit", "Audit produits", "Auditer les produits et leur historique"),
        ],
        
        "inventory": [
            ("inventory.view", "Voir l'inventaire", "Consulter les stocks"),
            ("inventory.create", "Ajouter au stock", "Ajouter de nouveaux éléments au stock"),
            ("inventory.update", "Modifier stock", "Modifier les informations de stock"),
            ("inventory.delete", "Supprimer du stock", "Retirer des éléments du stock"),
            ("inventory.adjust", "Ajuster stocks", "Corriger les quantités en stock"),
            ("inventory.transfer", "Transférer stocks", "Déplacer des stocks entre emplacements"),
            ("inventory.alerts", "Alertes stock", "Gérer les alertes de stock bas"),
            ("inventory.audit", "Audit inventaire", "Effectuer des audits d'inventaire"),
            ("inventory.sync", "Synchroniser stocks", "Synchroniser les données de stock"),
        ],
        
        "orders": [
            ("orders.view", "Voir les commandes", "Consulter les commandes"),
            ("orders.create", "Créer commandes", "Passer de nouvelles commandes"),
            ("orders.update", "Modifier commandes", "Modifier des commandes existantes"),
            ("orders.delete", "Supprimer commandes", "Annuler des commandes"),
            ("orders.approve", "Approuver commandes", "Valider des commandes importantes"),
            ("orders.fulfill", "Traiter commandes", "Marquer comme traitées"),
            ("orders.track", "Suivre commandes", "Suivre le statut des commandes"),
        ],
        
        "kitchen": [
            ("kitchen.view", "Voir cuisine", "Accéder à l'interface cuisine"),
            ("kitchen.orders", "Gérer commandes", "Traiter les commandes cuisine"),
            ("kitchen.recipes", "Gérer recettes", "Modifier les recettes et compositions"),
            ("kitchen.prep", "Gestion préparation", "Organiser la préparation"),
            ("kitchen.inventory", "Stock cuisine", "Gérer les stocks cuisine"),
            ("kitchen.equipment", "Équipements", "Gérer les équipements cuisine"),
        ],
        
        "tables": [
            ("tables.view", "Voir les tables", "Consulter l'état des tables"),
            ("tables.manage", "Gérer tables", "Ouvrir/fermer des tables"),
            ("tables.assign", "Attribuer tables", "Assigner des serveurs aux tables"),
            ("tables.reservations", "Réservations", "Gérer les réservations"),
            ("tables.layout", "Configuration", "Modifier la disposition des tables"),
        ],
        
        "supplies": [
            ("supplies.view", "Voir fournitures", "Consulter les fournitures"),
            ("supplies.create", "Ajouter fournitures", "Ajouter de nouvelles fournitures"),
            ("supplies.update", "Modifier fournitures", "Modifier les fournitures"),
            ("supplies.delete", "Supprimer fournitures", "Retirer des fournitures"),
            ("supplies.order", "Commander", "Passer des commandes fournisseurs"),
            ("supplies.receive", "Réceptionner", "Réceptionner les livraisons"),
            ("supplies.audit", "Audit fournitures", "Auditer les fournitures"),
        ],
        
        "suppliers": [
            ("suppliers.view", "Voir fournisseurs", "Consulter les fournisseurs"),
            ("suppliers.create", "Créer fournisseurs", "Ajouter de nouveaux fournisseurs"),
            ("suppliers.update", "Modifier fournisseurs", "Modifier les fournisseurs"),
            ("suppliers.delete", "Supprimer fournisseurs", "Retirer des fournisseurs"),
            ("suppliers.manage", "Gérer relations", "Gérer les relations fournisseurs"),
        ],
        
        "reports": [
            ("reports.view", "Voir rapports", "Consulter les rapports"),
            ("reports.create", "Créer rapports", "Générer de nouveaux rapports"),
            ("reports.export", "Exporter rapports", "Exporter les rapports"),
            ("reports.schedule", "Programmer rapports", "Automatiser la génération"),
            ("reports.analytics", "Analyses avancées", "Accéder aux analyses détaillées"),
            ("reports.dashboard", "Tableaux de bord", "Configurer les dashboards"),
            ("reports.daily", "Rapport quotidien", "Générer le rapport quotidien"),
        ],
        
        "analytics": [
            ("analytics.view", "Voir analyses", "Consulter les analyses"),
            ("analytics.sales", "Analyses ventes", "Analyser les performances de vente"),
            ("analytics.customers", "Analyses clients", "Analyser le comportement client"),
            ("analytics.products", "Analyses produits", "Analyser les performances produits"),
            ("analytics.financial", "Analyses financières", "Analyser la santé financière"),
            ("analytics.predictive", "Analyses prédictives", "Accéder aux prédictions"),
        ],
        
        "settings": [
            ("settings.view", "Voir paramètres", "Consulter la configuration"),
            ("settings.update", "Modifier paramètres", "Modifier la configuration système"),
            ("settings.backup", "Sauvegardes", "Gérer les sauvegardes"),
            ("settings.restore", "Restaurations", "Restaurer des sauvegardes"),
            ("settings.integrations", "Intégrations", "Configurer les intégrations externes"),
            ("settings.notifications", "Notifications", "Configurer les notifications"),
            ("settings.security", "Sécurité", "Gérer les paramètres de sécurité"),
        ],
        
        "monitoring": [
            ("monitoring.view", "Voir monitoring", "Consulter les métriques système"),
            ("monitoring.logs", "Voir logs", "Accéder aux journaux système"),
            ("monitoring.performance", "Performance", "Surveiller les performances"),
            ("monitoring.errors", "Gestion erreurs", "Gérer les erreurs système"),
            ("monitoring.alerts", "Alertes système", "Configurer les alertes"),
        ],
        
        "alerts": [
            ("alerts.view", "Voir alertes", "Consulter les alertes"),
            ("alerts.create", "Créer alertes", "Configurer de nouvelles alertes"),
            ("alerts.update", "Modifier alertes", "Modifier les alertes existantes"),
            ("alerts.delete", "Supprimer alertes", "Retirer des alertes"),
            ("alerts.acknowledge", "Acquitter", "Marquer les alertes comme vues"),
            ("alerts.escalate", "Escalader", "Escalader des alertes critiques"),
        ],
        
        "audit": [
            ("audit.view", "Voir audits", "Consulter les journaux d'audit"),
            ("audit.export", "Exporter audits", "Exporter les données d'audit"),
            ("audit.configure", "Configurer audit", "Paramétrer l'audit système"),
            ("audit.compliance", "Conformité", "Gérer la conformité réglementaire"),
        ],
        
        "help": [
            ("help.view", "Voir aide", "Accéder à la documentation"),
            ("help.support", "Support", "Contacter le support technique"),
            ("help.training", "Formation", "Accéder aux ressources de formation"),
        ],
        
        "profile": [
            ("profile.view", "Voir profil", "Consulter son profil personnel"),
            ("profile.update", "Modifier profil", "Modifier ses informations personnelles"),
        ]
    }
    
    # Statistiques
    total_permissions = sum(len(perms) for perms in permissions_data.values())
    print(f"📊 CRÉATION DE {total_permissions} PERMISSIONS DANS {len(permissions_data)} CATÉGORIES")
    
    # Supprimer toutes les permissions existantes pour repartir à zéro
    print(f"\n🗑️  NETTOYAGE DES PERMISSIONS EXISTANTES...")
    deleted_count = Permission.objects.all().delete()[0]
    print(f"   ✅ {deleted_count} permissions supprimées")
    
    # Créer toutes les nouvelles permissions
    print(f"\n➕ CRÉATION DES NOUVELLES PERMISSIONS...")
    created_count = 0
    
    for category, permissions in permissions_data.items():
        print(f"\n🔹 Catégorie: {category.upper()}")
        
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
    print(f"   • Catégories: {len(permissions_data)}")
    
    return created_count == total_permissions

def verify_permissions_in_database():
    """Vérifier que toutes les permissions sont bien créées"""
    print(f"\n✅ VÉRIFICATION EN BASE DE DONNÉES")
    print("=" * 60)
    
    all_permissions = Permission.objects.all().order_by('category', 'code')
    
    # Grouper par catégorie
    categories = {}
    for perm in all_permissions:
        cat = perm.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(perm)
    
    print(f"📊 PERMISSIONS EN BASE:")
    print(f"   • Total: {all_permissions.count()}")
    print(f"   • Catégories: {len(categories)}")
    print(f"   • Actives: {all_permissions.filter(is_active=True).count()}")
    
    print(f"\n📋 DÉTAIL PAR CATÉGORIE:")
    for cat, perms in sorted(categories.items()):
        print(f"   🔹 {cat.upper()}: {len(perms)} permissions")
        for perm in perms[:3]:  # Montrer les 3 premières
            print(f"      • {perm.code} - {perm.name}")
        if len(perms) > 3:
            print(f"      ... et {len(perms) - 3} autres")
    
    return len(categories) > 0

def test_api_response():
    """Tester que l'API retourne toutes les permissions"""
    print(f"\n🌐 TEST API PERMISSIONS")
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
            
            print(f"\n📁 CATÉGORIES DANS L'API:")
            for cat, perms in sorted(api_categories.items()):
                print(f"   🔹 {cat}: {len(perms)} permissions")
            
            return len(api_categories) > 15  # Au moins 15 catégories
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def create_default_user_with_permissions():
    """Créer un utilisateur de test avec quelques permissions"""
    print(f"\n👤 CRÉATION UTILISATEUR DE TEST")
    print("=" * 60)
    
    from django.contrib.auth.hashers import make_password
    from accounts.models import User, UserPermission
    
    # Créer ou récupérer l'utilisateur test
    username = "testuser_complete"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': make_password('temp123456'),
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Utilisateur créé: {username}")
    else:
        print(f"✅ Utilisateur existant: {username}")
    
    # Attribuer quelques permissions de test
    test_permissions = [
        'dashboard.view',
        'users.view',
        'sales.view', 'sales.create',
        'products.view', 'products.create',
        'inventory.view',
        'reports.view',
        'help.view'
    ]
    
    # Supprimer les anciennes permissions
    UserPermission.objects.filter(user=user).delete()
    
    # Ajouter les nouvelles permissions
    assigned_count = 0
    for perm_code in test_permissions:
        try:
            permission = Permission.objects.get(code=perm_code)
            UserPermission.objects.create(user=user, permission=permission)
            assigned_count += 1
        except Permission.DoesNotExist:
            print(f"   ⚠️  Permission non trouvée: {perm_code}")
    
    print(f"   🔑 {assigned_count} permissions attribuées")
    return user

def main():
    """Fonction principale"""
    print("🚀 CRÉATION SYSTÈME COMPLET DE PERMISSIONS")
    print("Pour le dialog de création d'utilisateur BarStockWise")
    print()
    
    # 1. Créer toutes les permissions
    success = create_complete_permission_system()
    
    if success:
        # 2. Vérifier en base
        db_ok = verify_permissions_in_database()
        
        # 3. Tester l'API
        api_ok = test_api_response()
        
        # 4. Créer un utilisateur de test
        test_user = create_default_user_with_permissions()
        
        # 5. Résumé final
        print(f"\n" + "=" * 60)
        print(f"📋 RÉSUMÉ FINAL:")
        print(f"   • Création permissions: {'✅ SUCCÈS' if success else '❌ ÉCHEC'}")
        print(f"   • Base de données: {'✅ OK' if db_ok else '❌ PROBLÈME'}")
        print(f"   • API fonctionnelle: {'✅ OK' if api_ok else '❌ PROBLÈME'}")
        print(f"   • Utilisateur test: {'✅ CRÉÉ' if test_user else '❌ ÉCHEC'}")
        
        if success and db_ok and api_ok:
            print(f"\n🎉 SYSTÈME COMPLET CRÉÉ AVEC SUCCÈS!")
            print(f"✅ Toutes les permissions sont disponibles dans le dialog")
            print(f"✅ Organisées en {len(Permission.objects.values('category').distinct())} catégories")
            print(f"✅ Actualisez le frontend pour voir toutes les permissions")
            print(f"\n💡 UTILISATEUR DE TEST:")
            print(f"   • Username: testuser_complete")
            print(f"   • Password: temp123456")
        else:
            print(f"\n❌ PROBLÈMES DÉTECTÉS - Vérifiez les logs ci-dessus")
    else:
        print(f"\n❌ ÉCHEC DE LA CRÉATION DES PERMISSIONS")

if __name__ == '__main__':
    main()
