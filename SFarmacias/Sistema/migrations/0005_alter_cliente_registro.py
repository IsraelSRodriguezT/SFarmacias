# Generated by Django 5.1.5 on 2025-01-26 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0004_cliente_registro_alter_sucursal_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='registro',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='Sistema.registro'),
        ),
    ]
