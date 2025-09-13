"""
URL configuration for crud_clientes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import crud_clientes.views.view_index as vi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vi.bienvenida, name="Bienvenida"),
    path('despedida/', vi.despedida, name="Despedida"),
    path('enviar_datos/<str:nombre>/<str:apellido>/<int:edad>/<str:curso>/', vi.enviar_datos, name="Datos enviados"), 
]
