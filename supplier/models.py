from django.db import models


class SupplierPortal(models.Model):
    # Model fields here

    class Meta:
        permissions = [
            ("view_supplier_portal", "Can view supplier portal"),
        ]


class CTM(models.Model):
    CTM_TYPE_CHOICES = [
        ('Bulk', 'Bulk'),
        ('Individual', 'Individual'),
    ]
    ctm_type = models.CharField(max_length=10, choices=CTM_TYPE_CHOICES)
    device = models.CharField(max_length=200)
    lot_number = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    class Meta:
        abstract = True


class BulkCTM(CTM):
    depot = models.ForeignKey('depots.Depot', on_delete=models.CASCADE, null=True, blank=True, related_name="bulk_ctms")

    def __str__(self):
        return f"{self.device} - {self.lot_number}"

class IndividualCTM(CTM):
    kit_serial_number = models.CharField(max_length=100, unique=True)
    depot = models.ForeignKey('depots.Depot', on_delete=models.CASCADE, null=True, blank=True, related_name="individual_ctms")

    def __str__(self):
        return f"{self.device} - {self.kit_serial_number}"

