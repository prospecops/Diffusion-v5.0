# Generated by Django 4.2.2 on 2023-12-03 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0012_temporaryctminventory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temporaryctminventory',
            name='session_id',
        ),
        migrations.AddField(
            model_name='temporaryctminventory',
            name='page_session_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]