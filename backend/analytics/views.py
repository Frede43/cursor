from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from sales.models import Sale
from products.models import Product


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def sales_chart(request):
    """
    API pour les données du graphique des ventes par heure
    """
    period = request.GET.get('period', 'day')
    date_str = request.GET.get('date')
    
    if date_str:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        target_date = timezone.now().date()
    
    # Données mockées pour le développement
    # TODO: Remplacer par de vraies données de ventes
    mock_data = [
        {"time": "08:00", "sales": 15000},
        {"time": "10:00", "sales": 32000},
        {"time": "12:00", "sales": 45000},
        {"time": "14:00", "sales": 38000},
        {"time": "16:00", "sales": 52000},
        {"time": "18:00", "sales": 61000},
        {"time": "20:00", "sales": 75000},
        {"time": "22:00", "sales": 68000},
    ]
    
    return Response({
        'data': mock_data,
        'period': period,
        'date': target_date
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def product_sales_chart(request):
    """
    API pour les données du graphique de répartition des ventes par produit
    """
    period = request.GET.get('period', 'day')
    date_str = request.GET.get('date')
    
    if date_str:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        target_date = timezone.now().date()
    
    # Données mockées pour le développement
    # TODO: Calculer les vraies données depuis les ventes
    mock_data = [
        {"name": "Boissons", "value": 45},
        {"name": "Plats", "value": 30},
        {"name": "Snacks", "value": 25},
    ]
    
    return Response({
        'data': mock_data,
        'period': period,
        'date': target_date
    })
