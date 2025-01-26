# farmacia/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import ClienteRegistroForm, EmpleadoRegistroForm, UserRegistrationForm

# Vista para el inicio de sesión
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  # Si el usuario es administrador
                return redirect('admin_dashboard')
            elif hasattr(user, 'empleado'):  # Si el usuario es empleado (farmacéutico)
                return redirect('farmaceutico_dashboard')
            elif hasattr(user, 'cliente'):  # Si el usuario es cliente
                return redirect('cliente_dashboard')
        else:
            # Aquí podrías añadir un mensaje de error
            return redirect('login')  # Volver al login en caso de error

    return render(request, 'login.html')

# Vista para crear una cuenta (registro)
def registro_view(request):
    if request.method == 'POST':
        # Formulario para crear un Usuario (todos los usuarios deben crearse primero como User)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()  # Guardamos el usuario
            # Ahora que el usuario está creado, redirigimos al formulario específico de Cliente o Empleado
            if 'cargo' in request.POST:  # Si hay un campo 'cargo', es un Empleado
                empleado_form = EmpleadoRegistroForm(request.POST)
                if empleado_form.is_valid():
                    empleado = empleado_form.save(commit=False)
                    empleado.user = user
                    empleado.save()
                    return redirect('login')  # Redirigir al login después de registrar empleado
            else:  # Si no es un Empleado, es un Cliente
                cliente_form = ClienteRegistroForm(request.POST)
                if cliente_form.is_valid():
                    cliente = cliente_form.save(commit=False)
                    cliente.user = user
                    cliente.save()
                    return redirect('login')  # Redirigir al login después de registrar cliente
        else:
            print(user_form.errors)  # Si hay errores, puedes verlos para depurar
    else:
        user_form = UserRegistrationForm()

    return render(request, 'registro.html', {'user_form': user_form})


# Vistas para los dashboards

def admin_dashboard(request):
    # Aquí puedes agregar lógica específica para el Administrador si es necesario
    return render(request, 'admin_dashboard.html')

def farmaceutico_dashboard(request):
    # Aquí puedes agregar lógica específica para el Farmacéutico si es necesario
    return render(request, 'farmaceutico_dashboard.html')

def cliente_dashboard(request):
    # Aquí puedes agregar lógica específica para el Cliente si es necesario
    return render(request, 'cliente_dashboard.html')
