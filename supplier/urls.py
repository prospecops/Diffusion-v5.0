from django.urls import path

from . import views
from .views import add_ctm, CTMListView

app_name = "supplier"
urlpatterns = [
    path('portal/', views.supplier_portal, name='supplier_portal'),
    path('add_ctm/', add_ctm, name='add_ctm'),
    path('ctm_list/', CTMListView.as_view(), name='ctm_list'),  # Add this line
]
