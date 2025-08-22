from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Graphiques et analytics
    path('sales-chart/', views.sales_chart, name='sales_chart'),
    path('product-sales/', views.product_sales_chart, name='product_sales_chart'),
]
