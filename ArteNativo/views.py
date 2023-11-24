import datetime
from typing import Any
from django.db import models
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
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request, 'ArteNativo.html')

@login_required
def administracion(request):
    return render(request, 'administracion.html')



# Vistas por Clase, para ver las lista de las tablas como primera visión de caga gestión
class ProductoListView(ListView):
    model = Productos
    template_name = "ListaProductos.html"
    context_object_name = 'productos'
    
class TablaListView(LoginRequiredMixin, ListView):
    model = Productos
    template_name = "TablaProductos.html"
    context_object_name = 'ListadeProductos'

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

@login_required
def FiltroClientes(request, Id_cliente=None):
    if Id_cliente:
        clientes = Clientes.objects.filter(IdCliente__startswith = Id_cliente)
    else:
        clientes = Clientes.objects.all()
    
    context = {'NominaClientes': clientes}
    return render(request, 'ListaClientes.html', context)

@login_required
def FiltroUsuario(request, nombre=None):
    print(nombre)
    if nombre:
        usuarios = User.objects.filter(first_name__startswith = nombre)
    elif nombre==None:
        usuarios = User.objects.all()
    
    context = {'ListaUsuarios': usuarios}
    return render(request, 'ListaUsuarios.html', context)

@login_required
def FiltroTablaProductos(request, id_producto=None):
    if id_producto:
        ListaFiltadaProductos = Productos.objects.filter(IdProducto__startswith = id_producto)
    else:
        ListaFiltadaProductos = Productos.objects.all()
    
    Contexto = {'ListadeProductos': ListaFiltadaProductos}
    return render(request, 'TablaProductos.html', Contexto)

class ListaUsuariosView(LoginRequiredMixin, ListView):
    model = User
    template_name='ListaUsuarios.html'
    context_object_name ="ListaUsuarios"


# Vistas para crear Clientes, Productos, Ventas, etc.
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cliente ha sido creado con éxito!')
            return redirect('ListaClientes')  # Redirige a la lista de clientes después de crear uno nuevo
    else:
        form = ClienteForm()

    return render(request, 'Form_Clientes.html', {'form': form})

@login_required(login_url='entrar')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('TablaProductos')  # Redirige a la lista de productos después de crear uno nuevo
    else:
        form = ProductoForm()

    return render(request, 'Form_Productos.html', {'form': form})

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

def agregar_al_carrito(request, producto_id): #Crear Carrito de Compras para lanzar cotización.
    if request.method == 'POST':
        producto = Productos.objects.get(pk=producto_id)
        cantidad = request.POST.get('cantidad', 1)  # Puedes ajustar cómo manejas la cantidad

        # Verificar si el elemento ya está en el carrito
        carrito_item, creado = CArritoItem.objects.get_or_create(
            user=request.user,
            producto=producto
        )

        # Si ya está en el carrito, aumentar la cantidad
        if not creado:
            carrito_item.cantidad += int(cantidad)
            carrito_item.save()

    return redirect('ListaProducto')

def ver_carrito(request):
    carrito_items = CArritoItem.objects.filter(user = request.user)
    return render(request, 'carrito.html', {'carrito_item':carrito_items})



#Vistas para editar tablas

# class ClienteUpdateView(UpdateView): #La forma fácil para editar un registro con UpdateView
#     model = Clientes
#     template_name = 'EditarCliente.html'
#     form_class = ClienteForm
#     success_url = reverse_lazy('ListaClientes')

class EditarClienteView(LoginRequiredMixin, View): #Forma para editar utilizando View
    template_name = 'Form_Clientes.html'

    def get(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        form = ClienteForm(instance=cliente)
        return render(request, self.template_name, {'form': form, 'cliente': cliente})

    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Información de {cliente.Nombres} actualizada con éxito!')
            return redirect('ListaClientes')
        return render(request, self.template_name, {'form': form, 'cliente': cliente})    

class EliminarClienteView(LoginRequiredMixin,View):
    template_name = 'EliminarCliente.html'

    def get(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        return render(request, self.template_name, {'cliente': cliente})

    def post(self, request, pk, *args, **kwargs):
        cliente = get_object_or_404(Clientes, pk=pk)
        cliente.delete()
        messages.warning(request, 'Se eliminó el registro del cliente.')
        return redirect('ListaClientes')

class ProductoEditar(LoginRequiredMixin, UpdateView): #Revisar si se programa la vista como View
    model = Productos
    template_name = 'Form_Productos.html'
    form_class = ProductoForm
    success_url = reverse_lazy('TablaProductos')

class EliminarProductoView(LoginRequiredMixin,View):
    template_name = 'EliminarProducto.html'

    def get(self, request, pk, *args, **kwargs):
        ProductoEliminar = get_object_or_404(Productos, pk=pk)
        return render(request, self.template_name, {'producto': ProductoEliminar})

    def post(self, request, pk, *args, **kwargs):
        ProductoEliminar = get_object_or_404(Productos, pk=pk)
        ProductoEliminar.delete()
        messages.warning(request, f'Se ha eliminado el producto: {ProductoEliminar.NombreProducto}.')
        return redirect('TablaProductos')

class EliminarUsuarioView(LoginRequiredMixin,View):
    template_name = 'EliminarUsuario.html'

    def get(self, request, pk, *args, **kwargs):
        UsuarioEliminar = get_object_or_404(User, pk=pk)
        return render(request, self.template_name, {'usuario': UsuarioEliminar})

    def post(self, request, pk, *args, **kwargs):
        UsuarioEliminar = get_object_or_404(User, pk=pk)
        UsuarioEliminar.delete()
        messages.warning(request, f'Se ha eliminado el usuario: {UsuarioEliminar.username}.')
        return redirect('ListaUsuarios')
    






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
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entrar')
    else:
        form = CrearUsuarioForm()
    return render(request, 'Form_Usuario.html', {'form': form})

class EditarUsuario(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditarUsuarioForm
    template_name = 'Form_Usuario.html'
    success_url = reverse_lazy('entrar')
