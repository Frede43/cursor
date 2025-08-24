#!/usr/bin/env python
"""
Script pour analyser toutes les permissions existantes et recommander un système complet
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from accounts.models import Permission

def analyze_current_permissions():
    """Analyser toutes les permissions actuelles"""
    print("📊 PERMISSIONS ACTUELLES DANS LE SYSTÈME")
    print("=" * 60)
    
    all_permissions = Permission.objects.all().order_by('category', 'code')
    
    # Grouper par catégorie
    categories = {}
    for perm in all_permissions:
        cat = perm.category or 'Autre'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(perm)
    
    print(f"📈 Total permissions: {all_permissions.count()}")
    print(f"📁 Catégories: {len(categories)}")
    
    print(f"\n📋 DÉTAIL PAR CATÉGORIE:")
    for cat, perms in sorted(categories.items()):
        active_count = len([p for p in perms if p.is_active])
        print(f"\n🔹 {cat.upper()} ({len(perms)} permissions, {active_count} actives)")
        
        for perm in perms:
            status = "✅" if perm.is_active else "❌"
            print(f"   {status} {perm.code} - {perm.name}")
    
    return categories

def recommend_complete_permission_system():
    """Recommander un système de permissions complet pour une application web sécurisée"""
    print(f"\n🔐 SYSTÈME DE PERMISSIONS RECOMMANDÉ")
    print("=" * 60)
    print("Basé sur les meilleures pratiques de sécurité pour applications web")
    
    recommended_permissions = {
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
            ("sales.view", "Voir les ventes", "Consulter les ventes"),
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
            ("finances.taxes", "Gestion fiscale", "Gérer les taxes et déclarations"),
        ],
        
        "inventory": [
            ("inventory.view", "Voir l'inventaire", "Consulter les stocks"),
            ("inventory.create", "Ajouter produits", "Ajouter de nouveaux produits"),
            ("inventory.update", "Modifier produits", "Modifier les informations produits"),
            ("inventory.delete", "Supprimer produits", "Retirer des produits"),
            ("inventory.adjust", "Ajuster stocks", "Corriger les quantités en stock"),
            ("inventory.transfer", "Transférer stocks", "Déplacer des stocks entre emplacements"),
            ("inventory.alerts", "Alertes stock", "Gérer les alertes de stock bas"),
            ("inventory.audit", "Audit inventaire", "Effectuer des audits d'inventaire"),
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
        
        "reports": [
            ("reports.view", "Voir rapports", "Consulter les rapports"),
            ("reports.create", "Créer rapports", "Générer de nouveaux rapports"),
            ("reports.export", "Exporter rapports", "Exporter les rapports"),
            ("reports.schedule", "Programmer rapports", "Automatiser la génération"),
            ("reports.analytics", "Analyses avancées", "Accéder aux analyses détaillées"),
            ("reports.dashboard", "Tableaux de bord", "Configurer les dashboards"),
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
        ]
    }
    
    print(f"\n📋 PERMISSIONS RECOMMANDÉES PAR CATÉGORIE:")
    total_recommended = 0
    
    for category, permissions in recommended_permissions.items():
        print(f"\n🔹 {category.upper()} ({len(permissions)} permissions)")
        for code, name, description in permissions:
            print(f"   • {code} - {name}")
            print(f"     └─ {description}")
        total_recommended += len(permissions)
    
    print(f"\n📊 RÉSUMÉ:")
    print(f"   • Total recommandé: {total_recommended} permissions")
    print(f"   • Catégories: {len(recommended_permissions)}")
    
    return recommended_permissions

def compare_current_vs_recommended(current_categories, recommended_permissions):
    """Comparer les permissions actuelles avec les recommandations"""
    print(f"\n🔄 COMPARAISON ACTUEL VS RECOMMANDÉ")
    print("=" * 60)
    
    # Permissions actuelles
    current_codes = set()
    for cat, perms in current_categories.items():
        for perm in perms:
            current_codes.add(perm.code)
    
    # Permissions recommandées
    recommended_codes = set()
    for cat, perms in recommended_permissions.items():
        for code, name, desc in perms:
            recommended_codes.add(code)
    
    # Analyse
    missing = recommended_codes - current_codes
    extra = current_codes - recommended_codes
    common = current_codes & recommended_codes
    
    print(f"📊 STATISTIQUES:")
    print(f"   • Permissions actuelles: {len(current_codes)}")
    print(f"   • Permissions recommandées: {len(recommended_codes)}")
    print(f"   • Communes: {len(common)}")
    print(f"   • Manquantes: {len(missing)}")
    print(f"   • En surplus: {len(extra)}")
    
    if missing:
        print(f"\n❌ PERMISSIONS MANQUANTES ({len(missing)}):")
        for code in sorted(missing):
            # Trouver la catégorie et description
            for cat, perms in recommended_permissions.items():
                for rec_code, name, desc in perms:
                    if rec_code == code:
                        print(f"   • {code} ({cat}) - {name}")
                        break
    
    if extra:
        print(f"\n➕ PERMISSIONS SUPPLÉMENTAIRES ({len(extra)}):")
        for code in sorted(extra):
            print(f"   • {code}")
    
    # Calcul du score de complétude
    completeness = (len(common) / len(recommended_codes)) * 100 if recommended_codes else 0
    print(f"\n📈 SCORE DE COMPLÉTUDE: {completeness:.1f}%")
    
    return missing, extra, completeness

def security_recommendations():
    """Recommandations de sécurité pour les permissions"""
    print(f"\n🔐 RECOMMANDATIONS DE SÉCURITÉ")
    print("=" * 60)
    
    recommendations = [
        "🔹 PRINCIPE DU MOINDRE PRIVILÈGE",
        "   • Accordez uniquement les permissions nécessaires",
        "   • Révisez régulièrement les permissions accordées",
        "   • Supprimez les permissions inutilisées",
        "",
        "🔹 SÉPARATION DES RESPONSABILITÉS",
        "   • Séparez les permissions critiques (ex: delete, approve)",
        "   • Évitez de donner tous les pouvoirs à un seul utilisateur",
        "   • Implémentez des workflows d'approbation",
        "",
        "🔹 AUDIT ET TRAÇABILITÉ",
        "   • Loggez toutes les actions sensibles",
        "   • Gardez un historique des changements de permissions",
        "   • Surveillez les accès anormaux",
        "",
        "🔹 GESTION DES RÔLES",
        "   • Créez des rôles prédéfinis (Admin, Manager, Staff, etc.)",
        "   • Utilisez des templates de permissions par rôle",
        "   • Facilitez l'attribution en masse",
        "",
        "🔹 SÉCURITÉ TECHNIQUE",
        "   • Validez les permissions côté backend ET frontend",
        "   • Utilisez des tokens JWT avec expiration",
        "   • Implémentez une authentification à deux facteurs",
        "   • Chiffrez les données sensibles",
        "",
        "🔹 CONFORMITÉ",
        "   • Respectez les réglementations (RGPD, etc.)",
        "   • Documentez les accès aux données personnelles",
        "   • Implémentez le droit à l'oubli",
        "",
        "🔹 MONITORING",
        "   • Alertes sur les actions critiques",
        "   • Détection d'anomalies dans les accès",
        "   • Rapports réguliers d'utilisation des permissions"
    ]
    
    for rec in recommendations:
        print(rec)

def main():
    """Fonction principale d'analyse"""
    print("🚀 ANALYSE COMPLÈTE DU SYSTÈME DE PERMISSIONS")
    print("Recommandations pour une application web sécurisée")
    print()
    
    # 1. Analyser les permissions actuelles
    current_categories = analyze_current_permissions()
    
    # 2. Recommandations complètes
    recommended_permissions = recommend_complete_permission_system()
    
    # 3. Comparaison
    missing, extra, completeness = compare_current_vs_recommended(current_categories, recommended_permissions)
    
    # 4. Recommandations de sécurité
    security_recommendations()
    
    # 5. Conclusion
    print(f"\n" + "=" * 60)
    print(f"📋 CONCLUSION:")
    
    if completeness >= 80:
        print(f"✅ Système de permissions bien développé ({completeness:.1f}%)")
    elif completeness >= 60:
        print(f"⚠️  Système de permissions correct mais incomplet ({completeness:.1f}%)")
    else:
        print(f"❌ Système de permissions insuffisant ({completeness:.1f}%)")
    
    print(f"\n💡 PROCHAINES ÉTAPES RECOMMANDÉES:")
    print(f"   1. Implémenter les {len(missing)} permissions manquantes")
    print(f"   2. Créer des rôles prédéfinis avec templates")
    print(f"   3. Améliorer l'audit et la traçabilité")
    print(f"   4. Tester la sécurité avec des tests de pénétration")
    print(f"   5. Former les utilisateurs sur la sécurité")

if __name__ == '__main__':
    main()
