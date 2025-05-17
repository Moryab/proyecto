from rest_framework import serializers
from .models import ProductoSucursal

class ProductoSucursalSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source='sucursal.nombre')
    sucursal_id = serializers.IntegerField(source='sucursal.id')
    producto_nombre = serializers.CharField(source='producto.nombre')
    producto_id = serializers.IntegerField(source='producto.id')

    class Meta:
        model = ProductoSucursal
        fields = [
            'producto_id', 'producto_nombre',
            'sucursal_id', 'sucursal_nombre',
            'precio', 'stock'
        ]
