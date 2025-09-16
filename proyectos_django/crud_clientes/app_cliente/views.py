from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Clientes
from .forms import ClientesForm


# Create your views here.


def inicio(request):
    return render(request,'pages/inicio.html')

def nosotros(request):
    return render(request, 'pages/nosotros.html')

def listado_clientes(request):
    clientes= Clientes.objects.all()
    return render(request,'crud/listado.html',{'clientes':clientes})

def crear(request):
    formulario=ClientesForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado-clientes')
    return render(request,'crud/crear.html',{'formulario':formulario})

def eliminar(request,id):
    obj=Clientes.objects.get(id=id)
    obj.delete()
    return redirect('listado-clientes')