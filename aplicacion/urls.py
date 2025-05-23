from django.urls import path
from .views import index, producto_detalle, realizar_venta, buscar_por_nombre

urlpatterns = [
    # Vista principal del frontend
    path('', index, name='index'),

    # API REST
    path('api/productos/<int:producto_id>/', producto_detalle, name='producto-detalle'),
    path('api/productos/nombre/<str:nombre>/', buscar_por_nombre, name='producto-nombre'),
    path('api/venta/', realizar_venta, name='realizar-venta'),
]
