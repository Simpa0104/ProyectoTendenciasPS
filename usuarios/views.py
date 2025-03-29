from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from django.contrib.auth.decorators import login_required

##############################################################################

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autenticamos automáticamente después del registro
            messages.success(request, "Registro exitoso.")
            return redirect('login')  # Redirigir al login después de registrarse
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")  # Muestra los errores
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('dashboard')  # Redirigir después de iniciar sesión
    else:
        form = LoginForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')  # Redirigir al login después de cerrar sesión

@login_required
def dashboard(request):
    return render(request, 'usuarios/dashboard.html')
