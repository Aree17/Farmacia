# Generated by Django 5.1.4 on 2025-01-30 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Farmacia', '0006_remove_factura_pedido_delete_itempedido'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pedido',
        ),
    ]
