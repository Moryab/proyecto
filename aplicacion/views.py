from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto, ProductoSucursal
from .serializers import ProductoSucursalSerializer
import redis
from django.http import StreamingHttpResponse

# Vista para mostrar el frontend (como ya tienes)
def index(request):
    return render(request, "aplicacion/index.html")

# API: obtener stock y precios de un producto por sucursal
@api_view(['GET'])
def producto_detalle(request, producto_id):
    items = ProductoSucursal.objects.filter(producto_id=producto_id)
    serializer = ProductoSucursalSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def convertir_clp_a_usd(request):
    try:
        clp = float(request.GET.get('clp', 0))
        tasa = 940  # Ejemplo de tasa CLP -> USD
        usd = round(clp / tasa, 2)
        return Response({"usd": usd})
    except:
        return Response({"error": "Parámetro inválido"}, status=400)




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
    
        # Verificar si el stock llegó a 0 y publicar en Redis
    if producto_sucursal.stock == 0:
        r = redis.Redis()
        mensaje = f"⚠️ Stock agotado en {producto_sucursal.sucursal.nombre} para '{producto_sucursal.producto.nombre}'"
        r.publish('stock_alerts', mensaje)


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



def sse_stock(request):
    def event_stream():
        r = redis.Redis()
        pubsub = r.pubsub()
        pubsub.subscribe('stock_alerts')

        for message in pubsub.listen():
            if message['type'] == 'message':
                yield f"data: {message['data'].decode('utf-8')}\n\n"
    
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
