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
    # remove ctm_type field
    device = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    expiration_date = models.DateField()


class IndividualCTM(CTM):
    # remove ctm_type field
    device = models.CharField(max_length=100)
    kit_serial_number = models.CharField(max_length=100, unique=True) # combined field
    quantity = models.IntegerField(default=1)
    expiration_date = models.DateField()
    lot_number = models.CharField(max_length=100)

