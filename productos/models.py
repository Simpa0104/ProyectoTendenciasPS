from django.db import models
from django.core.validators import MinValueValidator

class Producto(models.Model):
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    nombre = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=50, default="Desconocida")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"
    #definimos el método __str__ para que al imprimir el objeto se muestre el nombre y la marca del producto.

precio = models.DecimalField(
    max_digits=10, 
    decimal_places=2,
    validators=[MinValueValidator(0.01)]  # Precio debe ser positivo
)
