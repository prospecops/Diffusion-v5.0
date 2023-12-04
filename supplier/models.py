import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

class SupplierShipment(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Shipped', 'Shipped'),
        # Additional statuses can be added as needed.
    ]

    # Primary key 'id' is automatically added by Django

    depot = models.ForeignKey('depots.Depot', on_delete=models.CASCADE)  # Link to Depot model
    shipment_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    individual_ctm = models.ForeignKey('IndividualCTM', on_delete=models.SET_NULL, null=True, blank=True)
    individual_ctm_quantity = models.PositiveIntegerField(default=0)  # Quantity for individual CTM
    bulk_ctm = models.ForeignKey('BulkCTM', on_delete=models.SET_NULL, null=True, blank=True)
    bulk_ctm_quantity = models.PositiveIntegerField(default=0)  # Quantity for bulk CTM
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Shipment {self.shipment_id} - {self.status}"

    def save(self, *args, **kwargs):
        # Update the depot inventory before saving the shipment record
        if self.status == 'Shipped':
            self.update_depot_inventory()
        super(SupplierShipment, self).save(*args, **kwargs)

    def update_depot_inventory(self):
        # Logic to update inventory at the depot
        # Implement this method based on your application's specific needs
        pass

    class Meta:
        permissions = [
            ("view_supplier_shipment", "Can view supplier shipments"),
        ]


class CTM(models.Model):
    CTM_TYPE_CHOICES = [
        ('Bulk', 'Bulk'),
        ('Individual', 'Individual'),
    ]
    ctm_type = models.CharField(max_length=10, choices=CTM_TYPE_CHOICES)
    ctm_name = models.CharField(max_length=200)
    lot_number = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()

    class Meta:
        abstract = True


class BulkCTM(CTM):
    # Removed the depot field
    def __str__(self):
        return f"{self.ctm_name} - {self.lot_number}"


class IndividualCTM(CTM):
    kit_serial_number = models.CharField(max_length=100, unique=True)

    # Removed the depot field
    def __str__(self):
        return f"{self.ctm_name} - {self.kit_serial_number}"


class CTMInventory(models.Model):
    CTM_TYPE_CHOICES = [
        ('Bulk', 'Bulk'),
        ('Individual', 'Individual'),
    ]

    ctm_type = models.CharField(max_length=10, choices=CTM_TYPE_CHOICES)
    ctm_name = models.CharField(max_length=200)
    lot_number = models.CharField(max_length=200)
    expiration_date = models.DateField()
    kit_serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    bulk_batch_id = models.IntegerField(null=True, blank=True)
    bulk_ctm_identifier = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.ctm_type == 'Individual':
            return f"Individual: {self.ctm_name} - Serial: {self.kit_serial_number} - Lot: {self.lot_number} - Exp: {self.expiration_date}"
        else:
            return f"Bulk: {self.ctm_name} - Lot: {self.lot_number} - Exp: {self.expiration_date}"


class TemporaryCTMInventory(models.Model):
    # Page session identifier
    page_session_id = models.UUIDField(default=uuid.uuid4)

    # Fields similar to CTMInventory
    CTM_TYPE_CHOICES = [
        ('Bulk', 'Bulk'),
        ('Individual', 'Individual'),
    ]

    ctm_type = models.CharField(max_length=10, choices=CTM_TYPE_CHOICES)
    ctm_name = models.CharField(max_length=200)
    lot_number = models.CharField(max_length=200)
    expiration_date = models.DateField()
    kit_serial_number = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    # Additional fields for tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ctm_type}: {self.ctm_name} - Lot: {self.lot_number} - Exp: {self.expiration_date}"

    def clean(self):
        # Ensure expiration date is in the future
        if self.expiration_date <= date.today():
            raise ValidationError(_('Expiration date must be in the future.'))

        # Quantity validation
        if self.ctm_type == 'Individual' and self.quantity != 1:
            raise ValidationError(_('Quantity for Individual CTM must be 1.'))
        elif self.ctm_type == 'Bulk' and not (1 <= self.quantity <= 10000):
            raise ValidationError(_('Quantity for Bulk CTM must be between 1 and 10,000.'))

        # Kit serial number validation for Individual CTM
        if self.ctm_type == 'Individual':
            if not self.kit_serial_number.isdigit():
                raise ValidationError(_('Kit serial number must be numeric.'))
            if TemporaryCTMInventory.objects.filter(kit_serial_number=self.kit_serial_number).exists() or \
               CTMInventory.objects.filter(kit_serial_number=self.kit_serial_number).exists():
                raise ValidationError(_('Kit serial number must be unique across Temporary and main CTM inventories.'))
        elif self.ctm_type == 'Bulk' and self.kit_serial_number:
            raise ValidationError(_('Kit serial number should not be set for Bulk CTM.'))

    class Meta:
        verbose_name = "Temporary CTM Inventory"
        verbose_name_plural = "Temporary CTM Inventories"
