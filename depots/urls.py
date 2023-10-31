from django.urls import path
from . import views

app_name = 'depots'

urlpatterns = [
    path('', views.depot_inventory, name='depot_inventory'),
    path('depot_shipments/', views.depot_shipments, name='depot_shipments'),
    path('returned_inventory/', views.returned_inventory, name='returned_inventory'),
]

