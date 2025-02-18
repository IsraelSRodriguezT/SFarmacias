# Generated by Django 5.1.5 on 2025-01-27 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0013_remove_medicamento_cantidad_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='esta_pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='venta',
            name='registro',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='Sistema.registro'),
        ),
    ]
