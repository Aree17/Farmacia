# Generated by Django 5.1.4 on 2025-01-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Farmacia', '0003_remove_cliente_farmacia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='telefono',
        ),
        migrations.AddField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='cedula',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
