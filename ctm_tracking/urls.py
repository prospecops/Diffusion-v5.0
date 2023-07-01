from django.urls import path
from . import views

app_name = 'ctm_tracking'
urlpatterns = [
    path('', views.ctm_tracking_home, name='ctm_tracking_home'),
    path('drug_inventory/', views.drug_inventory, name='drug_inventory'),
    path('drug_shipments/', views.drug_shipments, name='drug_shipments'),
    path('drug_request/', views.drug_request, name='drug_request'),
    path('accountability/', views.accountability, name='accountability'),
    path('final_disposition/', views.final_disposition, name='final_disposition'),
]
