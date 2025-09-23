from django.shortcuts import render
from .models import *
from .forms import ClienteForm
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse


# Create your views here.
class Inicio(TemplateView):
    template_name='pages/inicio.html'

class Lista(ListView):
    template_name='crud/listado.html'
    model=Cliente
    ordering='nombre'
    queryset=Cliente.objects.all()
    context_object_name='clientes'

class Crear(CreateView):
    template_name='crud/crear.html'
    model=Cliente
    #fields = '__all__'
    form_class=ClienteForm
    context_object_name='formulario'

    def get_success_url(self,**kwargs):
        return reverse('clientes_app:lista')
