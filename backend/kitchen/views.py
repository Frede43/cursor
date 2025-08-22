from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Ingredient, IngredientMovement, Recipe, RecipeIngredient
from .serializers import (
    IngredientSerializer, IngredientListSerializer, IngredientMovementSerializer,
    RecipeSerializer, RecipeListSerializer, RecipeCreateSerializer,
    RecipeIngredientSerializer, IngredientStockUpdateSerializer
)


class IngredientListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des ingrédients"""
    
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['unite', 'is_active', 'fournisseur']
    search_fields = ['nom', 'description']
    ordering_fields = ['nom', 'quantite_restante', 'seuil_alerte', 'date_maj']
    ordering = ['nom']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IngredientListSerializer
        return IngredientSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtres spéciaux
        status_filter = self.request.query_params.get('status')
        if status_filter == 'alerte':
            queryset = queryset.filter(quantite_restante__lte=F('seuil_alerte'))
        elif status_filter == 'rupture':
            queryset = queryset.filter(quantite_restante__lte=0)
        elif status_filter == 'ok':
            queryset = queryset.filter(quantite_restante__gt=F('seuil_alerte'))
        
        return queryset.select_related('fournisseur')


class IngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, modifier ou supprimer un ingrédient"""
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().select_related('fournisseur')


class IngredientMovementListView(generics.ListAPIView):
    """Vue pour lister les mouvements d'ingrédients"""
    
    serializer_class = IngredientMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ingredient', 'movement_type', 'reason', 'user']
    search_fields = ['ingredient__nom', 'notes', 'reference']
    ordering_fields = ['created_at', 'quantity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = IngredientMovement.objects.select_related(
            'ingredient', 'user', 'supplier'
        )
        
        # Filtrer par ingrédient si spécifié
        ingredient_id = self.request.query_params.get('ingredient_id')
        if ingredient_id:
            queryset = queryset.filter(ingredient_id=ingredient_id)
        
        # Filtrer par période
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__gte=date_from)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__lte=date_to)
            except ValueError:
                pass
        
        return queryset


