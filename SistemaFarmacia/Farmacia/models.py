from django.db import models
from decimal import Decimal


class Farmacia(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)

    class Meta:
        abstract = True

    def obtener_info(self):
        return f"{self.nombre} - {self.cedula} "

class Cargo(models.TextChoices):
    EMPLEADO = "EMPLEADO", "Empleado"
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

class Empleado(Persona):
    salario = models.FloatField()
    cargo = models.CharField(max_length=15, choices=Cargo.choices)
    farmacia = models.ForeignKey("Farmacia", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.cargo})"

class Cliente(Persona):
    telefono = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    direccion = models.CharField(max_length=100)
    farmacia = models.ForeignKey(Farmacia, related_name='sucursal_list', on_delete=models.CASCADE)

    def __str__(self):
        return f"Sucursal {self.numero} - {self.farmacia.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class TipoEntrega(models.TextChoices):
    RETIRO_ORIGEN = "Retiro en origen", "Retiro en origen"
    RETIRO_SUCURSAL_ACTUAL = "Retiro en sucursal actual", "Retiro en sucursal actual"

class MetodoPago(models.TextChoices):
    EFECTIVO = "EFECTIVO", "Efectivo"
    TARJETA_CREDITO = "TARJETA", "Tarjeta"

class Inventario(models.Model):
    codigo = models.CharField(max_length=10, unique=True, null=True)
    sucursal = models.ForeignKey(Sucursal, related_name='inventario_list', on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Inventario {self.producto.nombre} {self.sucursal}"

class Factura(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    sucursal = models.ForeignKey(Sucursal, related_name='factura_list', on_delete=models.CASCADE, null=True)
    cliente = models.ForeignKey(Cliente,related_name='factura_list', on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, null=True)
    cantidad = models.PositiveIntegerField(default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices)
    TipoEntrega = models.CharField(max_length=30, choices=TipoEntrega.choices, default=TipoEntrega.RETIRO_ORIGEN)

    def calcular_subtotal(self):
        self.subtotal = self.inventario.producto.precio*self.cantidad
        self.impuesto = self.subtotal * Decimal(0.12)

    def calcular_total(self):
        self.total= self.subtotal + self.impuesto

    def __str__(self):
        return f"Factura {self.numero} - {self.cliente.nombre}"

    def actualizar_inventario(self):
        if self.inventario:
            self.inventario.cantidad -= self.cantidad
            self.inventario.save()

    def save(self, *args, **kwargs):
        self.calcular_subtotal()
        self.calcular_total()
        self.actualizar_inventario()
        super(Factura, self).save(*args, **kwargs)

class Estado(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    COMPLETADA = 'COMPLETADA', 'Completada'
    CANCELADA = 'CANCELADA', 'Cancelada'

class Transferencia(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField(default=0)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, related_name='transferencia_list', on_delete=models.CASCADE, null=True)
    origen = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_origen", null=True)
    destino = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="transferencias_destino", null=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)

    def __str__(self):
        return f"Transferencia {self.numero} - {self.producto.nombre} - {self.cantidad} unidades"

