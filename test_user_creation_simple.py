#!/usr/bin/env python
"""
Script simplifié pour créer et tester un utilisateur avec permissions spécifiques
Utilise directement Django ORM
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.barstock_api.settings')
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
            print(f"✅ Permission créée: {permission.name}")
        else:
            print(f"ℹ️  Permission existante: {permission.name}")
        created_permissions.append(permission)
    
    return created_permissions

def create_test_user():
    """Créer l'utilisateur de test"""
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
    
    print(f"✅ Utilisateur créé: {user.get_full_name()} ({user.username})")
    return user

def assign_permissions(user):
    """Assigner les permissions à l'utilisateur"""
    permission_codes = ['sales.view', 'sales.create', 'sales.history']
    
    print(f"\n🔑 Attribution des permissions:")
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
            else:
                print(f"   ℹ️  Déjà assignée: {permission.name} ({code})")
        except Permission.DoesNotExist:
            print(f"   ❌ Permission non trouvée: {code}")

def test_user_authentication():
    """Tester l'authentification de l'utilisateur"""
    username = "testuser_sales"
    password = "temp123456"
    
    print(f"\n🔐 Test d'authentification:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    user = authenticate(username=username, password=password)
    if user:
        print(f"   ✅ Authentification réussie!")
        return user
    else:
        print(f"   ❌ Échec de l'authentification")
        return None

def verify_permissions(user):
    """Vérifier les permissions de l'utilisateur"""
    print(f"\n📋 Vérification des permissions pour {user.username}:")
    
    # Permissions directes
    user_permissions = UserPermission.objects.filter(user=user, is_active=True)
    print(f"   Permissions directes: {user_permissions.count()}")
    
    for up in user_permissions:
        print(f"   • {up.permission.name} ({up.permission.code})")
    
    # Test des méthodes de vérification
    print(f"\n🎯 Tests de vérification:")
    
    # Simuler les vérifications que ferait le frontend
    has_sales_view = user_permissions.filter(permission__code='sales.view').exists()
    has_sales_create = user_permissions.filter(permission__code='sales.create').exists()
    has_sales_history = user_permissions.filter(permission__code='sales.history').exists()
    
    print(f"   • Peut voir les ventes: {'✅' if has_sales_view else '❌'}")
    print(f"   • Peut créer des ventes: {'✅' if has_sales_create else '❌'}")
    print(f"   • Peut voir l'historique: {'✅' if has_sales_history else '❌'}")
    
    return {
        'sales.view': has_sales_view,
        'sales.create': has_sales_create,
        'sales.history': has_sales_history
    }

def simulate_menu_access(permissions):
    """Simuler l'accès aux menus frontend"""
    print(f"\n🎯 Simulation des menus accessibles:")
    
    menus = {
        "Dashboard": True,  # Toujours accessible
        "Ventes (POS)": permissions.get('sales.create', False),
        "Historique des Ventes": permissions.get('sales.history', False),
        "Liste des Ventes": permissions.get('sales.view', False),
        "Produits": False,  # Pas de permission
        "Stocks": False,    # Pas de permission
        "Utilisateurs": False,  # Pas de permission
        "Paramètres": False     # Pas de permission
    }
    
    accessible = []
    restricted = []
    
    for menu, has_access in menus.items():
        if has_access:
            accessible.append(menu)
            print(f"   ✅ {menu}")
        else:
            restricted.append(menu)
            print(f"   ❌ {menu}")
    
    return accessible, restricted

def main():
    """Fonction principale"""
    print("🚀 Test de création d'utilisateur avec permissions spécifiques")
    print("=" * 65)
    
    try:
        # 1. Créer les permissions nécessaires
        print("1️⃣ Création des permissions...")
        create_permissions_if_needed()
        
        # 2. Créer l'utilisateur
        print(f"\n2️⃣ Création de l'utilisateur...")
        user = create_test_user()
        
        # 3. Assigner les permissions
        print(f"\n3️⃣ Attribution des permissions...")
        assign_permissions(user)
        
        # 4. Tester l'authentification
        print(f"\n4️⃣ Test d'authentification...")
        auth_user = test_user_authentication()
        
        if auth_user:
            # 5. Vérifier les permissions
            print(f"\n5️⃣ Vérification des permissions...")
            user_perms = verify_permissions(auth_user)
            
            # 6. Simuler l'accès aux menus
            print(f"\n6️⃣ Simulation des menus...")
            accessible, restricted = simulate_menu_access(user_perms)
            
            # Résumé final
            print("\n" + "=" * 65)
            print("✅ SUCCÈS - Utilisateur créé et testé!")
            print("=" * 65)
            print(f"👤 Utilisateur: Jean Vendeur (testuser_sales)")
            print(f"🔑 Permissions: Voir ventes, Créer ventes, Historique ventes")
            print(f"📱 Menus accessibles: {len(accessible)}")
            print(f"🚫 Menus restreints: {len(restricted)}")
            
            print(f"\n📝 Informations de connexion:")
            print(f"   Username: testuser_sales")
            print(f"   Password: temp123456")
            
            print(f"\n🎯 L'utilisateur peut maintenant:")
            print(f"   • Se connecter au système")
            print(f"   • Accéder au module de ventes")
            print(f"   • Créer de nouvelles ventes")
            print(f"   • Consulter l'historique des ventes")
            
        else:
            print("\n❌ ÉCHEC - Problème d'authentification")
            
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
