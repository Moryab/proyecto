from rest_framework import serializers
from .models import ProductoSucursal

class ProductoSucursalSerializer(serializers.ModelSerializer):
    sucursal = serializers.CharField(source='sucursal.nombre')
    producto = serializers.CharField(source='producto.nombre')

    class Meta:
        model = ProductoSucursal
        fields = ['producto', 'sucursal', 'precio', 'stock']
