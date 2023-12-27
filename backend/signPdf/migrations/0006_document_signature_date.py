# Generated by Django 5.0 on 2023-12-26 23:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signPdf', '0005_alter_document_document_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='signature_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
