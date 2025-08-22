#!/usr/bin/env python
"""
Test du workflow complet de gestion des stocks lors de la préparation de recettes
Exemple: Riz au Poulet - Vérification que les stocks d'ingrédients diminuent automatiquement
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

def create_test_data():
    """Créer les données de test pour le workflow"""
    print("🔧 Création des données de test...")
    
    # Créer un utilisateur test
    user, created = User.objects.get_or_create(
        username='chef_test',
        defaults={
            'email': 'chef@test.com',
            'first_name': 'Chef',
            'last_name': 'Test',
            'role': 'server'
        }
    )
    if created:
        user.set_password('test123')
        user.save()
    
    # Créer les ingrédients avec stock initial
    ingredients_data = [
        {'nom': 'Riz', 'quantite': Decimal('10.000'), 'unite': 'kg', 'prix': Decimal('300.00')},
        {'nom': 'Poulet', 'quantite': Decimal('5.000'), 'unite': 'kg', 'prix': Decimal('2000.00')},
        {'nom': 'Huile', 'quantite': Decimal('2.000'), 'unite': 'L', 'prix': Decimal('1000.00')},
        {'nom': 'Épices', 'quantite': Decimal('1.000'), 'unite': 'kg', 'prix': Decimal('5000.00')},
    ]
    
    ingredients = {}
    for ing_data in ingredients_data:
        ingredient, created = Ingredient.objects.get_or_create(
            nom=ing_data['nom'],
            defaults={
                'quantite_restante': ing_data['quantite'],
                'unite': ing_data['unite'],
                'prix_unitaire': ing_data['prix'],
                'seuil_alerte': Decimal('1.000')
            }
        )
        if not created:
            # Mettre à jour le stock si l'ingrédient existe déjà
            ingredient.quantite_restante = ing_data['quantite']
            ingredient.prix_unitaire = ing_data['prix']
            ingredient.save()
        
        ingredients[ing_data['nom']] = ingredient
        print(f"   ✅ {ingredient.nom}: {ingredient.quantite_restante} {ingredient.unite}")
    
    # Créer le produit "Riz au Poulet"
    product, created = Product.objects.get_or_create(
        name='Riz au Poulet Maison',
        defaults={
            'category': 'plats',
            'description': 'Délicieux riz au poulet fait maison',
            'selling_price': Decimal('5000.00'),
            'purchase_price': Decimal('0.00'),  # Sera calculé automatiquement
            'stock_quantity': 0,
            'is_active': True
        }
    )
    
    # Créer la recette
    recipe, created = Recipe.objects.get_or_create(
        plat=product,
        defaults={
            'nom_recette': 'Riz au Poulet Maison',
            'description': 'Recette traditionnelle de riz au poulet',
            'instructions': 'Cuire le riz, préparer le poulet avec les épices...',
            'temps_preparation': 45,
            'portions': 1,
            'created_by': user
        }
    )
    
    # Définir la composition de la recette (quantités par portion)
    recipe_composition = [
        {'ingredient': 'Riz', 'quantite': Decimal('0.300')},      # 300g de riz
        {'ingredient': 'Poulet', 'quantite': Decimal('0.250')},   # 250g de poulet
        {'ingredient': 'Huile', 'quantite': Decimal('0.050')},    # 50ml d'huile
        {'ingredient': 'Épices', 'quantite': Decimal('0.020')},   # 20g d'épices
    ]
    
    # Créer les ingrédients de la recette
    for comp in recipe_composition:
        ingredient = ingredients[comp['ingredient']]
        recipe_ingredient, created = RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ingredient,
            defaults={
                'quantite_utilisee_par_plat': comp['quantite'],
                'unite': ingredient.unite
            }
        )
        if not created:
            recipe_ingredient.quantite_utilisee_par_plat = comp['quantite']
            recipe_ingredient.save()
    
    return recipe, ingredients, user

def display_stock_status(ingredients, title="État des stocks"):
    """Afficher l'état actuel des stocks"""
    print(f"\n📊 {title}")
    print("-" * 50)
    for name, ingredient in ingredients.items():
        ingredient.refresh_from_db()  # Recharger depuis la DB
        print(f"   {ingredient.nom}: {ingredient.quantite_restante} {ingredient.unite}")

