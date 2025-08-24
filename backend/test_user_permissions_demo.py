#!/usr/bin/env python
"""
Script de démonstration pour créer un utilisateur avec permissions spécifiques
et tester le système de permissions
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission
from django.contrib.auth import authenticate

def create_permissions_if_needed():
    """Créer les permissions nécessaires si elles n'existent pas"""
    permissions_to_create = [
        {
            'code': 'sales.view',
            'name': 'Voir les ventes',
            'description': 'Accès à la page des ventes et consultation des ventes',
            'category': 'sales'
        },
        {
            'code': 'sales.create',
            'name': 'Créer des ventes',
            'description': 'Pouvoir effectuer des ventes (POS)',
            'category': 'sales'
        },
        {
            'code': 'sales.history',
            'name': 'Historique des ventes',
            'description': 'Accès à l\'historique complet des ventes',
            'category': 'sales'
        }
    ]
    
    print("🔑 Vérification/Création des permissions...")
    created_permissions = []
    for perm_data in permissions_to_create:
        permission, created = Permission.objects.get_or_create(
            code=perm_data['code'],
            defaults={
                'name': perm_data['name'],
                'description': perm_data['description'],
                'category': perm_data['category'],
                'is_active': True
            }
        )
        if created:
            print(f"   ✅ Créée: {permission.name}")
        else:
            print(f"   ℹ️  Existante: {permission.name}")
        created_permissions.append(permission)
    
    return created_permissions

def create_test_user():
    """Créer l'utilisateur de test avec les informations demandées"""
    username = "testuser_sales"
    
    # Supprimer l'utilisateur s'il existe déjà
    try:
        existing_user = User.objects.get(username=username)
        print(f"⚠️  Suppression de l'utilisateur existant: {username}")
        existing_user.delete()
    except User.DoesNotExist:
        pass
    
    # Créer le nouvel utilisateur
    user = User.objects.create_user(
        username=username,
        first_name="Jean",
        last_name="Vendeur",
        email="jean.vendeur@barstock.com",
        phone="+257 79 123 456",
        role="server",
        password="temp123456"
    )
    
    print(f"👤 Utilisateur créé:")
    print(f"   • Nom: {user.get_full_name()}")
    print(f"   • Username: {user.username}")
    print(f"   • Email: {user.email}")
    print(f"   • Rôle: {user.role}")
    print(f"   • Mot de passe: temp123456")
    
    return user

def assign_permissions(user):
    """Assigner les permissions demandées à l'utilisateur"""
    permission_codes = ['sales.view', 'sales.create', 'sales.history']
    
    print(f"\n🔐 Attribution des permissions à {user.username}:")
    assigned_count = 0
    
    for code in permission_codes:
        try:
            permission = Permission.objects.get(code=code)
            user_permission, created = UserPermission.objects.get_or_create(
                user=user,
                permission=permission,
                defaults={'is_active': True}
            )
            if created:
                print(f"   ✅ {permission.name} ({code})")
                assigned_count += 1
            else:
                print(f"   ℹ️  Déjà assignée: {permission.name} ({code})")
        except Permission.DoesNotExist:
            print(f"   ❌ Permission non trouvée: {code}")
    
    print(f"   📊 Total: {assigned_count} nouvelles permissions assignées")

