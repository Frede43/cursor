#!/usr/bin/env python
"""
Script pour vérifier le champ is_active des permissions Sales
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def check_permissions_is_active():
    """Vérifier le champ is_active des permissions"""
    print("🔍 VÉRIFICATION CHAMP is_active DES PERMISSIONS")
    print("=" * 50)
    
    # Vérifier toutes les permissions Sales
    sales_permissions = Permission.objects.filter(category='sales')
    print(f"📊 Total permissions Sales: {sales_permissions.count()}")
    
    if sales_permissions.exists():
        print(f"\n💰 PERMISSIONS SALES:")
        for perm in sales_permissions:
            status = "✅ ACTIF" if perm.is_active else "❌ INACTIF"
            print(f"   • {perm.code} - {perm.name}")
            print(f"     Status: {status}")
            print(f"     ID: {perm.id}")
            print()
        
        # Compter actives vs inactives
        active_count = sales_permissions.filter(is_active=True).count()
        inactive_count = sales_permissions.filter(is_active=False).count()
        
        print(f"📈 RÉSUMÉ:")
        print(f"   • Actives: {active_count}")
        print(f"   • Inactives: {inactive_count}")
        
        if inactive_count > 0:
            print(f"\n⚠️  PROBLÈME IDENTIFIÉ!")
            print(f"   {inactive_count} permissions Sales sont INACTIVES")
            print(f"   L'API filtre avec is_active=True")
            print(f"   Ces permissions n'apparaissent pas dans le frontend")
            return False
        else:
            print(f"\n✅ TOUTES LES PERMISSIONS SALES SONT ACTIVES")
            return True
    else:
        print(f"\n❌ AUCUNE PERMISSION SALES TROUVÉE")
        return False

def fix_inactive_permissions():
    """Activer toutes les permissions Sales inactives"""
    print(f"\n🔧 ACTIVATION DES PERMISSIONS INACTIVES")
    print("=" * 50)
    
    # Trouver les permissions inactives
    inactive_sales = Permission.objects.filter(category='sales', is_active=False)
    count = inactive_sales.count()
    
    if count > 0:
        print(f"🔄 Activation de {count} permissions Sales...")
        
        # Activer toutes les permissions inactives
        updated = inactive_sales.update(is_active=True)
        print(f"✅ {updated} permissions activées")
        
        # Vérifier le résultat
        still_inactive = Permission.objects.filter(category='sales', is_active=False).count()
        if still_inactive == 0:
            print(f"🎉 TOUTES LES PERMISSIONS SALES SONT MAINTENANT ACTIVES")
            return True
        else:
            print(f"⚠️  {still_inactive} permissions restent inactives")
            return False
    else:
        print(f"✅ Aucune permission Sales inactive trouvée")
        return True

def test_api_after_fix():
    """Tester l'API après correction"""
    print(f"\n🌐 TEST API APRÈS CORRECTION")
    print("=" * 50)
    
    import requests
    
    try:
        url = "http://127.0.0.1:8000/accounts/permissions/list/"
        response = requests.get(url, timeout=10)
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Analyser les permissions
            if isinstance(data, dict) and 'results' in data:
                permissions = data['results']
            elif isinstance(data, list):
                permissions = data
            else:
                print(f"❌ Format de réponse inattendu")
                return False
            
            # Chercher Sales
            sales_found = False
            for perm in permissions:
                if perm.get('category') == 'sales':
                    sales_found = True
                    break
            
            if sales_found:
                print(f"🎉 SALES MAINTENANT VISIBLE DANS L'API!")
                
                # Compter les permissions Sales
                sales_count = len([p for p in permissions if p.get('category') == 'sales'])
                print(f"💰 {sales_count} permissions Sales retournées")
                return True
            else:
                print(f"❌ Sales toujours absent de l'API")
                return False
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    print("🚀 DIAGNOSTIC ET CORRECTION - CHAMP is_active")
    print()
    
    # 1. Vérifier l'état actuel
    all_active = check_permissions_is_active()
    
    # 2. Si des permissions sont inactives, les corriger
    if not all_active:
        fixed = fix_inactive_permissions()
        
        if fixed:
            # 3. Re-vérifier après correction
            all_active = check_permissions_is_active()
            
            # 4. Tester l'API
            api_ok = test_api_after_fix()
            
            if api_ok:
                print(f"\n🎉 PROBLÈME RÉSOLU!")
                print(f"✅ Sales devrait maintenant apparaître dans le frontend")
                print(f"✅ Actualisez le navigateur (Ctrl+Shift+R)")
            else:
                print(f"\n⚠️  Problème API persistant")
        else:
            print(f"\n❌ Échec de la correction")
    else:
        # Tester l'API même si tout semble OK
        api_ok = test_api_after_fix()
        
        if api_ok:
            print(f"\n✅ TOUT FONCTIONNE!")
            print(f"Sales devrait être visible dans le frontend")
        else:
            print(f"\n🔍 Problème API malgré permissions actives")

if __name__ == '__main__':
    main()
