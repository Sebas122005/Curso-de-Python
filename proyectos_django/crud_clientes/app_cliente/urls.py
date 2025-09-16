from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns =[
    path('',views.inicio,name='inicio'),
    path('nosotros',views.nosotros,name='nosotros'),
    path('clientes/listar',views.listado_clientes,name='listado-clientes'),
    path('clientes/crear',views.crear,name='crear-clientes'),
    path('clientes/eliminar/<int:id>',views.eliminar,name='eliminar')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

