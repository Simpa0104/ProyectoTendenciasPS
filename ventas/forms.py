from django import forms
from .models import Venta
from productos.models import Producto

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente_nombre', 'cliente_documento', 'metodo_pago']
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-select'}),
        }

class DetalleVentaForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(cantidad__gt=0),
        widget=forms.Select(attrs={'class': 'form-select producto-select'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control cantidad-input'})
    )