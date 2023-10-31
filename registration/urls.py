from django.urls import path, include

from. import views

app_name = 'registration'
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('account/', include(('allauth.urls', 'allauth'), namespace='account')),
]

