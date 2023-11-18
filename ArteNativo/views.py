import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.

def index(request):
    return render(request, 'ArteNativo.html')

@login_required(login_url='entrar')
def administracion(request):
    return render(request, 'administracion.html')



# Vistas por Clase, para ver las lista de las tablas como primera visión de caga gestión
class ProductoListView(ListView):
    model = Productos
    template_name = "ListaProductos.html"
    context_object_name = 'productos'

class ClienteListView(LoginRequiredMixin,ListView):
    model = Clientes
    template_name = 'ListaClientes.html'
    context_object_name = 'NominaClientes'

def presentacion(request, tipo_producto=None): # Para filtrar la lista de productos por TipoProducto
    if tipo_producto:
        productos = Productos.objects.filter(TipoProducto=tipo_producto)
    else:
        productos = Productos.objects.all()
        
    context = {'productos': productos}
    return render(request, 'ListaProductos.html',context)


def FiltroClientes(request, Id_cliente=None):
    if Id_cliente:
        clientes = Clientes.objects.filter(IdCliente = Id_cliente)
    else:
        clientes = Productos.objects.all()
    
    context = {'NominaClientes': clientes}
    return render(request, 'ListaClientes.html', context)




# Vistas para crear Clientes, Productos, Ventas, etc.
@login_required(login_url='entrar')
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            print('Se ha creado el nuevo cliente')
            return redirect('ListaClientes')  # Redirige a la lista de clientes después de crear uno nuevo
    else:
        form = ClienteForm()

    return render(request, 'NuevoCliente.html', {'form': form})

@login_required(login_url='entrar')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')  # Redirige a la lista de productos después de crear uno nuevo
    else:
        form = ProductoForm()

    return render(request, 'crear_producto.html', {'form': form})

@login_required(login_url='entrar')
def crear_venta(request):
    if request.method == 'POST':
        Venta_form = VentaForm(request.POST)
        Detalle_form = DetalleVentaForm(request.POST)
        
        if Venta_form.is_valid() and Detalle_form.is_valid():
            venta = Venta_form.save()
            detalle = Detalle_form.save(commit=False)
            detalle.venta = venta
            detalle.total_linea = detalle.cantidad * detalle.PrecioUnitario
            detalle.save()
            
            Ventas.TotalVenta
            return redirect('lista_ventas')  # Redirige a la lista de ventas después de crear una nueva
    else:
        form = VentaForm()

    return render(request, 'crear_venta.html', {'form': form})

@login_required(login_url='entrar')
def crear_detalle_venta(request):
    if request.method == 'POST':
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_detalle_ventas')  # Redirige a la lista de detalles de ventas después de crear uno nuevo
    else:
        form = DetalleVentaForm()

    return render(request, 'crear_detalle_venta.html', {'form': form})






#Vistas para editar tablas

class EditarClienteView(View):
    template_name = 'EditarCliente.html'

    def get(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        form = ClienteForm(instance=cliente)
        return render(request, self.template_name, {'form': form, 'cliente': cliente})

    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('ListaClientes')
        return render(request, self.template_name, {'form': form, 'cliente': cliente})


class EliminarClienteView(View):
    template_name = 'EliminarCliente.html'

    def get(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        return render(request, self.template_name, {'cliente': cliente})

    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        cliente.delete()
        return redirect('ListaClientes')






# Las vistas de Login, log-out, y Crear Usuarios.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('administracion')
        else:
            return render(request, 'login.html', {'error': 'Nombre de usuario o contraseña incorrectos.'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('ListaProducto')

@login_required(login_url='entrar')
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrar')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
