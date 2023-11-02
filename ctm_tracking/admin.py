from django.contrib import admin
from .models import ClinicalSite

@admin.register(ClinicalSite)
class ClinicalSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)

