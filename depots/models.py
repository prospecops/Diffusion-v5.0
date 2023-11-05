from django.contrib.auth.models import User
from django.db import models
from ctm_tracking.models import ClinicalSite


class Depot(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    clinical_sites = models.ManyToManyField(ClinicalSite, through='DepotClinicalSiteAssociation', blank=True)

    class Meta:
        permissions = [
            ("view_depot_portal", "Can view Depot Portal"),
        ]

    def __str__(self):
        return self.name


class DepotClinicalSiteAssociation(models.Model):
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    clinical_site = models.ForeignKey(ClinicalSite, on_delete=models.CASCADE)

    class Meta:
        db_table = 'depots_depot_site_link'
        unique_together = ['depot', 'clinical_site']
        verbose_name = 'Depot Clinical Site Association'
        verbose_name_plural = 'Depot Clinical Site Associations'

    def __str__(self):
        return f"{self.depot.name} - {self.clinical_site.name}"


class DepotInventory(models.Model):
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    bulk_ctm = models.ForeignKey('supplier.BulkCTM', on_delete=models.CASCADE, null=True, blank=True, related_name="bulk_ctm_inventory")  # Refers to the BulkCTM model in supplier
    individual_ctm = models.ForeignKey('supplier.IndividualCTM', on_delete=models.CASCADE, null=True, blank=True, related_name="individual_ctm_inventory")  # Refers to the IndividualCTM model in supplier
    quantity_received = models.PositiveIntegerField()

    def __str__(self):
        ctm_type = self.bulk_ctm if self.bulk_ctm else self.individual_ctm
        return f"{self.depot.name} - {ctm_type} - {self.quantity_received}"



