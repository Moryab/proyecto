from django.urls import path
from .views import index, producto_detalle, realizar_venta, buscar_por_nombre, convertir_clp_a_usd, sse_stock, addproduc

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # Vista principal del frontend
    path('', index, name='index'),
    path('addproduc/', addproduc, name='addproduc'),

    # API REST
    path('api/productos/<int:producto_id>/', producto_detalle, name='producto-detalle'),
    path('api/productos/nombre/<str:nombre>/', buscar_por_nombre, name='producto-nombre'),
    path('api/venta/', realizar_venta, name='realizar-venta'),
    path("api/convertir-clp-a-usd/", convertir_clp_a_usd),
    path('sse/stock/', sse_stock, name='sse_stock'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)