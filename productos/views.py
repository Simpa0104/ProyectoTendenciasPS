from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

##############################################################################

@login_required
def agregar_producto(request):
    query = request.GET.get('q', '')
    
    if request.method == "POST":
        nombre = request.POST['nombre']
        marca = request.POST['marca']
        cantidad = request.POST['cantidad']
        precio = request.POST['precio']
        imagen = request.FILES.get('imagen', None)

        Producto.objects.create(nombre=nombre, marca=marca, cantidad=cantidad, precio=precio, imagen=imagen)
        
        return redirect('agregar_producto')
    
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    return render(request, 'productos/agregar_productos.html', {'productos': productos, 'query': query})

##############################################################################

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST['nombre']
        producto.marca = request.POST['marca']
        producto.cantidad = request.POST['cantidad']
        producto.precio = request.POST['precio']
        
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']

        producto.save()
        return redirect('agregar_producto')

##############################################################################

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('agregar_producto')

##############################################################################
