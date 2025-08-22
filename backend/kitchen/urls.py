from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Pas de router pour cette app, on utilise des vues basées sur les classes

urlpatterns = [
    # Ingrédients
    path('ingredients/', views.IngredientListCreateView.as_view(), name='ingredient-list-create'),
    path('ingredients/<int:pk>/', views.IngredientDetailView.as_view(), name='ingredient-detail'),
    path('ingredients/<int:ingredient_id>/update-stock/', views.update_ingredient_stock, name='ingredient-update-stock'),
    
    # Mouvements d'ingrédients
    path('ingredient-movements/', views.IngredientMovementListView.as_view(), name='ingredient-movement-list'),
    
    # Recettes
    path('recipes/', views.RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/<int:recipe_id>/check-availability/', views.check_recipe_availability, name='recipe-check-availability'),
    path('recipes/validate-multiple/', views.validate_multiple_recipes, name='validate-multiple-recipes'),
    
    # Alertes et tableau de bord
    path('alerts/', views.ingredients_alerts, name='ingredients-alerts'),
    path('dashboard/', views.kitchen_dashboard, name='kitchen-dashboard'),
    path('report/', views.kitchen_report, name='kitchen-report'),

    # Calcul automatique des prix d'achat
    path('recalculate-purchase-prices/', views.recalculate_all_purchase_prices, name='recalculate-purchase-prices'),
]
