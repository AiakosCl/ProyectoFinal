from django.db import models, IntegrityError
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.

class Clientes(models.Model):
    app_label = 'ArteNativo'
    Condicion = (
        ('C', 'Contado'),
        ('X', 'Crédito'),
        ('E', 'Efectivo')
    )
    IdCliente = models.CharField(primary_key=True,max_length=13)
    Nombres = models.CharField(max_length=30, blank=False)
    ApPaterno = models.CharField(max_length=15, blank=False)
    ApMaterno = models.CharField(max_length=15)
    FechaNacimiento = models.DateField()
    Correo = models.EmailField(max_length=50, unique=True)
    Telefono = models.CharField(max_length=12, unique=True)
    Direccion = models.CharField(max_length=100)
    CondPago = models.CharField(max_length=1,choices=Condicion, default='C')
    
class Productos(models.Model):
    app_label = 'ArteNativo'
    tipo =(
        ('A', 'Domirtorio'),
        ('B', 'Sala'),
        ('C', 'Comedor'),
        ('D', 'Cocina'),
        ('E', 'Exteriores'),
        ('F', 'Decoración')
        
    )
    Estados = (
        (True, 'Activo'),
        (False, 'Inactivo')
    )
    IdProducto = models.CharField(max_length=10, primary_key=True)
    NombreProducto = models.CharField(max_length=50, blank=False, null=False, default='Descripción corta')
    TipoProducto = models.CharField(max_length=1, choices=tipo, null=False, blank=False,default='B')
    ImagenProducto = models.ImageField(upload_to='ImgProducto/',null=False, blank=False)
    PrecioUnitario = models.DecimalField(max_digits=8, default=0, decimal_places=2)
    Stock = models.IntegerField(blank=False, null=False, default=0)
    Descripcion = RichTextField(blank=True, null=True)
    EstadoProducto = models.BooleanField(blank=False, null=False, choices=Estados, default=True)
    

class Ventas(models.Model):
    app_label = 'ArteNativo'
    IdVenta = models.AutoField(primary_key=True)
    IdCliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=False, blank=False)
    FechaVenta = models.DateField(null=False, blank=False)
    CondPago = models.CharField(max_length=1, blank=False, null=False)
    TotalVenta = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    def ImportarCondicion(self):
        CondicionImportada = self.IdCliente.CondPago
        self.CondPago = CondicionImportada
        self.save()

    
class DetalleVenta(models.Model):
    app_label = 'ArteNativo'
    IdVenta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    IdProducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Cantidad = models.IntegerField(blank=False, null=False, default=1)
    PrecioLinea = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    TotalLinea = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def ImportarPrecio(self):
        PrecioImportado = self.IdProducto.PrecioUnitario
        self.PrecioLinea = PrecioImportado
        self.save()
        

class CArritoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    CodProducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Cantidad = models.PositiveIntegerField(default=1)
    

    




