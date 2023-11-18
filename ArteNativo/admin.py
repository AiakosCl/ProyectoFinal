from django.contrib import admin
from ArteNativo.models import *

# Register your models here.

class ProductossAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Productos._meta.get_fields()]
    list_filter = ('IdProducto','NombreProducto','TipoProducto')
    search_fields = ('IdProducto', 'NombreProducto','TipoProducto')

admin.site.register(Clientes)
admin.site.register(Productos)
admin.site.register(Ventas)
admin.site.register(DetalleVenta)

#@admin.register(Productos)




