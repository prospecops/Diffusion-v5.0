"""
URL configuration for user_registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Django allauth urls
    path('', include('registration.urls')),  # Include your registration app urls here
    path('core/', include('core.urls')),  # Include your core app urls here
    path('ctm_tracking/', include('ctm_tracking.urls')),  # Include your ctm_tracking app urls here
    path('supplier/', include('supplier.urls')),  # Include your supplier app urls here
]




