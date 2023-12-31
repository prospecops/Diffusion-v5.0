from django.urls import path

from . import views
from .views import create_inventory, supplier_inventory, depot_inventory_shipments

app_name = "supplier"
urlpatterns = [
    path('create_inventory/', create_inventory, name='create_inventory'),
    path('process_ctm_entries/', views.process_ctm_entries, name='process_ctm_entries'),
    path('cleanup_sessions/', views.cleanup_sessions, name='cleanup_sessions'),
    path('supplier_inventory/', supplier_inventory, name='supplier_inventory'),
    path('depot_inventory_shipments/', depot_inventory_shipments, name='depot_inventory_shipments'),
    path('returned_inventory/', views.returned_inventory, name='returned_inventory'),
]
