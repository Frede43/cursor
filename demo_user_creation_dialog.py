#!/usr/bin/env python
"""
Script de démonstration du Dialog Modal de création d'utilisateur
Simule l'utilisation du formulaire complet dans Users.tsx
"""

import os
import sys
import django

# Configuration Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission

def simulate_dialog_form_submission():
    """Simuler la soumission du formulaire de création d'utilisateur"""
    print("🎯 SIMULATION DU DIALOG MODAL DE CRÉATION D'UTILISATEUR")
    print("=" * 65)
    print("Interface: Users.tsx - Dialog 'Créer un nouvel utilisateur'")
    print("=" * 65)
    
    # Données du formulaire comme saisies dans le dialog
    form_data = {
        "username": "testuser_sales",
        "first_name": "Jean",
        "last_name": "Vendeur", 
        "email": "jean.vendeur@barstock.com",
        "phone": "+257 79 123 456",
        "role": "server",
        "permissions": [
            "sales.view",      # ✅ Voir les ventes
            "sales.create",    # ✅ Créer des ventes (gérer les ventes)
            "sales.history"    # ✅ Visualiser l'historique des ventes
        ]
    }
    
    print("📋 DONNÉES DU FORMULAIRE:")
    print(f"   • Nom d'utilisateur: {form_data['username']}")
    print(f"   • Prénom: {form_data['first_name']}")
    print(f"   • Nom: {form_data['last_name']}")
    print(f"   • Email: {form_data['email']}")
    print(f"   • Téléphone: {form_data['phone']}")
    print(f"   • Rôle: {form_data['role']}")
    print(f"   • Permissions sélectionnées:")
    for perm in form_data['permissions']:
        permission_name = {
            'sales.view': 'Voir les ventes',
            'sales.create': 'Créer des ventes',
            'sales.history': 'Historique des ventes'
        }.get(perm, perm)
        print(f"     ☑️ {permission_name} ({perm})")
    
    return form_data

def simulate_frontend_validation(form_data):
    """Simuler la validation côté frontend"""
    print(f"\n🔍 VALIDATION FRONTEND:")
    
    errors = []
    
    # Validation des champs obligatoires
    if not form_data['username'].strip():
        errors.append("Nom d'utilisateur requis")
    if not form_data['first_name'].strip():
        errors.append("Prénom requis")
    if not form_data['last_name'].strip():
        errors.append("Nom requis")
    if not form_data['email'].strip():
        errors.append("Email requis")
    if not form_data['role']:
        errors.append("Rôle requis")
    
    # Validation de l'email
    if '@' not in form_data['email']:
        errors.append("Format email invalide")
    
    if errors:
        print("   ❌ Erreurs de validation:")
        for error in errors:
            print(f"      • {error}")
        return False
    else:
        print("   ✅ Validation réussie")
        return True

def simulate_api_call(form_data):
    """Simuler l'appel API de création d'utilisateur"""
    print(f"\n🌐 APPEL API - createUserMutation.mutateAsync():")
    
    # Préparer les données pour l'API
    api_data = {
        **form_data,
        "password": "temp123456"  # Mot de passe temporaire
    }
    
    print(f"   URL: POST /accounts/users/")
    print(f"   Payload: {api_data}")
    
    try:
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=form_data['username']).exists():
            print("   ⚠️  Utilisateur existant supprimé pour la démo")
            User.objects.filter(username=form_data['username']).delete()
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=api_data['username'],
            first_name=api_data['first_name'],
            last_name=api_data['last_name'],
            email=api_data['email'],
            phone=api_data['phone'],
            role=api_data['role'],
            password=api_data['password']
        )
        
        print(f"   ✅ Utilisateur créé avec ID: {user.id}")
        
        # Assigner les permissions
        for perm_code in api_data['permissions']:
            try:
                permission = Permission.objects.get(code=perm_code)
                UserPermission.objects.create(
                    user=user,
                    permission=permission,
                    is_active=True
                )
                print(f"   ✅ Permission assignée: {perm_code}")
            except Permission.DoesNotExist:
                print(f"   ❌ Permission non trouvée: {perm_code}")
        
        return user
        
    except Exception as e:
        print(f"   ❌ Erreur API: {str(e)}")
        return None

def simulate_success_response(user):
    """Simuler la réponse de succès et les actions frontend"""
    print(f"\n🎉 RÉPONSE DE SUCCÈS:")
    
    # Toast de succès
    print(f"   📢 Toast affiché:")
    print(f"      Titre: 'Utilisateur créé'")
    print(f"      Message: 'L'utilisateur a été créé avec succès. Mot de passe temporaire: temp123456'")
    
    # Réinitialisation du formulaire
    print(f"\n   🔄 Actions frontend:")
    print(f"      • Formulaire réinitialisé")
    print(f"      • Dialog fermé (setShowNewUserDialog(false))")
    print(f"      • Liste des utilisateurs actualisée (refetchUsers())")
    
    # Données retournées
    user_response = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "is_active": user.is_active,
        "permissions_by_category": {}
    }
    
    # Organiser les permissions par catégorie
    user_permissions = UserPermission.objects.filter(user=user, is_active=True)
    permissions_by_category = {}
    
    for up in user_permissions:
        category = up.permission.category
        if category not in permissions_by_category:
            permissions_by_category[category] = []
        
        permissions_by_category[category].append({
            "code": up.permission.code,
            "name": up.permission.name,
            "description": up.permission.description
        })
    
    user_response["permissions_by_category"] = permissions_by_category
    
    print(f"\n   📋 Données utilisateur retournées:")
    print(f"      • ID: {user_response['id']}")
    print(f"      • Nom complet: {user_response['first_name']} {user_response['last_name']}")
    print(f"      • Permissions par catégorie: {len(permissions_by_category)} catégories")
    
    return user_response

