from django import forms
from .models import *

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
            
        }
        

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = '__all__'

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

