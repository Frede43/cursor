from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Tables - Gestion de base
    path('tables/', views.TableListCreateView.as_view(), name='table_list_create'),
    path('tables/<int:pk>/', views.TableDetailView.as_view(), name='table_detail'),

    # Tables - Nouvelles fonctionnalités
    path('tables/list/', views.TableListView.as_view(), name='table_list'),
    path('tables/<int:table_id>/occupy/', views.occupy_table, name='occupy_table'),
    path('tables/<int:table_id>/free/', views.free_table, name='free_table'),
    path('tables/status-summary/', views.table_status_summary, name='table_status_summary'),
    path('tables/available/', views.available_tables, name='available_tables'),
    path('tables/analytics/', views.table_analytics, name='table_analytics'),

    # Réservations
    path('reservations/', views.TableReservationListCreateView.as_view(), name='reservation_list_create'),
    path('reservations/<int:pk>/', views.TableReservationDetailView.as_view(), name='reservation_detail'),
    path('reservations/<int:reservation_id>/confirm/', views.confirm_reservation, name='confirm_reservation'),
    path('reservations/<int:reservation_id>/seat/', views.seat_reservation, name='seat_reservation'),
    path('reservations/today/', views.todays_reservations, name='todays_reservations'),
    path('reservations/upcoming/', views.upcoming_reservations, name='upcoming_reservations'),

    # Ventes
    path('', views.SaleListCreateView.as_view(), name='sale_list_create'),
    path('<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('<int:pk>/update-status/', views.update_sale_status, name='update_status'),
    path('<int:pk>/cancel/', views.cancel_sale, name='cancel_sale'),
    path('<int:sale_id>/mark-paid/', views.mark_sale_as_paid, name='mark_sale_as_paid'),
    path('<int:pk>/invoice/', views.generate_invoice, name='generate_invoice'),

    # Statistiques et rapports
    path('statistics/', views.sales_statistics, name='statistics'),
    path('stats/', views.sales_stats, name='sales_stats'),
    path('daily-report/', views.daily_sales_report, name='daily_report'),
]
