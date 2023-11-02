from django.db import models


class ClinicalSite(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    class Meta:
        permissions = [
            ("view_ctm_tracking_portal", "Can view CTM Tracking Portal"),
        ]

    def __str__(self):
        return self.name
