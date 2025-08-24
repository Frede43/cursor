#!/usr/bin/env python
"""
Script pour vérifier les permissions d'accès à l'historique des ventes
et diagnostiquer pourquoi le menu n'est pas visible
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import User, Permission, UserPermission

def check_sales_history_permissions():
    """Vérifier les permissions pour l'historique des ventes"""
    print("🔍 DIAGNOSTIC DES PERMISSIONS HISTORIQUE DES VENTES")
    print("=" * 55)
    
    # 1. Vérifier l'utilisateur testuser_sales
    try:
        user = User.objects.get(username="testuser_sales")
        print(f"👤 Utilisateur: {user.get_full_name()}")
        print(f"   • Username: {user.username}")
        print(f"   • Rôle: {user.role}")
        print(f"   • Actif: {user.is_active}")
    except User.DoesNotExist:
        print("❌ Utilisateur testuser_sales non trouvé")
        return False
    
    # 2. Vérifier les permissions liées aux ventes
    print(f"\n🔑 PERMISSIONS LIÉES AUX VENTES:")
    
    sales_permissions = [
        'sales.view',
        'sales.create', 
        'sales.history',
        'sales.delete',
        'sales.update'
    ]
    
    user_has_permissions = []
    for perm_code in sales_permissions:
        try:
            permission = Permission.objects.get(code=perm_code)
            user_permission = UserPermission.objects.filter(
                user=user,
                permission=permission,
                is_active=True
            ).first()
            
            if user_permission:
                print(f"   ✅ {perm_code} - {permission.name}")
                user_has_permissions.append(perm_code)
            else:
                print(f"   ❌ {perm_code} - {permission.name} (NON ASSIGNÉE)")
                
        except Permission.DoesNotExist:
            print(f"   ⚠️  {perm_code} - Permission inexistante")
    
    # 3. Analyser le mapping frontend
    print(f"\n🎨 ANALYSE DU MAPPING FRONTEND:")
    print(f"   • Route: /sales-history")
    print(f"   • Composant: SalesHistory.tsx")
    print(f"   • Permission clé: 'sales-history' (dans Sidebar.tsx)")
    print(f"   • Permission backend: 'sales.history'")
    
    # 4. Vérifier la permission spécifique pour l'historique
    has_history_permission = 'sales.history' in user_has_permissions
    print(f"\n📊 RÉSULTAT:")
    print(f"   • Permission sales.history: {'✅ OUI' if has_history_permission else '❌ NON'}")
    
    if not has_history_permission:
        print(f"\n💡 PROBLÈME IDENTIFIÉ:")
        print(f"   L'utilisateur n'a pas la permission 'sales.history'")
        print(f"   Le menu 'Historique Ventes' ne sera pas visible")
        return False
    
    # 5. Vérifier le hook de permissions frontend
    print(f"\n🔧 VÉRIFICATION DU SYSTÈME DE PERMISSIONS:")
    print(f"   • useCanAccessMenu('sales-history') doit retourner true")
    print(f"   • Mapping: sales-history → sales.history")
    print(f"   • Backend: UserPermission.objects.filter(user=user, permission__code='sales.history', is_active=True)")
    
    return True

