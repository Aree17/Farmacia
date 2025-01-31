from django import forms
from django.contrib.auth.models import User

from Farmacia.models import Inventario, Transferencia, Producto, Factura

class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['codigo', 'sucursal', 'producto', 'cantidad']


class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ['numero', 'producto', 'origen', 'destino', 'cantidad', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['numero', 'sucursal', 'inventario', 'cantidad', 'fecha', 'cliente', 'total', 'metodo_pago', 'TipoEntrega']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'opcion_entrega': forms.Select(attrs={'class': 'custom-select'}),
        }