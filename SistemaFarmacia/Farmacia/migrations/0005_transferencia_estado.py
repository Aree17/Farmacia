# Generated by Django 5.1.4 on 2025-01-27 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farmacia', '0004_remove_cliente_apellido_remove_cliente_correo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferencia',
            name='estado',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADA', 'Completada'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=20),
        ),
    ]
