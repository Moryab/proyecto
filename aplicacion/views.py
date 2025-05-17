from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto, ProductoSucursal
from .serializers import ProductoSucursalSerializer
from django.db.models import Q

import time
from django.http import StreamingHttpResponse
from threading import Event

# Vista para mostrar el frontend (como ya tienes)
def index(request):
    return render(request, "aplicacion/index.html")

# API: obtener stock y precios de un producto por sucursal
@api_view(['GET'])
def producto_detalle(request, producto_id):
    items = ProductoSucursal.objects.filter(producto_id=producto_id)
    serializer = ProductoSucursalSerializer(items, many=True)
    return Response(serializer.data)


# Evento global para simular notificación
stock_bajo_event = Event()
stock_bajo_mensaje = None

def sse_stock_bajo(request):
    def event_stream():
        while True:
            stock_bajo_event.wait()  # Espera hasta que haya un evento
            yield f"data: {stock_bajo_mensaje}\n\n"
            stock_bajo_event.clear()
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response

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
        return Response({
        "error": f'Stock bajo en la sucursal "{producto_sucursal.sucursal.nombre}".'
    }, status=400)

    producto_sucursal.stock -= cantidad
    producto_sucursal.save()
    
    # Si el stock llegó a cero, disparamos un mensaje SSE
    if producto_sucursal.stock == 0:
        global stock_bajo_mensaje
        stock_bajo_mensaje = (
            f"Producto '{producto_sucursal.producto.nombre}' sin stock "
            f"en sucursal '{producto_sucursal.sucursal.nombre}'."
        )
        stock_bajo_event.set()

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