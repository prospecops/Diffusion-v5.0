# Generated by Django 4.2.2 on 2023-11-01 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ctm_tracking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DepotClinicalSiteAssociation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinical_site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctm_tracking.clinicalsite')),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depots.depot')),
            ],
            options={
                'verbose_name': 'Depot Clinical Site Association',
                'verbose_name_plural': 'Depot Clinical Site Associations',
                'db_table': 'depots_depot_site_link',
                'unique_together': {('depot', 'clinical_site')},
            },
        ),
        migrations.AddField(
            model_name='depot',
            name='clinical_sites',
            field=models.ManyToManyField(blank=True, through='depots.DepotClinicalSiteAssociation', to='ctm_tracking.clinicalsite'),
        ),
    ]
