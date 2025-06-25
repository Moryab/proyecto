import os
import sys

# Configurar Django
sys.path.append('C:/entorno/proyecto')  # Ajusta esta ruta si es necesario
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

import django
django.setup()

# Importaciones Django
from aplicacion.models import Producto, Sucursal, ProductoSucursal
from django.core.files.base import ContentFile
import uuid
from django.utils.crypto import get_random_string

# Importaciones gRPC
import grpc
from concurrent import futures
import grpc_services.producto_pb2 as producto_pb2
import grpc_services.producto_pb2_grpc as producto_pb2_grpc


import os
import sys

# Configurar Django
sys.path.append('C:/entorno/proyecto')  # Ajusta esta ruta si es necesario
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

import django
django.setup()

# Importaciones Django
from aplicacion.models import Producto, Sucursal, ProductoSucursal
from django.core.files.base import ContentFile
import uuid
from django.utils.crypto import get_random_string

# Importaciones gRPC
import grpc
from concurrent import futures
import grpc_services.producto_pb2 as producto_pb2
import grpc_services.producto_pb2_grpc as producto_pb2_grpc


class ProductoService(producto_pb2_grpc.ProductoServiceServicer):
    def CrearProducto(self, request, context):
        print("DEBUG: tipos recibidos ->",
              type(request.nombre), type(request.sucursal_id),
              type(request.precio), type(request.stock), type(request.imagen))
        try:
            sucursal = Sucursal.objects.get(id=int(request.sucursal_id))

            producto = Producto(nombre=request.nombre)

            if request.imagen:
                nombre_imagen = f'{uuid.uuid4()}.jpg'
                producto.imagen.save(nombre_imagen, ContentFile(request.imagen))
            producto.save()

            stock = int(request.stock)
            precio = float(request.precio)

            producto_sucursal = ProductoSucursal(
                producto=producto,
                sucursal=sucursal,
                stock=stock,
                precio=precio
            )
            producto_sucursal.save()

            return producto_pb2.ProductoResponse(
                exito=True,
                mensaje="Producto guardado con éxito"
            )

        except Exception as e:
            return producto_pb2.ProductoResponse(
                exito=False,
                mensaje=f"Error al guardar producto: {str(e)}"
            )

def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    producto_pb2_grpc.add_ProductoServiceServicer_to_server(ProductoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en puerto 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    servir()



def servir():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    producto_pb2_grpc.add_ProductoServiceServicer_to_server(ProductoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC corriendo en puerto 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    servir()
