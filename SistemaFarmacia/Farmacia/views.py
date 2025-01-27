from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView
from .forms import RegistroClienteForm, InventarioForm, TransferenciaForm, ProductoForm, FacturaForm
from .models import Cliente, Farmacia, Sucursal, Producto, Factura, Transferencia, Inventario


def registrar_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Crear el cliente asociado
            Cliente.objects.create(
                nombre=Cliente.nombre,
                cedula=Cliente.cedula,  # Puedes reemplazar esto con otro dato si lo necesitas
                telefono=Cliente.telefono,
                email=Cliente.email
            )

            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('inicio')  # Redirige a la página principal o deseada
    else:
        form = RegistroClienteForm()

    return render(request, 'registro.html', {'form': form})

def inicio(request):
    # Obtener las farmacias, sucursales y productos para mostrar
    farmacias = Farmacia.objects.all()
    sucursales = Sucursal.objects.all()
    productos = Producto.objects.all()

    return render(request, 'inicio.html', {
        'farmacias': farmacias,
        'sucursales': sucursales,
        'productos': productos
    })


class NoClienteMixin:
    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario tiene un objeto Cliente asociado
        if hasattr(request.user, 'Cliente'):
            # Si el usuario es cliente, lo redirigimos o mostramos un error
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return super().dispatch(request, *args, **kwargs)



class GestionInventarioListView(ListView):
    model = Inventario
    template_name = 'gestion_inventario.html'
    context_object_name = 'inventarios'
    paginate_by = 10  # Paginación de 10 resultados por página

    # Filtrar inventarios de una sucursal (si se necesita)
    def get_queryset(self):
        return Inventario.objects.all()

class GestionInventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'editar_inventario.html'
    success_url = reverse_lazy('gestion_inventario')  # Redirige a la lista de inventarios

    def form_valid(self, form):
        # Aquí se pueden agregar más validaciones, por ejemplo, si el stock no puede ser negativo
        return super().form_valid(form)

class GestionInventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'nuevo_inventario.html'
    success_url = reverse_lazy('gestion_inventario')

class GenerarTransferenciaView(View):
    def get(self, request):
        form = TransferenciaForm()
        return render(request, 'generar_transferencia.html', {'form': form})

    def post(self, request):
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            transferencia = form.save(commit=False)
            # Obtenemos datos de la transferencia
            origen = transferencia.origen
            destino = transferencia.destino
            producto = transferencia.producto
            cantidad = transferencia.cantidad

            # Verificamos el inventario en la sucursal de origen
            inventario_origen = origen.inventario_list.filter(producto=producto).first()
            inventario_destino = destino.inventario_list.filter(producto=producto).first()

            if inventario_origen and inventario_origen.cantidad >= cantidad:
                # Reducimos inventario en origen
                inventario_origen.cantidad -= cantidad
                inventario_origen.save()

                # Aumentamos inventario en destino o creamos uno nuevo
                if inventario_destino:
                    inventario_destino.cantidad += cantidad
                    inventario_destino.save()
                else:
                    destino.inventario_list.create(producto=producto, cantidad=cantidad)

                transferencia.estado = 'COMPLETADA'
            else:
                transferencia.estado = 'CANCELADA'

            transferencia.save()  # Guardamos finalmente la transferencia
            return redirect('transferencias_list')
        return render(request, 'generar_transferencia.html', {'form': form})


class ListaTransferenciasView(View):
    def get(self, request):
        transferencias = Transferencia.objects.all()
        return render(request, 'lista_transferencias.html', {'transferencias': transferencias})

class ProductoListView(View):
    def get(self, request):
        productos = Producto.objects.all()
        form = ProductoForm()
        return render(request, 'productos_list.html', {'productos': productos, 'form': form})

    def post(self, request):
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/productos')
        productos = Producto.objects.all()
        return render(request, 'productos_list.html', {'productos': productos, 'form': form})

def generarfactura(request):
        if request.method == 'POST':
            form = FacturaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('listar_facturas')  # Redirige a la vista que mostrará todas las facturas creadas
        else:
            form = FacturaForm()
        return render(request, 'generar_factura.html', {'form': form})

def listarfacturas(request):
        facturas = Factura.objects.all()
        return render(request, 'listar_facturas.html', {'facturas': facturas})