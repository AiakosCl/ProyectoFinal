from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.forms import *

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
        widgets ={
            'passowrd':forms.PasswordInput,
        }
        labels = {
            'username':'Nombre de Usuario',
            'password':'Contraseña',
            'email':'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'is_active': 'Activo?',
            'is_staff': 'Personal propio?',
            'is_superuser': 'Administrador?'
        }
        
        help_texts = {k:"" for k in fields}
        
class UserEditionForm(UserChangeForm):
    password = None
    email = forms.EmailField(label = "Correo Electrónico:")
    last_name = forms.CharField(label = "Apellido:")
    first_name = forms.CharField(label = "Nombre:")
    
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name']

class CrearUsuarioForm(UserCreationForm):
    username = forms.CharField(label="Nombre de Usuario:")
    email = forms.EmailField(label="Correo electrónico:")
    password1 = forms.CharField(label = "Contraseña:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir Contraseña:", widget=forms.PasswordInput)
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}