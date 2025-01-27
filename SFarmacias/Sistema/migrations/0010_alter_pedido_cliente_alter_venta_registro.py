# Generated by Django 5.1.5 on 2025-01-27 09:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0009_alter_pedido_traer_de_otra_sucursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='Sistema.cliente'),
        ),
        migrations.AlterField(
            model_name='venta',
            name='registro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ventas', to='Sistema.registro'),
        ),
    ]
