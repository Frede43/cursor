#!/usr/bin/env python
"""
Script pour créer les endpoints manquants pour Kitchen, Reports et Analytics
"""

import os
import sys

def create_ingredients_model():
    """Créer le modèle Ingredient dans inventory"""
    print("🔧 CRÉATION MODÈLE INGREDIENT...")
    
    ingredient_model = '''
# Ajout du modèle Ingredient
class Ingredient(models.Model):
    """
    Modèle pour les ingrédients de cuisine
    """
    CATEGORIES = [
        ('vegetables', 'Légumes'),
        ('meat', 'Viande'),
        ('fish', 'Poisson'),
        ('dairy', 'Produits laitiers'),
        ('grains', 'Céréales'),
        ('spices', 'Épices'),
        ('beverages', 'Boissons'),
        ('other', 'Autre'),
    ]
    
    UNITS = [
        ('kg', 'Kilogramme'),
        ('g', 'Gramme'),
        ('l', 'Litre'),
        ('ml', 'Millilitre'),
        ('piece', 'Pièce'),
        ('pack', 'Paquet'),
    ]
    
    nom = models.CharField(
        max_length=100,
        verbose_name='Nom de l\'ingrédient'
    )
    
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='other',
        verbose_name='Catégorie'
    )
    
    quantite_restante = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Quantité restante'
    )
    
    unite_mesure = models.CharField(
        max_length=10,
        choices=UNITS,
        default='kg',
        verbose_name='Unité de mesure'
    )
    
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Prix unitaire (BIF)'
    )
    
    seuil_alerte = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Seuil d\'alerte'
    )
    
    fournisseur = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Fournisseur principal'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Dernière modification'
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif'
    )
    
    class Meta:
        verbose_name = 'Ingrédient'
        verbose_name_plural = 'Ingrédients'
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.quantite_restante} {self.unite_mesure})"
    
    @property
    def is_low_stock(self):
        """Vérifier si le stock est bas"""
        return self.quantite_restante <= self.seuil_alerte
    
    @property
    def stock_value(self):
        """Calculer la valeur du stock"""
        return self.quantite_restante * self.prix_unitaire
'''
    
    try:
        # Ajouter au fichier models.py
        with open('backend/inventory/models.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'class Ingredient' not in content:
            content += ingredient_model
            
            with open('backend/inventory/models.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Modèle Ingredient ajouté")
        else:
            print("✅ Modèle Ingredient déjà présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création modèle: {e}")
        return False

def create_ingredients_serializer():
    """Créer le serializer pour Ingredient"""
    print("\n🔧 CRÉATION SERIALIZER INGREDIENT...")
    
    serializer_code = '''
# Serializer pour Ingredient
class IngredientSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()
    stock_value = serializers.ReadOnlyField()
    fournisseur_nom = serializers.CharField(source='fournisseur.nom', read_only=True)
    
    class Meta:
        model = Ingredient
        fields = [
            'id', 'nom', 'categorie', 'quantite_restante', 'unite_mesure',
            'prix_unitaire', 'seuil_alerte', 'fournisseur', 'fournisseur_nom',
            'date_creation', 'date_modification', 'actif', 'is_low_stock', 'stock_value'
        ]
        read_only_fields = ['date_creation', 'date_modification']
'''
    
    try:
        with open('backend/inventory/serializers.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter l'import du modèle
        if 'from .models import' in content and 'Ingredient' not in content:
            content = content.replace(
                'from .models import',
                'from .models import Ingredient,'
            )
        
        if 'class IngredientSerializer' not in content:
            content += serializer_code
            
            with open('backend/inventory/serializers.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Serializer Ingredient ajouté")
        else:
            print("✅ Serializer Ingredient déjà présent")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création serializer: {e}")
        return False

def create_ingredients_views():
    """Créer les vues pour Ingredient"""
    print("\n🔧 CRÉATION VUES INGREDIENT...")
    
    views_code = '''
# Vues pour Ingredient
class IngredientViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des ingrédients
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_fields = ['categorie', 'actif', 'fournisseur']
    search_fields = ['nom', 'categorie']
    ordering_fields = ['nom', 'quantite_restante', 'prix_unitaire', 'date_creation']
    ordering = ['nom']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtrer par stock bas
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock and low_stock.lower() == 'true':
            queryset = queryset.filter(quantite_restante__lte=models.F('seuil_alerte'))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Obtenir les ingrédients en stock bas"""
        ingredients = self.get_queryset().filter(
            quantite_restante__lte=models.F('seuil_alerte')
        )
        serializer = self.get_serializer(ingredients, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stock_value(self, request):
        """Calculer la valeur totale du stock"""
        ingredients = self.get_queryset()
        total_value = sum(ing.stock_value for ing in ingredients)
        
        return Response({
            'total_value': total_value,
            'ingredients_count': ingredients.count(),
            'low_stock_count': ingredients.filter(
                quantite_restante__lte=models.F('seuil_alerte')
            ).count()
        })
    
    @action(detail=False, methods=['get'])
    def shopping_list(self, request):
        """Générer une liste de courses"""
        low_stock_ingredients = self.get_queryset().filter(
            quantite_restante__lte=models.F('seuil_alerte')
        )
        
        shopping_list = []
        for ingredient in low_stock_ingredients:
            quantity_needed = max(
                ingredient.seuil_alerte * 2 - ingredient.quantite_restante,
                ingredient.seuil_alerte
            )
            
            shopping_list.append({
                'ingredient': IngredientSerializer(ingredient).data,
                'quantity_needed': quantity_needed,
                'estimated_cost': quantity_needed * ingredient.prix_unitaire
            })
        
        total_cost = sum(item['estimated_cost'] for item in shopping_list)
        
        return Response({
            'items': shopping_list,
            'total_items': len(shopping_list),
            'estimated_total_cost': total_cost
        })
'''
    
    try:
        with open('backend/inventory/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter les imports nécessaires
        if 'from .models import' in content and 'Ingredient' not in content:
            content = content.replace(
                'from .models import',
                'from .models import Ingredient,'
            )
        
        if 'from .serializers import' in content and 'IngredientSerializer' not in content:
            content = content.replace(
                'from .serializers import',
                'from .serializers import IngredientSerializer,'
            )
        
        if 'class IngredientViewSet' not in content:
            content += views_code
            
            with open('backend/inventory/views.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Vues Ingredient ajoutées")
        else:
            print("✅ Vues Ingredient déjà présentes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création vues: {e}")
        return False

def update_inventory_urls():
    """Mettre à jour les URLs pour inclure les ingrédients"""
    print("\n🔧 MISE À JOUR URLS INVENTORY...")
    
    try:
        with open('backend/inventory/urls.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'ingredients' not in content:
            # Ajouter la route ingredients
            content = content.replace(
                "router.register(r'supplies', views.SupplyViewSet, basename='supply')",
                "router.register(r'supplies', views.SupplyViewSet, basename='supply')\n"
                "router.register(r'ingredients', views.IngredientViewSet)"
            )
            
            with open('backend/inventory/urls.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Route ingredients ajoutée")
        else:
            print("✅ Route ingredients déjà présente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour URLs: {e}")
        return False

def create_dashboard_stats_view():
    """Créer la vue dashboard stats"""
    print("\n🔧 CRÉATION VUE DASHBOARD STATS...")
    
    dashboard_view = '''
# Vue pour les statistiques du dashboard
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Statistiques générales du dashboard
    """
    try:
        from django.db.models import Sum, Count, Avg
        from django.utils import timezone
        from datetime import timedelta
        
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Statistiques des ventes
        from sales.models import Sale
        sales_today = Sale.objects.filter(date_created__date=today)
        sales_week = Sale.objects.filter(date_created__date__gte=week_ago)
        sales_month = Sale.objects.filter(date_created__date__gte=month_ago)
        
        # Statistiques des commandes
        from orders.models import Order
        orders_today = Order.objects.filter(created_at__date=today)
        orders_pending = Order.objects.filter(status='pending')
        
        # Statistiques des produits
        from products.models import Product
        products_count = Product.objects.filter(is_active=True).count()
        low_stock_products = Product.objects.filter(
            stock_quantity__lte=models.F('min_stock_level')
        ).count()
        
        # Statistiques des ingrédients (si disponible)
        try:
            from inventory.models import Ingredient
            ingredients_count = Ingredient.objects.filter(actif=True).count()
            low_stock_ingredients = Ingredient.objects.filter(
                quantite_restante__lte=models.F('seuil_alerte')
            ).count()
        except:
            ingredients_count = 0
            low_stock_ingredients = 0
        
        stats = {
            'sales': {
                'today_count': sales_today.count(),
                'today_total': sales_today.aggregate(total=Sum('total_amount'))['total'] or 0,
                'week_count': sales_week.count(),
                'week_total': sales_week.aggregate(total=Sum('total_amount'))['total'] or 0,
                'month_count': sales_month.count(),
                'month_total': sales_month.aggregate(total=Sum('total_amount'))['total'] or 0,
            },
            'orders': {
                'today_count': orders_today.count(),
                'pending_count': orders_pending.count(),
                'total_count': Order.objects.count(),
            },
            'inventory': {
                'products_count': products_count,
                'low_stock_products': low_stock_products,
                'ingredients_count': ingredients_count,
                'low_stock_ingredients': low_stock_ingredients,
            },
            'alerts': {
                'total_alerts': low_stock_products + low_stock_ingredients,
                'critical_alerts': low_stock_ingredients,
            }
        }
        
        return Response(stats)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors du calcul des statistiques: {str(e)}'},
            status=500
        )
'''
    
    try:
        # Ajouter à analytics/views.py
        with open('backend/analytics/views.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'dashboard_stats' not in content:
            # Ajouter les imports nécessaires
            if 'from rest_framework.decorators import api_view, permission_classes' not in content:
                content = "from rest_framework.decorators import api_view, permission_classes\n" + content
            if 'from rest_framework.permissions import IsAuthenticated' not in content:
                content = "from rest_framework.permissions import IsAuthenticated\n" + content
            if 'from rest_framework.response import Response' not in content:
                content = "from rest_framework.response import Response\n" + content
            if 'from django.db import models' not in content:
                content = "from django.db import models\n" + content
            
            content += dashboard_view
            
            with open('backend/analytics/views.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Vue dashboard_stats ajoutée")
        else:
            print("✅ Vue dashboard_stats déjà présente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création vue dashboard: {e}")
        return False

def update_analytics_urls():
    """Mettre à jour les URLs analytics"""
    print("\n🔧 MISE À JOUR URLS ANALYTICS...")
    
    urls_content = '''from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('overview/', views.analytics_overview, name='analytics-overview'),
    path('trends/', views.analytics_trends, name='analytics-trends'),
    path('products/', views.analytics_products, name='analytics-products'),
    path('predictions/', views.analytics_predictions, name='analytics-predictions'),
    path('goals/', views.performance_goals, name='performance-goals'),
]
'''
    
    try:
        with open('backend/analytics/urls.py', 'w', encoding='utf-8') as f:
            f.write(urls_content)
        
        print("✅ URLs analytics mises à jour")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour URLs analytics: {e}")
        return False
