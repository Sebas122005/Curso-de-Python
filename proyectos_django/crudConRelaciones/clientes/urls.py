from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',inicio, name='inicio'),
    path('clientes/lista',lista,name='lista'),
    path('<int:id>',crear_editar,name='crear_editar'),
    path('clientes/eliminar/<int:id>',eliminar_cliente,name='eliminar')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

