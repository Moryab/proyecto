from django.contrib import admin
from .models import Sucursal, Producto, ProductoSucursal
# Register your models here.

admin.site.register(Sucursal)
admin.site.register(Producto)
admin.site.register(ProductoSucursal)

