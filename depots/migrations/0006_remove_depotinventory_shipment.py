# Generated by Django 4.2.2 on 2023-11-19 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('depots', '0005_depotinventory_shipment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depotinventory',
            name='shipment',
        ),
    ]
