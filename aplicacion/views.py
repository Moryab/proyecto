from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Producto, ProductoSucursal, Sucursal
from .serializers import ProductoSucursalSerializer
import redis
from django.http import StreamingHttpResponse
import grpc
import grpc_services.producto_pb2 as producto_pb2
import grpc_services.producto_pb2_grpc as producto_pb2_grpc
from django.contrib import messages

def index(request):
    return render(request, "aplicacion/index.html")

def addproduc(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        sucursal_id = request.POST['categoria']
        precio_str = request.POST['precio']
        stock_str = request.POST.get('stock', '0')  # viene como string, pon '0' por defecto

        # Convertir a tipos adecuados
        try:
            precio = float(precio_str)
        except ValueError:
            messages.error(request, "Precio inválido")
            return redirect('addproduc')

        try:
            stock = int(stock_str)
        except ValueError:
            messages.error(request, "Stock inválido")
            return redirect('addproduc')

        imagen_binaria = request.FILES['imagen'].read()

        respuesta = enviar_a_grpc(nombre, sucursal_id, precio, stock, imagen_binaria)

        if respuesta.exito:
            messages.success(request, 'Producto agregado exitosamente')
            return redirect('addproduc')
        else:
            messages.error(request, respuesta.mensaje)
    
    sucursales = Sucursal.objects.all()
    return render(request, "aplicacion/addproduc.html", {"sucursales": sucursales})

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

def enviar_a_grpc(nombre, sucursal_id, precio, stock, imagen_binaria):
    channel = grpc.insecure_channel('localhost:50051')
    stub = producto_pb2_grpc.ProductoServiceStub(channel)

    # Conversión segura de tipos
    try:
        precio_float = float(precio)
        stock_int = int(stock)
        sucursal_int = int(sucursal_id)  # ✅ esto es lo importante
    except (ValueError, TypeError) as e:
        raise ValueError("Error de conversión en los datos enviados a gRPC: " + str(e))

    request = producto_pb2.ProductoRequest(
        nombre=nombre,
        sucursal_id=sucursal_int,  # ✅ debe ser int
        precio=precio_float,
        stock=stock_int,
        imagen=imagen_binaria
    )

    response = stub.CrearProducto(request)
    return response
