from django.urls import path, include
from .views import index

urlpatterns = [
    #URL DE APLICACION
    path('', index, name='index'),
]
