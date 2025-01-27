from django.contrib import admin
from .models import (
    Farmacia, Empleado, Cliente, Sucursal, Inventario, Producto, Pedido, ItemPedido, Transferencia, Factura, ProductoInventario
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
    list_display = ('nombre', 'farmacia')
    search_fields = ('nombre',)
    list_filter = ('nombre', 'farmacia')

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
    list_display = ('nombre', 'inventario', 'precio',)
    search_fields = ('nombre',)
    list_filter = ('nombre', 'inventario',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'fecha', 'estado', 'sucursal',)
    search_fields = ('numero_orden', 'fecha',)
    list_filter = ('numero_orden', 'fecha',)

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('producto_inventario','cantidad', 'subtotal')
    search_fields = ('cantidad', 'subtotal')
    list_filter = ('cantidad', 'subtotal')

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('fecha','origen', 'destino', 'producto', 'cantidad', 'completada')
    search_fields = ('fecha',)
    list_filter = ('fecha', 'origen', 'destino')

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'numero', 'cliente', 'empleado', 'impuesto', 'descuento', 'subtotal','total',)
    search_fields = ('fecha', 'numero',)
    list_filter = ('fecha', 'numero','cliente',)

@admin.register(ProductoInventario)
class ProductoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'inventario', 'cantidad_disponible')
    search_fields = ('cantidad_disponible',)
    list_filter = ('producto', 'inventario', 'cantidad_disponible')

