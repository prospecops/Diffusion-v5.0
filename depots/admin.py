from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Depot, DepotClinicalSiteAssociation


class DepotClinicalSiteAssociationInline(admin.TabularInline):
    model = DepotClinicalSiteAssociation
    extra = 1


@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'user')
    search_fields = ('name', 'user__username')  # Allow searching by user's username
    inlines = [DepotClinicalSiteAssociationInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            depot_user_group = Group.objects.get(name="Depot User")
            kwargs["queryset"] = depot_user_group.user_set.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(DepotClinicalSiteAssociation)
