from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_venta, name='crear_venta'),
    path('listar/', views.listar_ventas, name='listar_ventas'),
    path('detalle/<int:venta_id>/', views.detalle_venta, name='detalle_venta'),
    path('buscar-producto/', views.buscar_producto, name='buscar_producto'),
]