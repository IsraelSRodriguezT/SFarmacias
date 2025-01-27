# Generated by Django 5.1.5 on 2025-01-27 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0007_pedido_traer_de_otra_sucursal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='es_para_retirar',
        ),
        migrations.AddField(
            model_name='pedido',
            name='sucursal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Sistema.sucursal'),
            preserve_default=False,
        ),
    ]