def simulate_user_list_update(user_response):
    """Simuler la mise à jour de la liste des utilisateurs"""
    print(f"\n📝 MISE À JOUR DE LA LISTE DES UTILISATEURS:")
    
    # Simuler le mapping des données comme dans Users.tsx
    mapped_user = {
        "id": str(user_response['id']),
        "firstName": user_response['first_name'],
        "lastName": user_response['last_name'],
        "email": user_response['email'],
        "phone": user_response['phone'],
        "role": user_response['role'],
        "status": "active" if user_response['is_active'] else "inactive",
        "lastLogin": "",
        "createdAt": "2024-08-23",
        "permissions": []
    }
    
    # Extraire les codes de permissions
    for category, perms in user_response['permissions_by_category'].items():
        for perm in perms:
            mapped_user['permissions'].append(perm['code'])
    
    print(f"   📊 Nouvel utilisateur dans la liste:")
    print(f"      • Nom: {mapped_user['firstName']} {mapped_user['lastName']}")
    print(f"      • Statut: {mapped_user['status']}")
    print(f"      • Rôle: {mapped_user['role']}")
    print(f"      • Permissions: {len(mapped_user['permissions'])}")
    
    # Simuler l'affichage dans l'interface
    print(f"\n   🎨 Affichage dans l'interface:")
    print(f"      • Card utilisateur ajoutée à la liste")
    print(f"      • Badge de statut: ✅ Actif")
    print(f"      • Badge de rôle: 🟢 Serveur")
    print(f"      • Actions disponibles: 👁️ Voir, ✏️ Modifier, 🗑️ Supprimer")
    
    return mapped_user

def demonstrate_permission_display():
    """Démontrer l'affichage des permissions dans le dialog de visualisation"""
    print(f"\n🔍 DIALOG DE VISUALISATION DES PERMISSIONS:")
    
    print(f"   Interface: Dialog 'Détails utilisateur'")
    print(f"   Déclencheur: Clic sur le bouton 👁️ Voir")
    
    print(f"\n   📋 Permissions détaillées affichées:")
    print(f"      📁 SALES (3 permissions):")
    print(f"         ☑️ Voir les ventes (sales.view)")
    print(f"         ☑️ Créer des ventes (sales.create)")
    print(f"         ☑️ Historique des ventes (sales.history)")
    print(f"      📁 PRODUCTS (0 permissions):")
    print(f"         ☐ Voir les produits (products.view)")
    print(f"         ☐ Créer des produits (products.create)")
    print(f"      📁 USERS (0 permissions):")
    print(f"         ☐ Voir les utilisateurs (users.view)")
    print(f"         ☐ Créer des utilisateurs (users.create)")

def main():
    """Fonction principale de démonstration"""
    print("🚀 DÉMONSTRATION COMPLÈTE DU DIALOG DE CRÉATION D'UTILISATEUR")
    print("Interface: src/pages/Users.tsx")
    print("Composant: Dialog 'Créer un nouvel utilisateur'")
    print()
    
    # 1. Simulation du remplissage du formulaire
    print("1️⃣ REMPLISSAGE DU FORMULAIRE")
    form_data = simulate_dialog_form_submission()
    
    # 2. Validation frontend
    print("2️⃣ VALIDATION FRONTEND")
    if not simulate_frontend_validation(form_data):
        print("❌ Validation échouée - Arrêt du processus")
        return
    
    # 3. Appel API
    print("3️⃣ APPEL API")
    user = simulate_api_call(form_data)
    
    if user:
        # 4. Réponse de succès
        print("4️⃣ TRAITEMENT DE LA RÉPONSE")
        user_response = simulate_success_response(user)
        
        # 5. Mise à jour de la liste
        print("5️⃣ MISE À JOUR DE L'INTERFACE")
        mapped_user = simulate_user_list_update(user_response)
        
        # 6. Démonstration des permissions
        print("6️⃣ AFFICHAGE DES PERMISSIONS")
        demonstrate_permission_display()
        
        # RÉSUMÉ FINAL
        print("\n" + "=" * 65)
        print("✅ DÉMONSTRATION TERMINÉE AVEC SUCCÈS")
        print("=" * 65)
        
        print("🎯 PROCESSUS COMPLET SIMULÉ:")
        print("   1. ✅ Ouverture du dialog de création")
        print("   2. ✅ Remplissage du formulaire complet")
        print("   3. ✅ Sélection des permissions spécifiques")
        print("   4. ✅ Validation des données")
        print("   5. ✅ Création via API")
        print("   6. ✅ Attribution des permissions")
        print("   7. ✅ Mise à jour de l'interface")
        print("   8. ✅ Affichage dans la liste")
        
        print(f"\n👤 UTILISATEUR CRÉÉ:")
        print(f"   • Nom: Jean Vendeur")
        print(f"   • Username: testuser_sales")
        print(f"   • Rôle: Serveur")
        print(f"   • Permissions: Gestion des ventes + Historique")
        
        print(f"\n🎮 POUR TESTER DANS L'INTERFACE:")
        print(f"   1. Démarrer le frontend: npm run dev")
        print(f"   2. Se connecter en tant qu'admin")
        print(f"   3. Aller sur la page Utilisateurs")
        print(f"   4. Vérifier que 'Jean Vendeur' apparaît dans la liste")
        print(f"   5. Cliquer sur 👁️ pour voir ses permissions")
        print(f"   6. Se déconnecter et tester la connexion avec:")
        print(f"      Username: testuser_sales")
        print(f"      Password: temp123456")
        print(f"   7. Vérifier que seuls les menus de vente sont visibles")
        
    else:
        print("❌ ÉCHEC - Impossible de créer l'utilisateur")

if __name__ == '__main__':
    main()
