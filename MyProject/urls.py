"""
URL configuration for MyProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ArteNativo import views, forms, models
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ProductoListView.as_view(), name='Base'),
    path('productos/', views.ProductoListView.as_view(), name='ListaProducto'),
    path('administracion/', views.administracion, name='administracion'),
    path('login/', views.user_login, name='entrar'),
    path('logout/', views.user_logout, name='salir'),
    path('NuevoUsuario/',views.user_register, name='crear_usuario'),
    path('productos/<str:tipo_producto>/', views.presentacion, name='ListaProductoFiltrada'),
    path('NuevoCliente/', views.crear_cliente, name="NuevoCliente"),
    path('Clientes/', views.ClienteListView.as_view(), name='ListaClientes'),
    path('Clientes/<str:Id_cliente>/', views.FiltroClientes, name="NominaFiltrada"),
    path('Clientes/editar/<str:pk>/', views.ClienteUpdateView.as_view(), name='editar_cliente'),
    path('Clientes/eliminar/<str:pk>/', views.EliminarClienteView.as_view(), name='eliminar_cliente'),
    path('ListaProductos/', views.TablaListView.as_view(), name="TablaProductos"),
    path('ListaProductos/editar/<str:pk>/', views.ProductoEditar.as_view(), name='EditarProductoForm'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)