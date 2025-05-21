from django.db import models
from productos.models import Producto
from usuarios.models import UsuarioPersonalizado
from django.core.validators import MinValueValidator

class Venta(models.Model):
    vendedor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.PROTECT)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    cliente_nombre = models.CharField(max_length=100)
    cliente_documento = models.CharField(max_length=20, blank=True, null=True)
    metodo_pago = models.CharField(max_length=50, choices=[
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
    ])

    def __str__(self):
        return f"Venta #{self.id} - {self.fecha_venta.strftime('%d/%m/%Y')}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"