def test_authentication():
    """Tester l'authentification de l'utilisateur créé"""
    username = "testuser_sales"
    password = "temp123456"
    
    print(f"\n🔐 Test d'authentification:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    user = authenticate(username=username, password=password)
    if user:
        print(f"   ✅ Authentification réussie pour {user.get_full_name()}!")
        return user
    else:
        print(f"   ❌ Échec de l'authentification")
        return None

def verify_user_permissions(user):
    """Vérifier et afficher les permissions de l'utilisateur"""
    print(f"\n📋 Permissions de {user.username}:")
    
    # Récupérer toutes les permissions actives de l'utilisateur
    user_permissions = UserPermission.objects.filter(user=user, is_active=True)
    
    if user_permissions.exists():
        print(f"   Total: {user_permissions.count()} permissions")
        for up in user_permissions:
            print(f"   • {up.permission.name}")
            print(f"     Code: {up.permission.code}")
            print(f"     Catégorie: {up.permission.category}")
            print(f"     Accordée le: {up.granted_at.strftime('%d/%m/%Y à %H:%M')}")
            print()
    else:
        print("   ❌ Aucune permission trouvée")
    
    return user_permissions

def simulate_frontend_menu_access(user):
    """Simuler l'accès aux menus du frontend basé sur les permissions"""
    print(f"🎯 Simulation des menus accessibles dans le frontend:")
    
    # Récupérer les codes de permissions de l'utilisateur
    user_permission_codes = list(
        UserPermission.objects.filter(user=user, is_active=True)
        .values_list('permission__code', flat=True)
    )
    
    print(f"   Codes de permissions: {user_permission_codes}")
    
    # Définir les menus et leurs permissions requises
    menu_structure = {
        "🏠 Dashboard": {
            "required_permissions": [],  # Toujours accessible
            "accessible": True
        },
        "💰 Ventes (POS)": {
            "required_permissions": ["sales.create"],
            "accessible": "sales.create" in user_permission_codes
        },
        "📋 Liste des Ventes": {
            "required_permissions": ["sales.view"],
            "accessible": "sales.view" in user_permission_codes
        },
        "📊 Historique des Ventes": {
            "required_permissions": ["sales.history"],
            "accessible": "sales.history" in user_permission_codes
        },
        "📦 Produits": {
            "required_permissions": ["products.view"],
            "accessible": "products.view" in user_permission_codes
        },
        "📈 Stocks": {
            "required_permissions": ["stocks.view"],
            "accessible": "stocks.view" in user_permission_codes
        },
        "👥 Utilisateurs": {
            "required_permissions": ["users.view"],
            "accessible": "users.view" in user_permission_codes
        },
        "⚙️ Paramètres": {
            "required_permissions": ["settings.view"],
            "accessible": "settings.view" in user_permission_codes
        }
    }
    
    accessible_menus = []
    restricted_menus = []
    
    print(f"\n   Résultats:")
    for menu_name, menu_info in menu_structure.items():
        if menu_info["accessible"]:
            accessible_menus.append(menu_name)
            print(f"   ✅ {menu_name}")
        else:
            restricted_menus.append(menu_name)
            print(f"   ❌ {menu_name}")
    
    return accessible_menus, restricted_menus

def demonstrate_permission_checks():
    """Démontrer comment vérifier les permissions dans le code"""
    print(f"\n💻 Exemple de vérification des permissions dans le code:")
    
    print(f"""
    # Dans le hook useAuth.tsx
    const hasPermission = (permissionCode) => {{
        return user?.permissions?.includes(permissionCode) || false;
    }};
    
    # Dans le composant Sidebar.tsx
    {{hasPermission('sales.create') && (
        <NavLink to="/sales">
            <ShoppingCart /> Ventes (POS)
        </NavLink>
    )}}
    
    {{hasPermission('sales.history') && (
        <NavLink to="/sales-history">
            <History /> Historique des Ventes
        </NavLink>
    )}}
    
    # Dans le composant Sales.tsx
    useEffect(() => {{
        if (!hasPermission('sales.create')) {{
            navigate('/unauthorized');
        }}
    }}, []);
    """)

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION - Création d'utilisateur avec permissions spécifiques")
    print("=" * 75)
    print("Objectif: Créer un utilisateur pouvant:")
    print("• Visualiser l'historique des ventes")
    print("• Gérer les ventes (créer des ventes)")
    print("=" * 75)
    
    try:
        # 1. Créer les permissions nécessaires
        print("\n1️⃣ ÉTAPE 1: Préparation des permissions")
        create_permissions_if_needed()
        
        # 2. Créer l'utilisateur
        print(f"\n2️⃣ ÉTAPE 2: Création de l'utilisateur")
        user = create_test_user()
        
        # 3. Assigner les permissions
        print(f"\n3️⃣ ÉTAPE 3: Attribution des permissions")
        assign_permissions(user)
        
        # 4. Tester l'authentification
        print(f"\n4️⃣ ÉTAPE 4: Test d'authentification")
        auth_user = test_authentication()
        
        if auth_user:
            # 5. Vérifier les permissions
            print(f"\n5️⃣ ÉTAPE 5: Vérification des permissions")
            user_permissions = verify_user_permissions(auth_user)
            
            # 6. Simuler l'accès aux menus
            print(f"\n6️⃣ ÉTAPE 6: Simulation des menus frontend")
            accessible, restricted = simulate_frontend_menu_access(auth_user)
            
            # 7. Démonstration du code
            demonstrate_permission_checks()
            
            # RÉSUMÉ FINAL
            print("\n" + "=" * 75)
            print("✅ SUCCÈS - DÉMONSTRATION TERMINÉE")
            print("=" * 75)
            
            print(f"👤 UTILISATEUR CRÉÉ:")
            print(f"   • Nom: Jean Vendeur")
            print(f"   • Username: testuser_sales")
            print(f"   • Password: temp123456")
            print(f"   • Rôle: Serveur")
            
            print(f"\n🔑 PERMISSIONS ASSIGNÉES:")
            print(f"   • sales.view - Voir les ventes")
            print(f"   • sales.create - Créer des ventes (gérer les ventes)")
            print(f"   • sales.history - Visualiser l'historique des ventes")
            
            print(f"\n📱 MENUS ACCESSIBLES ({len(accessible)}):")
            for menu in accessible:
                print(f"   • {menu}")
            
            print(f"\n🚫 MENUS RESTREINTS ({len(restricted)}):")
            for menu in restricted:
                print(f"   • {menu}")
            
            print(f"\n🎯 RÉSULTAT:")
            print(f"   ✅ L'utilisateur peut se connecter")
            print(f"   ✅ L'utilisateur peut gérer les ventes (POS)")
            print(f"   ✅ L'utilisateur peut voir l'historique des ventes")
            print(f"   ✅ L'utilisateur peut voir la liste des ventes")
            print(f"   ❌ L'utilisateur ne peut pas gérer les produits/stocks/utilisateurs")
            
            print(f"\n🔄 PROCHAINES ÉTAPES:")
            print(f"   1. Démarrer le serveur Django: python manage.py runserver")
            print(f"   2. Démarrer le frontend React: npm run dev")
            print(f"   3. Se connecter avec: testuser_sales / temp123456")
            print(f"   4. Vérifier que seuls les menus autorisés sont visibles")
            
        else:
            print("\n❌ ÉCHEC - Problème d'authentification")
            
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
