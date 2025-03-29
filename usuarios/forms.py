from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioPersonalizado  # Asegúrate de importar el modelo correcto

class RegistroForm(UserCreationForm):
    telefono = forms.CharField(required=False, label="Teléfono")

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'email', 'telefono', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    pass  # Dejamos el formulario de login con la configuración por defecto
