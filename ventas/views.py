from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from productos.models import Producto
from .models import Venta, DetalleVenta
from .forms import VentaForm
import json

@login_required
def crear_venta(request):
    if request.method == 'POST':
        print("Datos recibidos:", request.POST)  # Para depuración
        
        form_venta = VentaForm(request.POST)
        if form_venta.is_valid():
            try:
                with transaction.atomic():
                    venta = form_venta.save(commit=False)
                    venta.vendedor = request.user
                    
                    productos_ids = request.POST.getlist('productos')
                    cantidades = request.POST.getlist('cantidades')
                    
                    if not productos_ids:
                        raise ValueError("Debe seleccionar al menos un producto")

                    total_backend = 0
                    detalles = []
                    
                    for producto_id, cantidad in zip(productos_ids, cantidades):
                        producto = Producto.objects.get(id=producto_id)
                        cantidad = int(cantidad)
                        
                        if cantidad <= 0:
                            continue
                            
                        if producto.cantidad < cantidad:
                            raise ValueError(f"Stock insuficiente para {producto.nombre}")

                        subtotal = float(producto.precio) * cantidad
                        total_backend += subtotal
                        
                        detalles.append(DetalleVenta(
                            venta=venta,
                            producto=producto,
                            cantidad=cantidad,
                            precio_unitario=producto.precio,
                            subtotal=subtotal
                        ))

                    print("Total calculado en backend:", total_backend)  # Depuración
                    
                    if total_backend <= 0:
                        raise ValueError("El total de la venta debe ser mayor a cero")

                    venta.total = total_backend
                    venta.save()
                    DetalleVenta.objects.bulk_create(detalles)
                    
                    # Actualizar stock
                    for detalle in detalles:
                        detalle.producto.cantidad -= detalle.cantidad
                        detalle.producto.save()

                    messages.success(request, f'Venta registrada! Total: ${total_backend:.2f}')
                    return redirect('listar_ventas')

            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                print("Error en la transacción:", str(e))  # Depuración
        else:
            messages.error(request, 'Corrija los errores en el formulario')
    else:
        form_venta = VentaForm()

    productos = Producto.objects.all()
    return render(request, 'ventas/crear_venta.html', {
        'form_venta': form_venta,
        'productos': productos
    })

@login_required
def listar_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    return render(request, 'ventas/listar_ventas.html', {'ventas': ventas})

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    
    return render(request, 'ventas/detalle_venta.html', {
        'venta': venta,
        'detalles': detalles
    })

@login_required
def buscar_producto(request):
    term = request.GET.get('term', '')
    productos = Producto.objects.filter(
        nombre__icontains=term, 
        cantidad__gt=0
    ).values('id', 'nombre', 'precio', 'cantidad', 'imagen')
    
    # Agregar URL de imagen si existe
    for producto in productos:
        if producto['imagen']:
            producto['imagen_url'] = Producto.objects.get(id=producto['id']).imagen.url
    
    return JsonResponse(list(productos), safe=False)