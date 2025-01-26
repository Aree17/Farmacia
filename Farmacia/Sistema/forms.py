
from django import forms
from .models import Cliente, Empleado, Cargo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulario para registrar un Cliente
class ClienteRegistroForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'farmacia']

# Formulario para registrar un Empleado (Farmacéutico o Administrador)
class EmpleadoRegistroForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'cedula', 'correo', 'telefono', 'salario', 'cargo', 'farmacia']

    cargo = forms.ChoiceField(choices=Cargo.choices, widget=forms.Select)

# Formulario para registro de Usuario (para que todos puedan crear una cuenta)
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
