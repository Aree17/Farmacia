from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal

# ✅ Modelo de Farmacia
class Farmacia(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

# ✅ Modelo abstracto Persona
class Persona(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=10, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True  # 🔹 Esto indica que no se creará una tabla en la BD para Persona

    def obtener_info(self):
        return f"{self.nombre} {self.apellido} - {self.cedula} - {self.correo} - {self.telefono}"

# ✅ Enum para Cargo en Empleado
class Cargo(models.TextChoices):
    FARMACEUTICO = "Farmacéutico", "Farmacéutico"
    ADMINISTRADOR = "Administrador", "Administrador"

# ✅ Modelo de Empleado (hereda de Persona)
class Empleado(Persona):
    salario = models.FloatField()
    cargo = models.CharField(max_length=15, choices=Cargo.choices)
    farmacia = models.ForeignKey("Farmacia", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

# ✅ Modelo de Cliente (hereda de Persona)
class Cliente(Persona):
    farmacia = models.ForeignKey("Farmacia", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - Cliente de {self.farmacia.nombre}"


# ✅ Modelo de Sucursal
class Sucursal(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    direccion = models.CharField(max_length=100)
    farmacia = models.ForeignKey(Farmacia, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sucursal {self.numero} - {self.farmacia.nombre}"


# ✅ Modelo de Inventario por Sucursal
class Inventario(models.Model):
    codigo = models.CharField(max_length=10, unique=True, null=True)
    sucursal = models.OneToOneField(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventario {self.codigo} {self.sucursal}"


# ✅ Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ProductoInventario(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)  # Producto general
    inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE)  # Inventario de la sucursal
    cantidad_disponible = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('producto', 'inventario')  # Evita duplicados del mismo producto en una sucursal

    def __str__(self):
        return f"{self.producto.nombre} - {self.inventario.sucursal} ({self.cantidad_disponible} disponibles)"

    def actualizar_cantidad(self, cantidad):
        if self.cantidad_disponible >= cantidad:
            self.cantidad_disponible -= cantidad
            self.save()
        else:
            raise ValidationError(f"Stock insuficiente en {self.inventario.sucursal}")


class TipoEntrega(models.TextChoices):
    RETIRO_ORIGEN = "Retiro en origen", "Retiro en origen"
    RETIRO_SUCURSAL_ACTUAL = "Retiro en sucursal actual", "Retiro en sucursal actual"

class Pedido(models.Model):
    numero_orden = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="pedidos_origen", null=True)
    sucursal_actual = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="pedidos_sucursal_actual", null=True, blank=True)
    tipo_entrega = models.CharField(max_length=30, choices=TipoEntrega.choices, default=TipoEntrega.RETIRO_ORIGEN)

    def __str__(self):
        return f"Pedido {self.numero_orden} - {self.get_tipo_entrega_display()}"

    def verificar_o_transferir_stock(self):
        """ Verifica el stock en la sucursal elegida y genera una transferencia si es necesario. """
        sucursal_retiro = self.sucursal_origen if self.tipo_entrega == TipoEntrega.RETIRO_ORIGEN else self.sucursal_actual

        for item in self.items.all():
            inventario = ProductoInventario.objects.filter(
                producto=item.producto_inventario.producto, inventario__sucursal=sucursal_retiro
            ).first()

            if not inventario or inventario.cantidad_disponible < item.cantidad:
                # Buscar otra sucursal con stock suficiente
                sucursal_origen = ProductoInventario.objects.filter(
                    producto=item.producto_inventario.producto, cantidad_disponible__gte=item.cantidad
                ).exclude(inventario__sucursal=sucursal_retiro).first()

                if not sucursal_origen:
                    raise ValidationError(f"No hay stock disponible en ninguna sucursal para {item.producto_inventario.producto.nombre}.")

                # Crear transferencia automática
                Transferencia.objects.create(
                    numero=Transferencia.objects.count() + 1,
                    fecha=self.fecha,
                    cantidad=item.cantidad,
                    empleado=None,  # Opcionalmente asignar empleado
                    producto=item.producto_inventario.producto,
                    origen=sucursal_origen.inventario.sucursal,
                    destino=sucursal_retiro,
                    completada=False
                )

    def save(self, *args, **kwargs):
        """ Verifica stock y genera transferencia automática si es necesario. """
        super().save(*args, **kwargs)
        if self.tipo_entrega == TipoEntrega.RETIRO_SUCURSAL_ACTUAL:
            self.verificar_o_transferir_stock()

# ✅ Modelo de ItemPedido
class ItemPedido(models.Model):
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto_inventario = models.ForeignKey(ProductoInventario, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        """ Solo calcula el subtotal sin actualizar inventario aquí """
        self.subtotal = self.producto_inventario.precio * self.cantidad
        super().save(*args, **kwargs)









# ✅ Enum para Métodos de Pago
class MetodoPago(models.TextChoices):
    EFECTIVO = "Efectivo", "Efectivo"
    TARJETA_CREDITO = "Tarjeta de crédito", "Tarjeta de crédito"
    TARJETA_DEBITO = "Tarjeta de débito", "Tarjeta de débito"

# ✅ Modificar la Factura para calcular total basado en ItemFactura
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
    dinero_recibido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Solo para efectivo
    cambio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Solo para efectivo

    def calcular_subtotal(self):
        """ Calcula el subtotal sumando los subtotales de los ItemPedido asociados """
        self.subtotal = sum(item.subtotal for item in self.pedido.items.all())

    def calcular_total(self):
        """ Calcula el total aplicando impuestos y descuentos y el recargo si aplica """
        self.total = self.subtotal + self.impuesto - self.descuento

        # Si el pago es con tarjeta de crédito, aplicar recargo del 4%
        if self.metodo_pago == MetodoPago.TARJETA_CREDITO:
            recargo = Decimal("0.04")  # Usar Decimal en lugar de float
            self.total += self.total * recargo

    def actualizar_stock(self):
        """ Reduce el stock de los productos después de que la factura se haya guardado """
        for item in self.pedido.items.all():
            item.producto_inventario.actualizar_cantidad(item.cantidad)

    def save(self, *args, **kwargs):
        """ Verifica el stock antes de registrar la factura y ajusta según el método de pago """
        for item in self.pedido.items.all():
            if item.producto_inventario.cantidad_disponible < item.cantidad:
                raise ValidationError(f"Stock insuficiente en {item.producto_inventario.inventario.sucursal}")

        # Calcula subtotal y total
        self.calcular_subtotal()
        self.calcular_total()

        # Si el pago es en efectivo, calcula el cambio
        if self.metodo_pago == MetodoPago.EFECTIVO:
            if not self.dinero_recibido:
                raise ValidationError("Debe ingresar el dinero recibido en pagos en efectivo.")
            if self.dinero_recibido < self.total:
                raise ValidationError("El dinero recibido no es suficiente para cubrir el total.")
            self.cambio = self.dinero_recibido - self.total

        super().save(*args, **kwargs)  # Guarda la factura

        # Luego, actualiza el inventario si la factura se guardó correctamente
        self.actualizar_stock()

    def __str__(self):
        return f"Factura {self.numero} - Pedido {self.pedido.numero_orden}"



# ✅ Modelo de Transferencia entre Sucursales

class Transferencia(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    completada = models.BooleanField(default=False)
    cantidad = models.PositiveIntegerField()
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_origen")
    destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_destino")

    def completar_transferencia(self):
        """ Completa la transferencia moviendo el stock del origen al destino. """
        producto_origen = ProductoInventario.objects.get(
            producto=self.producto, inventario__sucursal=self.origen
        )
        producto_destino, created = ProductoInventario.objects.get_or_create(
            producto=self.producto, inventario__sucursal=self.destino,
            defaults={"cantidad_disponible": 0, "precio": producto_origen.precio}
        )

        if producto_origen.cantidad_disponible < self.cantidad:
            raise ValidationError(f"No hay suficiente stock en la sucursal origen {self.origen}")

        # Actualizar los inventarios
        producto_origen.cantidad_disponible -= self.cantidad
        producto_origen.save()

        producto_destino.cantidad_disponible += self.cantidad
        producto_destino.save()

        # Marcar la transferencia como completada
        self.completada = True
        self.save()

    def save(self, *args, **kwargs):
        if self.completada:
            self.completar_transferencia()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transferencia {self.numero} - {self.origen} → {self.destino} ({self.cantidad})"


