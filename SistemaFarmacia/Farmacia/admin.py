from django.contrib import admin
from .models import (
    Farmacia, Empleado, Cliente, Sucursal, Inventario, Producto, Transferencia, Factura
)

@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion', 'telefono')
    list_filter = ('nombre', 'direccion', 'telefono')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'salario', 'cargo', 'farmacia',)
    search_fields = ('nombre', 'salario', 'cargo',)
    list_filter = ('nombre', 'salario', 'cargo',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('numero', 'direccion', 'farmacia')
    search_fields = ('numero', 'direccion',)
    list_filter = ('numero', 'direccion', 'farmacia')

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('sucursal','codigo',)
    search_fields = ('codigo',)
    list_filter = ('sucursal',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio',)
    search_fields = ('nombre',)
    list_filter = ('nombre',)

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('fecha','origen', 'destino', 'producto', 'cantidad',)
    search_fields = ('fecha',)
    list_filter = ('fecha', 'origen', 'destino')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'numero', 'cliente', 'impuesto', 'descuento', 'subtotal','total',)
    search_fields = ('fecha', 'numero',)
    list_filter = ('fecha', 'numero','cliente',)


