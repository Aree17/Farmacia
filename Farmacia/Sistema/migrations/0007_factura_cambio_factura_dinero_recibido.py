# Generated by Django 5.1.4 on 2025-01-26 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sistema', '0006_remove_pedido_sucursal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='cambio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='factura',
            name='dinero_recibido',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