class RecipeListCreateView(generics.ListCreateAPIView):
    """Vue pour lister et créer des recettes"""
    
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'plat__category']
    search_fields = ['nom_recette', 'plat__name', 'description']
    ordering_fields = ['nom_recette', 'total_cost', 'temps_preparation']
    ordering = ['nom_recette']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'plat', 'created_by'
        ).prefetch_related('ingredients__ingredient')
        
        # Filtres spéciaux
        status_filter = self.request.query_params.get('status')
        if status_filter == 'available':
            queryset = queryset.filter(can_be_prepared=True, is_active=True)
        elif status_filter == 'unavailable':
            queryset = queryset.filter(can_be_prepared=False, is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vue pour récupérer, modifier ou supprimer une recette"""
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'plat', 'created_by'
        ).prefetch_related('ingredients__ingredient')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_ingredient_stock(request, ingredient_id):
    """Vue pour mettre à jour le stock d'un ingrédient"""
    
    try:
        ingredient = Ingredient.objects.get(id=ingredient_id)
    except Ingredient.DoesNotExist:
        return Response(
            {'error': 'Ingrédient non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = IngredientStockUpdateSerializer(
        data=request.data,
        context={'ingredient': ingredient, 'request': request}
    )
    
    if serializer.is_valid():
        data = serializer.validated_data
        movement_type = data['movement_type']
        quantity = data['quantity']
        
        # Sauvegarder l'ancien stock
        old_stock = ingredient.quantite_restante
        
        # Calculer le nouveau stock
        if movement_type == 'in':
            new_stock = old_stock + quantity
        elif movement_type == 'out':
            new_stock = old_stock - quantity
        else:  # adjustment
            new_stock = quantity
        
        # Mettre à jour l'ingrédient
        ingredient.quantite_restante = new_stock
        ingredient.save()
        
        # Créer le mouvement
        movement = IngredientMovement.objects.create(
            ingredient=ingredient,
            movement_type=movement_type,
            reason=data['reason'],
            quantity=quantity,
            unit_price=data.get('unit_price'),
            stock_before=old_stock,
            stock_after=new_stock,
            supplier=data.get('supplier'),
            user=request.user,
            notes=data.get('notes', ''),
            reference=data.get('reference', '')
        )
        
        return Response({
            'message': 'Stock mis à jour avec succès',
            'ingredient': IngredientSerializer(ingredient).data,
            'movement': IngredientMovementSerializer(movement).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ingredients_alerts(request):
    """Vue pour récupérer les alertes de stock des ingrédients"""
    
    # Ingrédients en alerte
    low_stock = Ingredient.objects.filter(
        quantite_restante__lte=F('seuil_alerte'),
        quantite_restante__gt=0,
        is_active=True
    ).select_related('fournisseur')
    
    # Ingrédients en rupture
    out_of_stock = Ingredient.objects.filter(
        quantite_restante__lte=0,
        is_active=True
    ).select_related('fournisseur')
    
    return Response({
        'low_stock': IngredientListSerializer(low_stock, many=True).data,
        'out_of_stock': IngredientListSerializer(out_of_stock, many=True).data,
        'low_stock_count': low_stock.count(),
        'out_of_stock_count': out_of_stock.count()
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kitchen_dashboard(request):
    """Vue pour le tableau de bord de la cuisine"""

    try:
        # Statistiques générales
        total_ingredients = Ingredient.objects.filter(is_active=True).count()
        low_stock_count = Ingredient.objects.filter(
            quantite_restante__lte=F('seuil_alerte'),
            is_active=True
        ).count()
        out_of_stock_count = Ingredient.objects.filter(
            quantite_restante__lte=0,
            is_active=True
        ).count()

        # Valeur totale du stock
        total_stock_value = Ingredient.objects.filter(
            is_active=True
        ).aggregate(
            total=Sum(F('quantite_restante') * F('prix_unitaire'))
        )['total'] or Decimal('0.00')

        # Recettes disponibles/indisponibles
        total_recipes = Recipe.objects.filter(is_active=True).count()

        # Calculer les recettes disponibles manuellement car can_be_prepared est une propriété
        try:
            recipes = Recipe.objects.filter(is_active=True).prefetch_related('ingredients__ingredient')
            available_recipes = sum(1 for recipe in recipes if recipe.can_be_prepared)
        except Exception as e:
            # En cas d'erreur, on met 0 pour éviter le crash
            available_recipes = 0

        # Mouvements récents
        recent_movements = IngredientMovement.objects.select_related(
            'ingredient', 'user'
        ).order_by('-created_at')[:10]

        return Response({
            'stats': {
                'total_ingredients': total_ingredients,
                'low_stock_count': low_stock_count,
                'out_of_stock_count': out_of_stock_count,
                'total_stock_value': total_stock_value,
                'total_recipes': total_recipes,
                'available_recipes': available_recipes,
                'unavailable_recipes': total_recipes - available_recipes
            },
            'recent_movements': IngredientMovementSerializer(recent_movements, many=True).data
        })

    except Exception as e:
        # En cas d'erreur, retourner des données par défaut
        return Response({
            'stats': {
                'total_ingredients': 0,
                'low_stock_count': 0,
                'out_of_stock_count': 0,
                'total_stock_value': 0,
                'total_recipes': 0,
                'available_recipes': 0,
                'unavailable_recipes': 0
            },
            'recent_movements': [],
            'error': f'Erreur lors du chargement du dashboard: {str(e)}'
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_recipe_availability(request, recipe_id):
    """
    Vérifie si une recette peut être préparée (version améliorée pour recettes complexes)
    """

    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response(
            {'error': 'Recette non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )

    quantity = int(request.data.get('quantity', 1))

    # Utiliser la nouvelle méthode de validation complète
    validation_result = recipe.validate_ingredients_availability(quantity)

    return Response({
        'recipe_name': recipe.nom_recette,
        'quantity_requested': quantity,
        'can_prepare': validation_result['can_prepare'],
        'total_ingredients': validation_result['total_ingredients'],
        'available_ingredients_count': validation_result['available_count'],
        'missing_ingredients_count': validation_result['missing_count'],
        'available_ingredients': validation_result['available_ingredients'],
        'missing_ingredients': validation_result['missing_ingredients'],
        'estimated_cost': float(recipe.total_cost * quantity) if recipe.total_cost else 0,
        'complexity_level': 'simple' if validation_result['total_ingredients'] <= 5 else 'complex'
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def kitchen_report(request):
    """
    Rapport de cuisine pour une date donnée
    """
    from datetime import datetime, date

    # Récupérer la date (par défaut aujourd'hui)
    date_param = request.GET.get('date')
    if date_param:
        try:
            report_date = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            report_date = date.today()
    else:
        report_date = date.today()

    # Mouvements d'ingrédients du jour
    movements = IngredientMovement.objects.filter(
        created_at__date=report_date
    ).select_related('ingredient', 'user', 'supplier')

    # Statistiques des ingrédients
    ingredients_stats = []
    for ingredient in Ingredient.objects.filter(is_active=True):
        # Mouvements du jour pour cet ingrédient
        ingredient_movements = movements.filter(ingredient=ingredient)

        # Calculs
        total_in = ingredient_movements.filter(movement_type='in').aggregate(
            total=Sum('quantity')
        )['total'] or Decimal('0.000')

        total_out = ingredient_movements.filter(movement_type='out').aggregate(
            total=Sum('quantity')
        )['total'] or Decimal('0.000')

        # Stock initial (approximatif)
        initial_stock = ingredient.quantite_restante + total_out - total_in

        ingredients_stats.append({
            'id': ingredient.id,
            'nom': ingredient.nom,
            'unite': ingredient.unite,
            'stock_initial': float(initial_stock),
            'entrees': float(total_in),
            'sorties': float(total_out),
            'stock_final': float(ingredient.quantite_restante),
            'valeur_stock': float(ingredient.quantite_restante * ingredient.prix_unitaire),
            'prix_unitaire': float(ingredient.prix_unitaire),
            'seuil_alerte': float(ingredient.seuil_alerte),
            'status': 'rupture' if ingredient.is_out_of_stock else 'alerte' if ingredient.is_low_stock else 'ok'
        })

    # Recettes préparées (basé sur les mouvements de consommation)
    recipes_prepared = []
    consumption_movements = movements.filter(
        movement_type='out',
        reason='consumption'
    )

    # Grouper par recette (approximatif basé sur les notes)
    recipe_notes = consumption_movements.values_list('notes', flat=True).distinct()

    # Résumé général
    total_ingredients = Ingredient.objects.filter(is_active=True).count()
    total_stock_value = sum(stat['valeur_stock'] for stat in ingredients_stats)
    low_stock_count = len([s for s in ingredients_stats if s['status'] == 'alerte'])
    out_of_stock_count = len([s for s in ingredients_stats if s['status'] == 'rupture'])

    return Response({
        'date': report_date.isoformat(),
        'summary': {
            'total_ingredients': total_ingredients,
            'total_stock_value': total_stock_value,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'total_movements': movements.count(),
            'total_entries': movements.filter(movement_type='in').count(),
            'total_exits': movements.filter(movement_type='out').count()
        },
        'ingredients': ingredients_stats,
        'movements': IngredientMovementSerializer(movements, many=True).data,
        'recipes_prepared': recipes_prepared
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def validate_multiple_recipes(request):
    """
    Valide la disponibilité pour plusieurs recettes simultanément
    Utile pour les commandes complexes avec plusieurs plats
    """

    recipes_data = request.data.get('recipes', [])
    if not recipes_data:
        return Response(
            {'error': 'Aucune recette spécifiée'},
            status=status.HTTP_400_BAD_REQUEST
        )

    results = []
    global_ingredients_needed = {}

    # 1. Calculer les besoins totaux en ingrédients
    for recipe_data in recipes_data:
        try:
            recipe = Recipe.objects.get(id=recipe_data['recipe_id'])
            quantity = int(recipe_data.get('quantity', 1))

            validation_result = recipe.validate_ingredients_availability(quantity)

            # Accumuler les besoins en ingrédients
            for ingredient_info in validation_result['available_ingredients'] + validation_result['missing_ingredients']:
                ingredient_name = ingredient_info['name']
                needed = ingredient_info['needed']

                if ingredient_name in global_ingredients_needed:
                    global_ingredients_needed[ingredient_name]['total_needed'] += needed
                else:
                    global_ingredients_needed[ingredient_name] = {
                        'total_needed': needed,
                        'available': ingredient_info['available'],
                        'unit': ingredient_info['unit']
                    }

            results.append({
                'recipe_id': recipe.id,
                'recipe_name': recipe.nom_recette,
                'quantity': quantity,
                'can_prepare_individually': validation_result['can_prepare'],
                'ingredients_count': validation_result['total_ingredients'],
                'missing_ingredients': validation_result['missing_ingredients']
            })

        except Recipe.DoesNotExist:
            results.append({
                'recipe_id': recipe_data['recipe_id'],
                'error': 'Recette non trouvée'
            })

    # 2. Vérifier la faisabilité globale
    global_missing = []
    can_prepare_all = True

    for ingredient_name, info in global_ingredients_needed.items():
        if info['total_needed'] > info['available']:
            can_prepare_all = False
            global_missing.append({
                'ingredient': ingredient_name,
                'total_needed': info['total_needed'],
                'available': info['available'],
                'shortage': info['total_needed'] - info['available'],
                'unit': info['unit']
            })

    return Response({
        'can_prepare_all': can_prepare_all,
        'recipes_count': len(recipes_data),
        'individual_results': results,
        'global_ingredients_needed': global_ingredients_needed,
        'global_missing_ingredients': global_missing,
        'recommendation': 'Commande possible' if can_prepare_all else 'Réapprovisionnement nécessaire'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def recalculate_all_purchase_prices(request):
    """
    Recalcule automatiquement tous les prix d'achat des produits
    basés sur le coût total des ingrédients de leurs recettes

    Exemple: Riz au Poulet
    - Riz: 300 FBU + Poulet: 2000 FBU + Huile: 200 FBU + Épices: 500 FBU = 3000 FBU
    - Le produit "Riz au Poulet" aura automatiquement purchase_price = 3000 FBU
    """
    try:
        recipes = Recipe.objects.filter(is_active=True).select_related('plat')
        updated_products = []

        for recipe in recipes:
            if recipe.plat:
                # Calculer le coût total des ingrédients
                total_cost = recipe.total_cost
                old_price = recipe.plat.purchase_price

                # Mettre à jour le prix d'achat
                recipe.plat.purchase_price = total_cost
                recipe.plat.save(update_fields=['purchase_price'])

                # Calculer le bénéfice unitaire
                selling_price = recipe.plat.selling_price or 0
                profit = selling_price - total_cost
                profit_margin = (profit / selling_price * 100) if selling_price > 0 else 0

                updated_products.append({
                    'product_id': recipe.plat.id,
                    'product_name': recipe.plat.name,
                    'recipe_name': recipe.nom_recette,
                    'old_purchase_price': float(old_price),
                    'new_purchase_price': float(total_cost),
                    'selling_price': float(selling_price),
                    'profit_per_unit': float(profit),
                    'profit_margin_percent': float(profit_margin),
                    'ingredients_detail': [
                        {
                            'ingredient': ing.ingredient.nom,
                            'quantity': float(ing.quantite_utilisee_par_plat),
                            'unit': ing.unite,
                            'unit_price': float(ing.ingredient.prix_unitaire),
                            'total_cost': float(ing.cost_per_portion)
                        }
                        for ing in recipe.ingredients.all()
                    ]
                })

        return Response({
            'success': True,
            'message': f'{len(updated_products)} produits mis à jour',
            'updated_products': updated_products,
            'summary': {
                'total_recipes_processed': len(recipes),
                'products_updated': len(updated_products),
                'total_ingredients_cost': sum(p['new_purchase_price'] for p in updated_products),
                'total_selling_value': sum(p['selling_price'] for p in updated_products),
                'total_potential_profit': sum(p['profit_per_unit'] for p in updated_products)
            }
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
