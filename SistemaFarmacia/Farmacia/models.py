from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

class Farmacia(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True

    def obtener_info(self):
        return f"{self.nombre} {self.apellido} - {self.cedula} - {self.correo} - {self.telefono}"

class Cargo(models.TextChoices):
    EMPLEADO = "Empleado", "Empleado"
    ADMINISTRADOR = "Administrador", "Administrador"

class Empleado(Persona):
    salario = models.FloatField()
    cargo = models.CharField(max_length=15, choices=Cargo.choices)
    farmacia = models.ForeignKey("Farmacia", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

class Cliente(Persona):
    farmacia = models.ForeignKey("Farmacia", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - Cliente de {self.farmacia.nombre}"

class Sucursal(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    direccion = models.CharField(max_length=100)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sucursal {self.numero} - {self.farmacia.nombre}"

class Inventario(models.Model):
    codigo = models.CharField(max_length=10, unique=True, null=True)
    sucursal = models.OneToOneField(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventario {self.codigo} {self.sucursal}"

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class ProductoInventario(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE)
    cantidad_disponible = models.PositiveIntegerField()

    class Meta:
        unique_together = ('producto', 'inventario')

    def __str__(self):
        return f"{self.producto.nombre} - {self.inventario.sucursal} ({self.cantidad_disponible} disponibles)"

    def actualizar_cantidad(self, cantidad):
        if self.cantidad_disponible >= cantidad:
            self.cantidad_disponible -= cantidad
            self.save()
        else:
            raise ValidationError(f"Stock insuficiente en {self.inventario.sucursal}")

    @property
    def precio(self):
        return self.producto.precio  # El precio se obtiene del producto relacionado




class TipoEntrega(models.TextChoices):
    RETIRO_ORIGEN = "Retiro en origen", "Retiro en origen"
    RETIRO_SUCURSAL_ACTUAL = "Retiro en sucursal actual", "Retiro en sucursal actual"

class Pedido(models.Model):
    numero_orden = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('enviado', 'Enviado')], null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=Sucursal.objects.first())
    tipo_entrega = models.CharField(max_length=30, choices=TipoEntrega.choices, default=TipoEntrega.RETIRO_ORIGEN)

    def __str__(self):
        return f"Pedido {self.numero_orden} - Cliente: {self.cliente.nombre} - {self.get_tipo_entrega_display()}"


# ✅ Modelo de ItemPedido
class ItemPedido(models.Model):
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto_inventario = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.producto_inventario.precio * self.cantidad  # Usamos precio del Producto
        super().save(*args, **kwargs)

        # Verificar stock y crear transferencia si es necesario
        self.verificar_stock_y_transferir()

    def verificar_stock_y_transferir(self):
        """Verifica si hay suficiente stock en la sucursal del pedido, si no, inicia una transferencia."""
        producto_inventario = self.producto_inventario

        # Si no hay suficiente stock en la sucursal del pedido
        if producto_inventario.cantidad_disponible < self.cantidad:
            # Buscar en otras sucursales con suficiente stock
            producto_origen = ProductoInventario.objects.filter(
                producto=producto_inventario.producto,
                cantidad_disponible__gte=self.cantidad
            ).exclude(inventario=producto_inventario.inventario).first()

            if not producto_origen:
                raise ValidationError(f"No hay stock suficiente para {producto_inventario.producto.nombre} en ninguna sucursal.")

            # Crear transferencia
            Transferencia.objects.create(
                numero=Transferencia.objects.count() + 1,
                fecha=self.pedido.fecha,
                cantidad=self.cantidad,
                producto=producto_inventario.producto,
                origen=producto_origen.inventario.sucursal,
                destino=self.pedido.sucursal,
                completada=False
            )



class MetodoPago(models.TextChoices):
    EFECTIVO = "Efectivo", "Efectivo"
    TARJETA_CREDITO = "Tarjeta de crédito", "Tarjeta de crédito"
    TARJETA_DEBITO = "Tarjeta de débito", "Tarjeta de débito"


class Factura(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    dinero_recibido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_subtotal(self):
        self.subtotal = sum(item.subtotal for item in self.pedido.items.all())

    def calcular_total(self):
        self.calcular_subtotal()
        self.total = self.subtotal + self.impuesto - self.descuento

        if self.metodo_pago == MetodoPago.TARJETA_CREDITO:
            recargo = Decimal("0.04")
            self.total += self.total * recargo

    def calcular_cambio(self):
        if self.dinero_recibido is not None:
            if self.dinero_recibido < self.total:
                raise ValidationError("El dinero recibido no es suficiente para cubrir el total.")
            self.cambio = self.dinero_recibido - self.total
        else:
            raise ValidationError("Debe ingresar el dinero recibido en pagos en efectivo.")

    def actualizar_stock(self):
        for item in self.pedido.items.all():
            item.producto_inventario.actualizar_cantidad(item.cantidad)

    def save(self, *args, **kwargs):
        self.calcular_total()

        if self.metodo_pago == MetodoPago.EFECTIVO:
            self.calcular_cambio()

        super().save(*args, **kwargs)

        # Actualizar stock solo al emitir la factura
        self.actualizar_stock()
    def __str__(self):
        return f"Factura {self.numero} - {self.cliente.nombre} - {self.empleado.nombre}"


class Transferencia(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    completada = models.BooleanField(default=False)
    cantidad = models.PositiveIntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_origen", null=True)
    destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_destino", null=True)

    def completar_transferencia(self):
        producto_origen = ProductoInventario.objects.get(
            producto=self.producto, inventario__sucursal=self.origen
        )
        producto_destino, created = ProductoInventario.objects.get_or_create(
            producto=self.producto, inventario__sucursal=self.destino,
        )

        if producto_origen.cantidad_disponible < self.cantidad:
            raise ValidationError(f"No hay suficiente stock en la sucursal origen {self.origen}")

        producto_origen.cantidad_disponible -= self.cantidad
        producto_origen.save()

        producto_destino.cantidad_disponible += self.cantidad
        producto_destino.save()

        # Actualizamos la transferencia SIN llamar nuevamente a save()
        Transferencia.objects.filter(pk=self.pk).update(completada=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo ejecutar el super().save() en la creación
            super().save(*args, **kwargs)

        # Si se marca como completada, actualizar stock una sola vez
        if self.completada and not kwargs.get('update_fields'):
            self.completar_transferencia()
