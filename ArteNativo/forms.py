from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'
        widgets = {
            'FechaNacimiento': forms.DateInput(format='%d/%m/%Y'),
        }
        labels = {
            'ApPaterno':'Apellido Paterno',
            'ApMaterno':'Apellido Materno',
            'IdCliente':'RUT',
            'CondPago':'Condición de Pago',
            'FechaNacimiento': 'Fecha de Nacimiento',
            
        }
        

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'
        # widgets = {
        #     'Descripcion': CKEditorWidget(),
        # }
        labels = {
            'IdProducto': 'Código del Producto',
            'NombreProducto': 'Nombre del Producto',
            'Tipo':'Habitación / Sector',
            'ImagenProducto': 'Imagen referencial',
            'PrecioUnitario': 'Precio Base',
            'Descripcion': 'Descripción del Producto',
            'EstadoProducto': 'Activo / Inactivo',
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Ventas
        fields = '__all__'
        
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class FiltroClienteForm(forms.Form):
    id_cliente = forms.CharField(max_length=13, label='RUT Cliente')
    

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username','password','email','first_name','last_name','is_active','is_staff','is_superuser']
        labels = {
            'username':'Nombre de Usuario',
            'email':'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'is_active': 'Activo?',
            'is_staff': 'Personal propio?',
            'is_superuser': 'Administrador?'
        }
        
