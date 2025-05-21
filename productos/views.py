from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q  # Para búsquedas más avanzadas

##############################################################################

@login_required
def agregar_producto(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page')
    
    # Obtener todos los productos (o filtrar si hay búsqueda)
    productos_list = Producto.objects.all()
    
    if query:
        # Búsqueda más avanzada que también considera la marca
        productos_list = productos_list.filter(
            Q(nombre__icontains=query) | Q(marca__icontains=query)
        )
    
    # Paginación
    paginator = Paginator(productos_list, 10)  # 10 items por página
    productos = paginator.get_page(page)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)  # Usamos el Form que ya teníamos definido
        
        if form.is_valid():
            form.save()
            messages.success(request, "Producto agregado correctamente")
            return redirect('agregar_producto')
        else:
            # Mostrar errores de validación
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProductoForm()  # Form vacío para GET
    
    context = {
        'productos': productos,
        'query': query,
        'form': form  # Pasamos el form al template
    }
    
    return render(request, 'productos/agregar_productos.html', context)

##############################################################################

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente")
            return redirect('agregar_producto')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    
    # Para GET mostramos el form precargado
    form = ProductoForm(instance=producto)
    
    # Podrías renderizar un template específico para edición
    # o manejar todo con modales como ya lo tienes
    return redirect('agregar_producto')

##############################################################################

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":  # Más seguro que solo GET
        producto.delete()
        messages.success(request, "Producto eliminado correctamente")
    
    return redirect('agregar_producto')

##############################################################################