def fix_sales_history_permission():
    """Corriger la permission pour l'historique des ventes"""
    print(f"\n🔧 CORRECTION DE LA PERMISSION:")
    
    try:
        user = User.objects.get(username="testuser_sales")
        permission = Permission.objects.get(code="sales.history")
        
        # Vérifier si la permission existe déjà
        user_permission, created = UserPermission.objects.get_or_create(
            user=user,
            permission=permission,
            defaults={'is_active': True}
        )
        
        if created:
            print(f"   ✅ Permission 'sales.history' ajoutée")
        else:
            if not user_permission.is_active:
                user_permission.is_active = True
                user_permission.save()
                print(f"   ✅ Permission 'sales.history' activée")
            else:
                print(f"   ℹ️  Permission 'sales.history' déjà active")
        
        return True
        
    except User.DoesNotExist:
        print(f"   ❌ Utilisateur non trouvé")
        return False
    except Permission.DoesNotExist:
        print(f"   ❌ Permission 'sales.history' non trouvée")
        return False
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def verify_all_sales_permissions():
    """Vérifier et corriger toutes les permissions de vente"""
    print(f"\n🔄 VÉRIFICATION COMPLÈTE DES PERMISSIONS DE VENTE:")
    
    try:
        user = User.objects.get(username="testuser_sales")
        
        # Permissions de vente requises
        required_permissions = [
            'sales.view',
            'sales.create',
            'sales.history'
        ]
        
        for perm_code in required_permissions:
            try:
                permission = Permission.objects.get(code=perm_code)
                user_permission, created = UserPermission.objects.get_or_create(
                    user=user,
                    permission=permission,
                    defaults={'is_active': True}
                )
                
                if created:
                    print(f"   ✅ Ajoutée: {perm_code}")
                elif not user_permission.is_active:
                    user_permission.is_active = True
                    user_permission.save()
                    print(f"   ✅ Activée: {perm_code}")
                else:
                    print(f"   ✅ OK: {perm_code}")
                    
            except Permission.DoesNotExist:
                print(f"   ❌ Permission inexistante: {perm_code}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def test_frontend_permission_mapping():
    """Tester le mapping des permissions frontend"""
    print(f"\n🎯 TEST DU MAPPING FRONTEND:")
    
    # Simuler le comportement du hook useCanAccessMenu
    permission_mapping = {
        'sales-history': 'sales.history',
        'sales': 'sales.view',
        'daily-report': 'reports.view',
        'reports': 'reports.view',
        'analytics': 'analytics.view'
    }
    
    try:
        user = User.objects.get(username="testuser_sales")
        
        for frontend_key, backend_permission in permission_mapping.items():
            try:
                permission = Permission.objects.get(code=backend_permission)
                has_permission = UserPermission.objects.filter(
                    user=user,
                    permission=permission,
                    is_active=True
                ).exists()
                
                status = "✅ VISIBLE" if has_permission else "❌ CACHÉ"
                print(f"   • {frontend_key} → {backend_permission}: {status}")
                
            except Permission.DoesNotExist:
                print(f"   • {frontend_key} → {backend_permission}: ⚠️  PERMISSION INEXISTANTE")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC COMPLET - HISTORIQUE DES VENTES")
    print("Utilisateur: testuser_sales")
    print()
    
    # 1. Diagnostic initial
    has_permissions = check_sales_history_permissions()
    
    # 2. Correction si nécessaire
    if not has_permissions:
        print(f"\n🔧 APPLICATION DE LA CORRECTION...")
        if verify_all_sales_permissions():
            print(f"✅ Permissions corrigées")
        else:
            print(f"❌ Correction échouée")
    
    # 3. Test du mapping frontend
    test_frontend_permission_mapping()
    
    # 4. Vérification finale
    print(f"\n" + "=" * 55)
    print(f"📋 RÉSUMÉ FINAL:")
    
    final_check = check_sales_history_permissions()
    
    if final_check:
        print(f"\n🎉 PROBLÈME RÉSOLU!")
        print(f"✅ L'utilisateur a maintenant accès à l'historique des ventes")
        print(f"✅ Le menu 'Historique Ventes' devrait être visible")
        print(f"\n🔄 ACTIONS À EFFECTUER:")
        print(f"1. Déconnectez-vous de l'application")
        print(f"2. Reconnectez-vous avec: testuser_sales / temp123456")
        print(f"3. Vérifiez que le menu 'Historique Ventes' est visible dans 'Finances'")
    else:
        print(f"\n❌ PROBLÈME PERSISTANT")
        print(f"Vérifiez la configuration des permissions dans le backend")

if __name__ == '__main__':
    main()
