from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static


app_name= 'clientes_app'
urlpatterns = [
    path('',views.Inicio.as_view(),name='inicio'),
    path('lista',views.Lista.as_view(),name="lista"),
    path('cliente/crear',views.Crear.as_view(),name='crear'),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