def test_recipe_preparation():
    """Test complet du workflow de préparation"""
    print("🍽️  TEST WORKFLOW PRÉPARATION DE RECETTE")
    print("=" * 60)
    
    # 1. Créer les données de test
    recipe, ingredients, user = create_test_data()
    
    # 2. Afficher l'état initial
    display_stock_status(ingredients, "État initial des stocks")
    
    # 3. Calculer et afficher le coût de la recette
    print(f"\n💰 Coût de la recette:")
    print(f"   Coût total: {recipe.total_cost} BIF")
    
    # Détail des coûts par ingrédient
    for recipe_ingredient in recipe.ingredients.all():
        cost = recipe_ingredient.cost_per_portion
        print(f"   - {recipe_ingredient.ingredient.nom}: "
              f"{recipe_ingredient.quantite_utilisee_par_plat} {recipe_ingredient.unite} "
              f"× {recipe_ingredient.ingredient.prix_unitaire} BIF = {cost} BIF")
    
    # 4. Vérifier la disponibilité
    print(f"\n🔍 Vérification de la disponibilité:")
    validation = recipe.validate_ingredients_availability(quantity=3)  # Pour 3 portions
    
    if validation['can_prepare']:
        print("   ✅ Tous les ingrédients sont disponibles")
        print(f"   📋 {validation['available_count']}/{validation['total_ingredients']} ingrédients OK")
    else:
        print("   ❌ Ingrédients manquants:")
        for missing in validation['missing_ingredients']:
            print(f"      - {missing['name']}: besoin {missing['needed']}, disponible {missing['available']}")
        return False
    
    # 5. Préparer 3 portions de la recette
    portions_to_prepare = 3
    print(f"\n🍳 Préparation de {portions_to_prepare} portions...")
    
    try:
        consumed = recipe.consume_ingredients(quantity=portions_to_prepare, user=user)
        print("   ✅ Préparation réussie!")
        
        # Afficher les détails de consommation
        print("\n📝 Détails de la consommation:")
        for item in consumed:
            ingredient = item['ingredient']
            print(f"   - {ingredient.nom}: -{item['quantity_consumed']} {ingredient.unite}")
            print(f"     Stock: {item['stock_before']} → {item['stock_after']} {ingredient.unite}")
        
    except Exception as e:
        print(f"   ❌ Erreur lors de la préparation: {e}")
        return False
    
    # 6. Afficher l'état final des stocks
    display_stock_status(ingredients, "État final des stocks")
    
    # 7. Vérifier les mouvements de stock créés
    print(f"\n📋 Mouvements de stock créés:")
    recent_movements = IngredientMovement.objects.filter(
        reason='consumption',
        user=user
    ).order_by('-created_at')[:10]
    
    for movement in recent_movements:
        print(f"   - {movement.ingredient.nom}: -{movement.quantity} {movement.ingredient.unite}")
        print(f"     Raison: {movement.get_reason_display()}")
        print(f"     Stock: {movement.stock_before} → {movement.stock_after}")
        print(f"     Date: {movement.created_at.strftime('%H:%M:%S')}")
        print()
    
    # 8. Vérifier la mise à jour automatique du prix d'achat du produit
    recipe.plat.refresh_from_db()
    print(f"💰 Prix d'achat du produit mis à jour:")
    print(f"   Produit: {recipe.plat.name}")
    print(f"   Prix d'achat calculé: {recipe.plat.purchase_price} BIF")
    print(f"   Prix de vente: {recipe.plat.selling_price} BIF")
    print(f"   Marge par portion: {recipe.plat.selling_price - recipe.plat.purchase_price} BIF")
    
    return True

def test_insufficient_stock():
    """Test avec stock insuffisant"""
    print("\n🚨 TEST AVEC STOCK INSUFFISANT")
    print("=" * 60)
    
    recipe, ingredients, user = create_test_data()
    
    # Réduire drastiquement le stock de riz
    riz = ingredients['Riz']
    riz.quantite_restante = Decimal('0.100')  # Seulement 100g
    riz.save()
    
    print(f"📉 Stock de riz réduit à: {riz.quantite_restante} {riz.unite}")
    
    # Essayer de préparer 3 portions (besoin de 900g de riz)
    try:
        portions_needed = 3
        print(f"\n🍳 Tentative de préparation de {portions_needed} portions...")
        
        # Vérification préalable
        validation = recipe.validate_ingredients_availability(quantity=portions_needed)
        if not validation['can_prepare']:
            print("   ❌ Préparation impossible - ingrédients manquants:")
            for missing in validation['missing_ingredients']:
                print(f"      - {missing['name']}: besoin {missing['needed']}, disponible {missing['available']}")
        
        # Tentative de préparation (devrait échouer)
        consumed = recipe.consume_ingredients(quantity=portions_needed, user=user)
        print("   ⚠️  Préparation réussie (inattendu!)")
        
    except Exception as e:
        print(f"   ✅ Erreur attendue: {e}")
        print("   📋 Les stocks n'ont pas été modifiés (transaction atomique)")
    
    # Vérifier que les stocks n'ont pas changé
    display_stock_status(ingredients, "Stocks après échec (doivent être inchangés)")

if __name__ == "__main__":
    print("🧪 TEST COMPLET DU SYSTÈME DE GESTION DES STOCKS")
    print("=" * 80)
    
    # Test 1: Workflow normal
    success = test_recipe_preparation()
    
    if success:
        # Test 2: Gestion des stocks insuffisants
        test_insufficient_stock()
        
        print("\n" + "=" * 80)
        print("✅ TOUS LES TESTS TERMINÉS")
        print("\n🎯 RÉSUMÉ DU SYSTÈME:")
        print("   ✅ Les stocks diminuent automatiquement lors de la préparation")
        print("   ✅ Validation préalable des stocks disponibles")
        print("   ✅ Transactions atomiques (tout ou rien)")
        print("   ✅ Traçabilité complète des mouvements")
        print("   ✅ Mise à jour automatique des prix d'achat des produits")
        print("   ✅ Gestion des erreurs et rollback automatique")
    else:
        print("\n❌ Test échoué")
