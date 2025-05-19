import os
import django
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventario.settings")  
django.setup()

from productos.models import Producto  

# Lista de productos a agregar
productos_data = [
    {"nombre": "Air Max 90", "marca": "Nike", "cantidad": 10, "precio": 420000},
    {"nombre": "Superstar", "marca": "Adidas", "cantidad": 15, "precio": 380000},
    {"nombre": "Old Skool", "marca": "Vans", "cantidad": 12, "precio": 300000},
    {"nombre": "Chuck Taylor All Star", "marca": "Converse", "cantidad": 20, "precio": 250000},
    {"nombre": "UltraBoost 22", "marca": "Adidas", "cantidad": 8, "precio": 600000},
    {"nombre": "React Infinity Run 3", "marca": "Nike", "cantidad": 5, "precio": 550000},
    {"nombre": "Sk8-Hi", "marca": "Vans", "cantidad": 14, "precio": 320000},
    {"nombre": "Forum Low", "marca": "Adidas", "cantidad": 18, "precio": 350000},
    {"nombre": "Jordan 1 Retro High", "marca": "Nike", "cantidad": 7, "precio": 750000},
    {"nombre": "Classic Leather", "marca": "Reebok", "cantidad": 11, "precio": 280000},
]

# Insertar productos en la base de datos
for data in productos_data:
    Producto.objects.create(**data)

print("✅ Productos agregados exitosamente.")
