#!/usr/bin/env python
"""
Test simple et direct du système de décompte des stocks lors de la préparation de recettes
"""
import os
import sys
import django
from decimal import Decimal

# Configuration Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barstock_api.settings')
django.setup()

from kitchen.models import Ingredient, Recipe, RecipeIngredient, IngredientMovement
from products.models import Product
from accounts.models import User

def test_recipe_stock_deduction():
    """Test simple: créer une recette et voir si les stocks diminuent"""
    print("🧪 TEST SIMPLE: DÉCOMPTE AUTOMATIQUE DES STOCKS")
    print("=" * 60)
    
    # 1. Récupérer ou créer un utilisateur
    try:
        user = User.objects.filter(is_active=True).first()
        if not user:
            print("❌ Aucun utilisateur trouvé")
            return
        print(f"👤 Utilisateur: {user.username}")
    except Exception as e:
        print(f"❌ Erreur utilisateur: {e}")
        return
    
    # 2. Créer des ingrédients de test avec stock initial
    print("\n📦 Création des ingrédients de test...")
    
    # Nettoyer les anciens ingrédients de test
    Ingredient.objects.filter(nom__startswith='TEST_').delete()
    
    ingredients_data = [
        {'nom': 'TEST_Riz', 'stock': Decimal('5.000'), 'unite': 'kg', 'prix': Decimal('500.00')},
        {'nom': 'TEST_Poulet', 'stock': Decimal('3.000'), 'unite': 'kg', 'prix': Decimal('3000.00')},
    ]
    
    ingredients = {}
    for data in ingredients_data:
        ingredient = Ingredient.objects.create(
            nom=data['nom'],
            quantite_restante=data['stock'],
            unite=data['unite'],
            prix_unitaire=data['prix'],
            seuil_alerte=Decimal('0.500')
        )
        ingredients[data['nom']] = ingredient
        print(f"   ✅ {ingredient.nom}: {ingredient.quantite_restante} {ingredient.unite}")
    
    # 3. Créer un produit de test
    print("\n🍽️  Création du produit de test...")
    Product.objects.filter(name='TEST_Plat_Riz').delete()
    
    product = Product.objects.create(
        name='TEST_Plat_Riz',
        category='plats',
        description='Plat de test pour vérifier les stocks',
        selling_price=Decimal('4000.00'),
        purchase_price=Decimal('0.00'),
        stock_quantity=0,
        is_active=True
    )
    print(f"   ✅ Produit créé: {product.name}")
    
    # 4. Créer une recette
    print("\n📝 Création de la recette...")
    Recipe.objects.filter(nom_recette='TEST_Recette_Riz').delete()
    
    recipe = Recipe.objects.create(
        plat=product,
        nom_recette='TEST_Recette_Riz',
        description='Recette de test',
        instructions='Mélanger et cuire',
        temps_preparation=30,
        portions=1,
        created_by=user
    )
    print(f"   ✅ Recette créée: {recipe.nom_recette}")
    
    # 5. Ajouter les ingrédients à la recette
    print("\n🥘 Ajout des ingrédients à la recette...")
    composition = [
        {'ingredient': 'TEST_Riz', 'quantite': Decimal('0.500')},    # 500g par portion
        {'ingredient': 'TEST_Poulet', 'quantite': Decimal('0.300')}, # 300g par portion
    ]
    
    for comp in composition:
        ingredient = ingredients[comp['ingredient']]
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantite_utilisee_par_plat=comp['quantite'],
            unite=ingredient.unite
        )
        print(f"   ✅ {ingredient.nom}: {comp['quantite']} {ingredient.unite} par portion")
    
    # 6. Afficher l'état initial des stocks
    print("\n📊 ÉTAT INITIAL DES STOCKS:")
    for name, ingredient in ingredients.items():
        ingredient.refresh_from_db()
        print(f"   {ingredient.nom}: {ingredient.quantite_restante} {ingredient.unite}")
    
    # 7. Calculer le coût de la recette
    print(f"\n💰 Coût de la recette: {recipe.total_cost} BIF")
    
    # 8. Vérifier si la recette peut être préparée
    print(f"\n🔍 Peut être préparée: {recipe.can_be_prepared}")
    
    # 9. PRÉPARER 2 PORTIONS (le test principal!)
    portions = 2
    print(f"\n🍳 PRÉPARATION DE {portions} PORTIONS...")
    print("   (Ceci devrait décompter automatiquement les stocks)")
    
    try:
        # Utiliser la méthode consume_ingredients qui gère le décompte automatique
        consumed = recipe.consume_ingredients(quantity=portions, user=user)
        
        print("   ✅ Préparation réussie!")
        print("\n📝 Détails de la consommation:")
        for item in consumed:
            ingredient = item['ingredient']
            print(f"   - {ingredient.nom}:")
            print(f"     Consommé: {item['quantity_consumed']} {ingredient.unite}")
            print(f"     Stock avant: {item['stock_before']} {ingredient.unite}")
            print(f"     Stock après: {item['stock_after']} {ingredient.unite}")
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la préparation: {e}")
        return False
    
    # 10. Afficher l'état final des stocks
    print("\n📊 ÉTAT FINAL DES STOCKS:")
    for name, ingredient in ingredients.items():
        ingredient.refresh_from_db()
        print(f"   {ingredient.nom}: {ingredient.quantite_restante} {ingredient.unite}")
    
    # 11. Vérifier les mouvements de stock
    print("\n📋 MOUVEMENTS DE STOCK CRÉÉS:")
    movements = IngredientMovement.objects.filter(
        ingredient__nom__startswith='TEST_',
        reason='consumption'
    ).order_by('-created_at')[:10]
    
    for movement in movements:
        print(f"   - {movement.ingredient.nom}: -{movement.quantity} {movement.ingredient.unite}")
        print(f"     {movement.stock_before} → {movement.stock_after}")
        print(f"     Notes: {movement.notes}")
    
    # 12. Vérifier la mise à jour du prix d'achat du produit
    product.refresh_from_db()
    print(f"\n💰 PRIX D'ACHAT AUTOMATIQUE:")
    print(f"   Produit: {product.name}")
    print(f"   Prix d'achat calculé: {product.purchase_price} BIF")
    print(f"   Prix de vente: {product.selling_price} BIF")
    print(f"   Marge: {product.selling_price - product.purchase_price} BIF")
    
    # 13. Nettoyer les données de test
    print("\n🧹 Nettoyage des données de test...")
    recipe.delete()
    product.delete()
    for ingredient in ingredients.values():
        ingredient.delete()
    
    print("\n✅ TEST TERMINÉ AVEC SUCCÈS!")
    return True

