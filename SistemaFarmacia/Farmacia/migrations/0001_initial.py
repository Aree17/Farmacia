# Generated by Django 5.1.4 on 2025-01-27 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('salario', models.FloatField()),
                ('cargo', models.CharField(choices=[('EMPLEADO', 'Empleado'), ('ADMINISTRADOR', 'Administrador')], max_length=15)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Farmacia.farmacia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Farmacia.farmacia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_orden', models.PositiveIntegerField(unique=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('enviado', 'Enviado')], max_length=20, null=True)),
                ('tipo_entrega', models.CharField(choices=[('Retiro en origen', 'Retiro en origen'), ('Retiro en sucursal actual', 'Retiro en sucursal actual')], default='Retiro en origen', max_length=30)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Farmacia.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(unique=True)),
                ('fecha', models.DateField()),
                ('impuesto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('metodo_pago', models.CharField(choices=[('EFECTIVO', 'Efectivo'), ('TARJETA', 'Tarjeta')], max_length=20)),
                ('dinero_recibido', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TipoEntrega', models.CharField(choices=[('Retiro en origen', 'Retiro en origen'), ('Retiro en sucursal actual', 'Retiro en sucursal actual')], default='Retiro en origen', max_length=30)),
                ('cambio', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factura_list', to='Farmacia.cliente')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Farmacia.pedido')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('factura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_factura_list', to='Farmacia.factura')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Farmacia.pedido')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_factura_list', to='Farmacia.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(unique=True)),
                ('direccion', models.CharField(max_length=100)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sucursal_list', to='Farmacia.farmacia')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Farmacia.sucursal'),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=10, null=True, unique=True)),
                ('cantidad', models.PositiveIntegerField(default=0)),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventario_list', to='Farmacia.producto')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario_list', to='Farmacia.sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='sucursal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='factura_list', to='Farmacia.sucursal'),
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(unique=True)),
                ('fecha', models.DateField()),
                ('cantidad', models.PositiveIntegerField()),
                ('destino', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_destino', to='Farmacia.sucursal')),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Farmacia.empleado')),
                ('origen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_origen', to='Farmacia.sucursal')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencia_list', to='Farmacia.producto')),
            ],
        ),
    ]
