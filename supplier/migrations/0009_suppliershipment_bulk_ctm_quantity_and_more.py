# Generated by Django 4.2.2 on 2023-11-18 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0008_remove_bulkctm_depot_remove_individualctm_depot'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliershipment',
            name='bulk_ctm_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='suppliershipment',
            name='individual_ctm_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]