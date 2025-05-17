from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto, ProductoSucursal
from .serializers import ProductoSucursalSerializer
from django.db.models import Q

# Vista para mostrar el frontend (como ya tienes)
def index(request):
    return render(request, "aplicacion/index.html")

# API: obtener stock y precios de un producto por sucursal
@api_view(['GET'])
def producto_detalle(request, producto_id):
    items = ProductoSucursal.objects.filter(producto_id=producto_id)
    serializer = ProductoSucursalSerializer(items, many=True)
    return Response(serializer.data)

# API: realizar una venta (descontar stock)
@api_view(['POST'])
def realizar_venta(request):
    producto_id = request.data.get("producto_id")
    sucursal_id = request.data.get("sucursal_id")
    cantidad = int(request.data.get("cantidad"))

    producto_sucursal = get_object_or_404(
        ProductoSucursal,
        producto_id=producto_id,
        sucursal_id=sucursal_id
    )

    if producto_sucursal.stock < cantidad:
        return Response({"error": "Stock insuficiente"}, status=400)

    producto_sucursal.stock -= cantidad
    producto_sucursal.save()

    return Response({"mensaje": "Venta realizada correctamente"})

@api_view(['GET'])
def buscar_por_nombre(request, nombre):
    productos = Producto.objects.filter(nombre__icontains=nombre)
    
    if not productos.exists():
        return Response([])

    producto = productos.first()  # Asumimos el primero
    items = ProductoSucursal.objects.filter(producto=producto)
    serializer = ProductoSucursalSerializer(items, many=True)
    return Response(serializer.data)