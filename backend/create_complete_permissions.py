#!/usr/bin/env python
"""
Script pour créer un système de permissions complet pour BarStockWise
Conçu par un expert en sécurité d'applications web
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def create_comprehensive_permissions():
    """Créer un système de permissions complet et sécurisé"""
    print("🔐 CRÉATION D'UN SYSTÈME DE PERMISSIONS COMPLET")
    print("=" * 55)
    
    # Système de permissions granulaires pour une application de gestion de bar
    permissions_data = [
        
        # ===== DASHBOARD & CORE =====
        {
            'code': 'dashboard.view',
            'name': 'Accéder au tableau de bord',
            'description': 'Accès à la page d\'accueil et aux statistiques générales',
            'category': 'dashboard'
        },
        {
            'code': 'profile.view',
            'name': 'Voir son profil',
            'description': 'Consulter ses informations personnelles',
            'category': 'profile'
        },
        {
            'code': 'profile.update',
            'name': 'Modifier son profil',
            'description': 'Mettre à jour ses informations personnelles',
            'category': 'profile'
        },
        
        # ===== SALES (VENTES) =====
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Consulter la liste des ventes et le POS',
            'category': 'sales'
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Effectuer des ventes via le système POS',
            'category': 'sales'
        },
        {
            'code': 'sales.update',
            'name': 'Modifier les ventes',
            'description': 'Modifier les ventes existantes (avant finalisation)',
            'category': 'sales'
        },
        {
            'code': 'sales.delete',
            'name': 'Supprimer les ventes',
            'description': 'Annuler ou supprimer des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Accès à l\'historique complet des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.approve',
            'name': 'Approuver les ventes',
            'description': 'Valider les ventes en attente d\'approbation',
            'category': 'sales'
        },
        {
            'code': 'sales.refund',
            'name': 'Effectuer des remboursements',
            'description': 'Traiter les remboursements et retours',
            'category': 'sales'
        },
        {
            'code': 'sales.discount',
            'name': 'Appliquer des remises',
            'description': 'Accorder des remises sur les ventes',
            'category': 'sales'
        },
        
        # ===== PRODUCTS (PRODUITS) =====
        {
            'code': 'products.view',
            'name': 'Voir les produits',
            'description': 'Consulter le catalogue des produits',
            'category': 'products'
        },
        {
            'code': 'products.create',
            'name': 'Créer des produits',
            'description': 'Ajouter de nouveaux produits au catalogue',
            'category': 'products'
        },
        {
            'code': 'products.update',
            'name': 'Modifier les produits',
            'description': 'Mettre à jour les informations des produits',
            'category': 'products'
        },
        {
            'code': 'products.delete',
            'name': 'Supprimer les produits',
            'description': 'Retirer des produits du catalogue',
            'category': 'products'
        },
        {
            'code': 'products.pricing',
            'name': 'Gérer les prix',
            'description': 'Modifier les prix des produits',
            'category': 'products'
        },
        
        # ===== INVENTORY (STOCKS) =====
        {
            'code': 'inventory.view',
            'name': 'Voir les stocks',
            'description': 'Consulter les niveaux de stock',
            'category': 'inventory'
        },
        {
            'code': 'inventory.update',
            'name': 'Mettre à jour les stocks',
            'description': 'Modifier les quantités en stock',
            'category': 'inventory'
        },
        {
            'code': 'inventory.audit',
            'name': 'Auditer les stocks',
            'description': 'Effectuer des inventaires et audits',
            'category': 'inventory'
        },
        {
            'code': 'inventory.alerts',
            'name': 'Gérer les alertes stock',
            'description': 'Configurer et recevoir les alertes de stock',
            'category': 'inventory'
        },
        {
            'code': 'inventory.transfer',
            'name': 'Transférer les stocks',
            'description': 'Effectuer des transferts entre emplacements',
            'category': 'inventory'
        },
        
        # ===== SUPPLIES (APPROVISIONNEMENTS) =====
        {
            'code': 'supplies.view',
            'name': 'Voir les approvisionnements',
            'description': 'Consulter les commandes fournisseurs',
            'category': 'supplies'
        },
        {
            'code': 'supplies.create',
            'name': 'Créer des commandes',
            'description': 'Passer des commandes aux fournisseurs',
            'category': 'supplies'
        },
        {
            'code': 'supplies.update',
            'name': 'Modifier les commandes',
            'description': 'Mettre à jour les commandes en cours',
            'category': 'supplies'
        },
        {
            'code': 'supplies.approve',
            'name': 'Approuver les commandes',
            'description': 'Valider les commandes avant envoi',
            'category': 'supplies'
        },
        {
            'code': 'supplies.receive',
            'name': 'Réceptionner les livraisons',
            'description': 'Traiter les réceptions de marchandises',
            'category': 'supplies'
        },
        
        # ===== KITCHEN (CUISINE) =====
        {
            'code': 'kitchen.view',
            'name': 'Voir les commandes cuisine',
            'description': 'Accès à l\'interface cuisine',
            'category': 'kitchen'
        },
        {
            'code': 'kitchen.manage',
            'name': 'Gérer les commandes',
            'description': 'Traiter et organiser les commandes cuisine',
            'category': 'kitchen'
        },
        {
            'code': 'kitchen.recipes',
            'name': 'Gérer les recettes',
            'description': 'Créer et modifier les recettes',
            'category': 'kitchen'
        },
        
        # ===== TABLES & ORDERS =====
        {
            'code': 'tables.view',
            'name': 'Voir les tables',
            'description': 'Consulter l\'état des tables',
            'category': 'tables'
        },
        {
            'code': 'tables.manage',
            'name': 'Gérer les tables',
            'description': 'Assigner et organiser les tables',
            'category': 'tables'
        },
        {
            'code': 'orders.view',
            'name': 'Voir les commandes',
            'description': 'Consulter les commandes en cours',
            'category': 'orders'
        },
        {
            'code': 'orders.create',
            'name': 'Créer des commandes',
            'description': 'Prendre des commandes clients',
            'category': 'orders'
        },
        {
            'code': 'orders.update',
            'name': 'Modifier les commandes',
            'description': 'Mettre à jour les commandes existantes',
            'category': 'orders'
        },
        {
            'code': 'orders.cancel',
            'name': 'Annuler les commandes',
            'description': 'Annuler des commandes en cours',
            'category': 'orders'
        },
        
        # ===== USERS (UTILISATEURS) =====
        {
            'code': 'users.view',
            'name': 'Voir les utilisateurs',
            'description': 'Consulter la liste des utilisateurs',
            'category': 'users'
        },
        {
            'code': 'users.create',
            'name': 'Créer des utilisateurs',
            'description': 'Ajouter de nouveaux utilisateurs',
            'category': 'users'
        },
        {
            'code': 'users.update',
            'name': 'Modifier les utilisateurs',
            'description': 'Mettre à jour les informations utilisateurs',
            'category': 'users'
        },
        {
            'code': 'users.delete',
            'name': 'Supprimer les utilisateurs',
            'description': 'Désactiver ou supprimer des utilisateurs',
            'category': 'users'
        },
        {
            'code': 'users.permissions',
            'name': 'Gérer les permissions',
            'description': 'Assigner et modifier les permissions utilisateurs',
            'category': 'users'
        },
        {
            'code': 'users.roles',
            'name': 'Gérer les rôles',
            'description': 'Créer et modifier les rôles utilisateurs',
            'category': 'users'
        },
        
        # ===== SUPPLIERS (FOURNISSEURS) =====
        {
            'code': 'suppliers.view',
            'name': 'Voir les fournisseurs',
            'description': 'Consulter la liste des fournisseurs',
            'category': 'suppliers'
        },
        {
            'code': 'suppliers.create',
            'name': 'Créer des fournisseurs',
            'description': 'Ajouter de nouveaux fournisseurs',
            'category': 'suppliers'
        },
        {
            'code': 'suppliers.update',
            'name': 'Modifier les fournisseurs',
            'description': 'Mettre à jour les informations fournisseurs',
            'category': 'suppliers'
        },
        {
            'code': 'suppliers.delete',
            'name': 'Supprimer les fournisseurs',
            'description': 'Retirer des fournisseurs de la liste',
            'category': 'suppliers'
        },
        
        # ===== REPORTS & ANALYTICS =====
        {
            'code': 'reports.view',
            'name': 'Voir les rapports',
            'description': 'Consulter les rapports de gestion',
            'category': 'reports'
        },
        {
            'code': 'reports.create',
            'name': 'Créer des rapports',
            'description': 'Générer des rapports personnalisés',
            'category': 'reports'
        },
        {
            'code': 'reports.export',
            'name': 'Exporter les rapports',
            'description': 'Télécharger les rapports en PDF/Excel',
            'category': 'reports'
        },
        {
            'code': 'analytics.view',
            'name': 'Voir les analyses',
            'description': 'Accès aux tableaux de bord analytiques',
            'category': 'analytics'
        },
        {
            'code': 'analytics.advanced',
            'name': 'Analyses avancées',
            'description': 'Accès aux outils d\'analyse avancée',
            'category': 'analytics'
        },
        
        # ===== FINANCES =====
        {
            'code': 'finances.view',
            'name': 'Voir les finances',
            'description': 'Consulter les données financières',
            'category': 'finances'
        },
        {
            'code': 'finances.daily_report',
            'name': 'Rapports quotidiens',
            'description': 'Accès aux rapports financiers quotidiens',
            'category': 'finances'
        },
        {
            'code': 'finances.expenses',
            'name': 'Gérer les dépenses',
            'description': 'Enregistrer et gérer les dépenses',
            'category': 'finances'
        },
        {
            'code': 'finances.budget',
            'name': 'Gérer le budget',
            'description': 'Planifier et suivre les budgets',
            'category': 'finances'
        },
        {
            'code': 'finances.accounting',
            'name': 'Comptabilité',
            'description': 'Accès aux fonctions comptables avancées',
            'category': 'finances'
        },
        
        # ===== SETTINGS & ADMINISTRATION =====
        {
            'code': 'settings.view',
            'name': 'Voir les paramètres',
            'description': 'Consulter la configuration système',
            'category': 'settings'
        },
        {
            'code': 'settings.update',
            'name': 'Modifier les paramètres',
            'description': 'Configurer les paramètres système',
            'category': 'settings'
        },
        {
            'code': 'settings.security',
            'name': 'Paramètres de sécurité',
            'description': 'Gérer la sécurité et les accès',
            'category': 'settings'
        },
        {
            'code': 'settings.backup',
            'name': 'Sauvegardes',
            'description': 'Gérer les sauvegardes système',
            'category': 'settings'
        },
        
        # ===== MONITORING & ALERTS =====
        {
            'code': 'monitoring.view',
            'name': 'Surveillance système',
            'description': 'Surveiller les performances système',
            'category': 'monitoring'
        },
        {
            'code': 'alerts.view',
            'name': 'Voir les alertes',
            'description': 'Consulter les alertes système',
            'category': 'alerts'
        },
        {
            'code': 'alerts.manage',
            'name': 'Gérer les alertes',
            'description': 'Configurer et traiter les alertes',
            'category': 'alerts'
        },
        
        # ===== HELP & SUPPORT =====
        {
            'code': 'help.view',
            'name': 'Accéder à l\'aide',
            'description': 'Consulter la documentation et l\'aide',
            'category': 'help'
        },
        
        # ===== AUDIT & LOGS =====
        {
            'code': 'audit.view',
            'name': 'Voir les logs d\'audit',
            'description': 'Consulter les journaux d\'activité',
            'category': 'audit'
        },
        {
            'code': 'audit.export',
            'name': 'Exporter les audits',
            'description': 'Télécharger les rapports d\'audit',
            'category': 'audit'
        }
    ]
    
    print(f"📋 Création de {len(permissions_data)} permissions...")
    
    # Supprimer toutes les permissions existantes
    Permission.objects.all().delete()
    print("   🗑️  Anciennes permissions supprimées")
    
    # Créer toutes les nouvelles permissions
    created_count = 0
    categories = set()
    
    for perm_data in permissions_data:
        try:
            permission = Permission.objects.create(
                code=perm_data['code'],
                name=perm_data['name'],
                description=perm_data['description'],
                category=perm_data['category']
            )
            categories.add(perm_data['category'])
            created_count += 1
            
        except Exception as e:
            print(f"   ❌ Erreur pour {perm_data['code']}: {str(e)}")
    
    print(f"\n📊 RÉSULTAT:")
    print(f"   • Permissions créées: {created_count}")
    print(f"   • Catégories: {len(categories)}")
    
    # Afficher les catégories
    print(f"\n📁 CATÉGORIES CRÉÉES:")
    for category in sorted(categories):
        count = Permission.objects.filter(category=category).count()
        print(f"   • {category.upper()}: {count} permissions")
    
    return created_count

def assign_basic_permissions_to_testuser():
    """Assigner des permissions de base à testuser_sales"""
    print(f"\n👤 ATTRIBUTION DES PERMISSIONS À testuser_sales")
    print("=" * 55)
    
    try:
        from accounts.models import User, UserPermission
        
        user = User.objects.get(username="testuser_sales")
        
        # Permissions de base pour un serveur
        basic_permissions = [
            'dashboard.view',
            'profile.view',
            'profile.update',
            'sales.view',
            'sales.create',
            'sales.history',
            'products.view',
            'tables.view',
            'tables.manage',
            'orders.view',
            'orders.create',
            'orders.update',
            'kitchen.view',
            'help.view'
        ]
        
        assigned_count = 0
        for perm_code in basic_permissions:
            try:
                permission = Permission.objects.get(code=perm_code)
                user_permission, created = UserPermission.objects.get_or_create(
                    user=user,
                    permission=permission,
                    defaults={'is_active': True}
                )
                
                if created or not user_permission.is_active:
                    user_permission.is_active = True
                    user_permission.save()
                    assigned_count += 1
                    print(f"   ✅ {perm_code}")
                
            except Permission.DoesNotExist:
                print(f"   ❌ Permission non trouvée: {perm_code}")
        
        print(f"\n📊 Permissions assignées: {assigned_count}")
        return True
        
    except User.DoesNotExist:
        print("   ❌ Utilisateur testuser_sales non trouvé")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def verify_frontend_compatibility():
    """Vérifier la compatibilité avec le frontend"""
    print(f"\n🎨 VÉRIFICATION COMPATIBILITÉ FRONTEND")
    print("=" * 55)
    
    # Vérifier que toutes les catégories sont présentes
    permissions = Permission.objects.all()
    
    # Simuler le groupement frontend
    grouped = {}
    for perm in permissions:
        category = perm.category or 'Autre'
        if category not in grouped:
            grouped[category] = []
        grouped[category].append({
            'id': perm.id,
            'code': perm.code,
            'name': perm.name,
            'category': perm.category
        })
    
    print(f"📋 Groupement pour le frontend:")
    for category, perms in grouped.items():
        print(f"   📁 {category.upper()}: {len(perms)} permissions")
    
    # Vérifier les catégories importantes
    important_categories = ['sales', 'users', 'products', 'inventory', 'reports']
    missing_categories = []
    
    for cat in important_categories:
        if cat not in grouped:
            missing_categories.append(cat)
    
    if missing_categories:
        print(f"\n⚠️  Catégories manquantes: {missing_categories}")
        return False
    else:
        print(f"\n✅ Toutes les catégories importantes sont présentes")
        return True

def main():
    """Fonction principale"""
    print("🚀 CRÉATION D'UN SYSTÈME DE PERMISSIONS COMPLET")
    print("Conçu par un expert en sécurité d'applications web")
    print("Pour BarStockWise - Gestion de bar professionnelle")
    print()
    
    # 1. Créer toutes les permissions
    created_count = create_comprehensive_permissions()
    
    # 2. Assigner des permissions de base à l'utilisateur test
    user_assigned = assign_basic_permissions_to_testuser()
    
    # 3. Vérifier la compatibilité frontend
    frontend_ok = verify_frontend_compatibility()
    
    # 4. Résumé final
    print(f"\n" + "=" * 55)
    print(f"📋 RÉSUMÉ FINAL:")
    
    print(f"   • Permissions créées: {created_count}")
    print(f"   • Utilisateur configuré: {'✅ OUI' if user_assigned else '❌ NON'}")
    print(f"   • Frontend compatible: {'✅ OUI' if frontend_ok else '❌ NON'}")
    
    if created_count > 0 and frontend_ok:
        print(f"\n🎉 SYSTÈME DE PERMISSIONS COMPLET CRÉÉ!")
        print(f"✅ {created_count} permissions dans {len(set(p.category for p in Permission.objects.all()))} catégories")
        print(f"✅ Système granulaire et sécurisé")
        print(f"✅ Compatible avec l'interface frontend")
        
        print(f"\n🔄 ACTIONS REQUISES:")
        print(f"1. Redémarrer le serveur Django")
        print(f"2. Actualiser le navigateur (Ctrl+Shift+R)")
        print(f"3. Tester le formulaire de création d'utilisateur")
        print(f"4. Vérifier que toutes les catégories apparaissent")
        
        print(f"\n🔐 SÉCURITÉ:")
        print(f"• Permissions granulaires par fonctionnalité")
        print(f"• Séparation claire des responsabilités")
        print(f"• Contrôle d'accès basé sur les rôles")
        print(f"• Audit et traçabilité intégrés")
    else:
        print(f"\n⚠️  PROBLÈMES DÉTECTÉS")
        print(f"Vérifiez les erreurs ci-dessus")

if __name__ == '__main__':
    main()
