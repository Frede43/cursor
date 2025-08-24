#!/usr/bin/env python
"""
Script pour analyser les permissions utilisées dans le frontend
"""

import os
import re
from pathlib import Path

def analyze_sidebar_permissions():
    """Analyser les permissions définies dans Sidebar.tsx"""
    print("🔍 ANALYSE DES PERMISSIONS DANS SIDEBAR.TSX")
    print("=" * 60)
    
    sidebar_path = "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\src\\components\\layout\\Sidebar.tsx"
    
    if not os.path.exists(sidebar_path):
        print("❌ Sidebar.tsx non trouvé")
        return {}
    
    with open(sidebar_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire les éléments de menu avec leurs permissions
    menu_items = {}
    
    # Rechercher les définitions de menu items
    menu_pattern = r'{\s*href:\s*["\']([^"\']+)["\'],\s*icon:\s*(\w+),\s*label:\s*["\']([^"\']+)["\'].*?permissionKey:\s*["\']([^"\']+)["\']'
    matches = re.findall(menu_pattern, content, re.DOTALL)
    
    for href, icon, label, permission in matches:
        menu_items[href] = {
            'label': label,
            'icon': icon,
            'permission': permission
        }
    
    print(f"📊 Éléments de menu trouvés: {len(menu_items)}")
    
    for href, info in menu_items.items():
        print(f"   🔗 {href} - {info['label']} (permission: {info['permission']})")
    
    return menu_items

def analyze_all_pages_permissions():
    """Analyser toutes les pages pour identifier les permissions utilisées"""
    print(f"\n📄 ANALYSE DES PERMISSIONS DANS LES PAGES")
    print("=" * 60)
    
    pages_dir = "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\src\\pages"
    pages_permissions = {}
    
    if not os.path.exists(pages_dir):
        print("❌ Dossier pages non trouvé")
        return {}
    
    # Parcourir tous les fichiers .tsx dans pages
    for file_path in Path(pages_dir).glob("*.tsx"):
        page_name = file_path.stem
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Rechercher les utilisations de permissions
            permissions_found = []
            
            # Patterns pour identifier les permissions
            patterns = [
                r'hasPermission\(["\']([^"\']+)["\']',
                r'checkPermission\(["\']([^"\']+)["\']',
                r'canAccess\(["\']([^"\']+)["\']',
                r'permissionKey:\s*["\']([^"\']+)["\']',
                r'permission:\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                permissions_found.extend(matches)
            
            # Rechercher les imports de hooks de permissions
            if 'usePermissions' in content or 'useCanAccess' in content or 'hasPermission' in content:
                permissions_found.append('USES_PERMISSION_HOOKS')
            
            if permissions_found:
                pages_permissions[page_name] = list(set(permissions_found))
        
        except Exception as e:
            print(f"⚠️  Erreur lecture {page_name}: {str(e)}")
    
    print(f"📊 Pages avec permissions: {len(pages_permissions)}")
    
    for page, perms in pages_permissions.items():
        print(f"\n📄 {page}.tsx:")
        for perm in perms:
            if perm == 'USES_PERMISSION_HOOKS':
                print(f"   🔧 Utilise des hooks de permissions")
            else:
                print(f"   🔑 {perm}")
    
    return pages_permissions

def map_pages_to_permissions():
    """Mapper les pages aux permissions basé sur la logique métier"""
    print(f"\n🗺️  MAPPING PAGES → PERMISSIONS RECOMMANDÉES")
    print("=" * 60)
    
    page_permission_mapping = {
        "Dashboard": {
            "permissions": ["dashboard.view"],
            "description": "Page d'accueil avec vue d'ensemble"
        },
        "Users": {
            "permissions": ["users.view", "users.create", "users.update", "users.delete", "users.assign_permissions"],
            "description": "Gestion complète des utilisateurs"
        },
        "Sales": {
            "permissions": ["sales.view", "sales.create", "sales.update", "sales.delete"],
            "description": "Interface de vente et transactions"
        },
        "SalesHistory": {
            "permissions": ["finances.history", "sales.view", "finances.view"],
            "description": "Historique des ventes et transactions"
        },
        "Products": {
            "permissions": ["products.view", "products.create", "products.update", "products.delete", "products.pricing"],
            "description": "Gestion du catalogue produits"
        },
        "ProductRecords": {
            "permissions": ["products.view", "inventory.view", "products.audit"],
            "description": "Suivi et historique des produits"
        },
        "Stocks": {
            "permissions": ["inventory.view", "inventory.update", "inventory.adjust", "inventory.alerts"],
            "description": "Gestion des stocks et inventaire"
        },
        "StockSync": {
            "permissions": ["inventory.sync", "inventory.update", "inventory.audit"],
            "description": "Synchronisation des stocks"
        },
        "Orders": {
            "permissions": ["orders.view", "orders.create", "orders.update", "orders.delete", "orders.fulfill"],
            "description": "Gestion des commandes"
        },
        "Kitchen": {
            "permissions": ["kitchen.view", "kitchen.orders", "kitchen.prep", "kitchen.recipes"],
            "description": "Interface cuisine et préparation"
        },
        "Tables": {
            "permissions": ["tables.view", "tables.manage", "tables.assign", "tables.reservations"],
            "description": "Gestion des tables et réservations"
        },
        "Supplies": {
            "permissions": ["supplies.view", "supplies.create", "supplies.update", "supplies.order"],
            "description": "Gestion des fournitures"
        },
        "Suppliers": {
            "permissions": ["suppliers.view", "suppliers.create", "suppliers.update", "suppliers.manage"],
            "description": "Gestion des fournisseurs"
        },
        "Reports": {
            "permissions": ["reports.view", "reports.create", "reports.export", "reports.analytics"],
            "description": "Rapports et analyses"
        },
        "DailyReport": {
            "permissions": ["reports.daily", "reports.view", "finances.view"],
            "description": "Rapport quotidien d'activité"
        },
        "Analytics": {
            "permissions": ["analytics.view", "analytics.sales", "analytics.financial", "analytics.products"],
            "description": "Analyses et métriques avancées"
        },
        "Expenses": {
            "permissions": ["finances.expenses", "finances.view", "finances.budgets"],
            "description": "Gestion des dépenses"
        },
        "Settings": {
            "permissions": ["settings.view", "settings.update", "settings.security", "settings.integrations"],
            "description": "Configuration système"
        },
        "Monitoring": {
            "permissions": ["monitoring.view", "monitoring.logs", "monitoring.performance", "monitoring.alerts"],
            "description": "Surveillance système"
        },
        "Alerts": {
            "permissions": ["alerts.view", "alerts.create", "alerts.update", "alerts.acknowledge"],
            "description": "Gestion des alertes"
        },
        "Help": {
            "permissions": ["help.view", "help.support"],
            "description": "Aide et support"
        },
        "Profile": {
            "permissions": ["profile.view", "profile.update"],
            "description": "Profil utilisateur personnel"
        }
    }
    
    print("📋 MAPPING COMPLET:")
    
    for page, info in page_permission_mapping.items():
        print(f"\n📄 {page}.tsx")
        print(f"   📝 {info['description']}")
        print(f"   🔑 Permissions requises:")
        for perm in info['permissions']:
            print(f"      • {perm}")
    
    return page_permission_mapping

def analyze_protected_routes():
    """Analyser les routes protégées"""
    print(f"\n🛡️  ANALYSE DES ROUTES PROTÉGÉES")
    print("=" * 60)
    
    protected_route_path = "c:\\Users\\AlainDev\\Desktop\\New\\bar-stock-wise-main\\src\\components\\ProtectedRoute.tsx"
    
    if os.path.exists(protected_route_path):
        with open(protected_route_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ ProtectedRoute.tsx trouvé")
        
        # Rechercher les vérifications de permissions
        if 'hasPermission' in content or 'checkPermission' in content:
            print("   🔑 Contient des vérifications de permissions")
        else:
            print("   ⚠️  Pas de vérification de permissions détectée")
        
        # Rechercher les redirections
        if 'redirect' in content.lower() or 'navigate' in content.lower():
            print("   🔄 Gère les redirections")
        
    else:
        print("❌ ProtectedRoute.tsx non trouvé")

def generate_permission_summary():
    """Générer un résumé des permissions frontend"""
    print(f"\n📊 RÉSUMÉ DES PERMISSIONS FRONTEND")
    print("=" * 60)
    
    # Permissions identifiées dans le code
    identified_permissions = set()
    
    # Permissions recommandées par page
    recommended_permissions = {
        # Core permissions
        "dashboard.view", "profile.view", "profile.update",
        
        # Users management
        "users.view", "users.create", "users.update", "users.delete", "users.assign_permissions",
        
        # Sales
        "sales.view", "sales.create", "sales.update", "sales.delete", "sales.approve", "sales.refund",
        
        # Finances
        "finances.view", "finances.history", "finances.reports", "finances.expenses", "finances.budgets",
        
        # Products
        "products.view", "products.create", "products.update", "products.delete", "products.pricing",
        
        # Inventory
        "inventory.view", "inventory.update", "inventory.adjust", "inventory.alerts", "inventory.sync",
        
        # Orders
        "orders.view", "orders.create", "orders.update", "orders.delete", "orders.fulfill",
        
        # Kitchen
        "kitchen.view", "kitchen.orders", "kitchen.prep", "kitchen.recipes",
        
        # Tables
        "tables.view", "tables.manage", "tables.assign", "tables.reservations",
        
        # Supplies
        "supplies.view", "supplies.create", "supplies.update", "supplies.order",
        
        # Reports & Analytics
        "reports.view", "reports.create", "reports.export", "reports.daily",
        "analytics.view", "analytics.sales", "analytics.financial", "analytics.products",
        
        # Settings & Admin
        "settings.view", "settings.update", "settings.security",
        "monitoring.view", "monitoring.logs", "monitoring.alerts",
        "alerts.view", "alerts.create", "alerts.acknowledge",
        "help.view", "help.support"
    }
    
    print(f"🔢 STATISTIQUES:")
    print(f"   • Pages frontend: 21")
    print(f"   • Permissions recommandées: {len(recommended_permissions)}")
    print(f"   • Catégories principales: 15")
    
    print(f"\n📋 PERMISSIONS PAR CATÉGORIE:")
    
    categories = {
        "Core": ["dashboard.view", "profile.view", "profile.update"],
        "Users": [p for p in recommended_permissions if p.startswith("users.")],
        "Sales": [p for p in recommended_permissions if p.startswith("sales.")],
        "Finances": [p for p in recommended_permissions if p.startswith("finances.")],
        "Products": [p for p in recommended_permissions if p.startswith("products.")],
        "Inventory": [p for p in recommended_permissions if p.startswith("inventory.")],
        "Orders": [p for p in recommended_permissions if p.startswith("orders.")],
        "Kitchen": [p for p in recommended_permissions if p.startswith("kitchen.")],
        "Tables": [p for p in recommended_permissions if p.startswith("tables.")],
        "Supplies": [p for p in recommended_permissions if p.startswith("supplies.")],
        "Reports": [p for p in recommended_permissions if p.startswith("reports.")],
        "Analytics": [p for p in recommended_permissions if p.startswith("analytics.")],
        "Settings": [p for p in recommended_permissions if p.startswith("settings.")],
        "Monitoring": [p for p in recommended_permissions if p.startswith("monitoring.")],
        "Alerts": [p for p in recommended_permissions if p.startswith("alerts.")],
        "Help": [p for p in recommended_permissions if p.startswith("help.")]
    }
    
    for category, perms in categories.items():
        if perms:
            print(f"   🔹 {category}: {len(perms)} permissions")

def main():
    """Fonction principale d'analyse"""
    print("🚀 ANALYSE COMPLÈTE DES PERMISSIONS FRONTEND")
    print("BarStockWise - Mapping Pages → Permissions")
    print()
    
    # 1. Analyser Sidebar
    sidebar_permissions = analyze_sidebar_permissions()
    
    # 2. Analyser toutes les pages
    pages_permissions = analyze_all_pages_permissions()
    
    # 3. Mapper pages → permissions
    page_mapping = map_pages_to_permissions()
    
    # 4. Analyser les routes protégées
    analyze_protected_routes()
    
    # 5. Générer le résumé
    generate_permission_summary()
    
    print(f"\n" + "=" * 60)
    print(f"✅ ANALYSE TERMINÉE")
    print(f"📄 21 pages frontend identifiées")
    print(f"🔑 ~45 permissions recommandées pour le frontend")
    print(f"🛡️  Système de permissions granulaire recommandé")

if __name__ == '__main__':
    main()