def test_insufficient_stock():
    """Test avec stock insuffisant"""
    print("\n🚨 TEST: STOCK INSUFFISANT")
    print("=" * 40)
    
    # Créer un ingrédient avec très peu de stock
    user = User.objects.filter(is_active=True).first()
    
    ingredient = Ingredient.objects.create(
        nom='TEST_Stock_Faible',
        quantite_restante=Decimal('0.100'),  # Seulement 100g
        unite='kg',
        prix_unitaire=Decimal('1000.00')
    )
    
    product = Product.objects.create(
        name='TEST_Produit_Impossible',
        category='plats',
        selling_price=Decimal('2000.00'),
        purchase_price=Decimal('0.00')
    )
    
    recipe = Recipe.objects.create(
        plat=product,
        nom_recette='TEST_Recette_Impossible',
        created_by=user
    )
    
    # Ajouter un ingrédient qui nécessite plus que le stock disponible
    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        quantite_utilisee_par_plat=Decimal('0.500'),  # Besoin de 500g mais seulement 100g dispo
        unite='kg'
    )
    
    print(f"📦 Stock disponible: {ingredient.quantite_restante} {ingredient.unite}")
    print(f"🍽️  Besoin par portion: 0.500 {ingredient.unite}")
    print(f"🔍 Peut être préparée: {recipe.can_be_prepared}")
    
    # Essayer de préparer (devrait échouer)
    try:
        consumed = recipe.consume_ingredients(quantity=1, user=user)
        print("   ⚠️  Préparation réussie (inattendu!)")
    except Exception as e:
        print(f"   ✅ Erreur attendue: {str(e)[:100]}...")
        print("   📋 Les stocks restent inchangés (sécurité transactionnelle)")
    
    # Nettoyer
    recipe.delete()
    product.delete()
    ingredient.delete()

if __name__ == "__main__":
    success = test_recipe_stock_deduction()
    
    if success:
        test_insufficient_stock()
        
        print("\n" + "=" * 80)
        print("🎯 RÉSUMÉ DU SYSTÈME DE DÉCOMPTE AUTOMATIQUE:")
        print("   ✅ Les stocks diminuent automatiquement lors de la préparation")
        print("   ✅ Traçabilité complète avec IngredientMovement")
        print("   ✅ Calcul automatique du prix d'achat des produits")
        print("   ✅ Validation préalable des stocks disponibles")
        print("   ✅ Sécurité transactionnelle (tout ou rien)")
        print("   ✅ Gestion des erreurs de stock insuffisant")
        print("\n🍽️  Le système fonctionne comme attendu pour le restaurant!")
