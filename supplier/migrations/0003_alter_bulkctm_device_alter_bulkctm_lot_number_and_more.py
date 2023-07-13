# Generated by Django 4.2.2 on 2023-07-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_bulkctm_individualctm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bulkctm',
            name='device',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bulkctm',
            name='lot_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='bulkctm',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='individualctm',
            name='device',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='individualctm',
            name='kit_serial_number',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='individualctm',
            name='lot_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='individualctm',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
