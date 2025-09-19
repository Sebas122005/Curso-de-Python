from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm


# Create your views here.
def inicio(request):
    return render(request,'pages/inicio.html')

def lista(request):
    client = Cliente.objects.all()
    return render(request,'crud/listado.html',{'clientes':client})

def crear_editar(request,id=0):
    if(request.method=='GET'):
        formulario=ClienteForm()
        return render(request,'crud/crear.html',{'formulario':formulario})
    else:
        formulario=ClienteForm(request.POST)
        if(formulario.is_valid()):
            formulario.save()
            return redirect('lista')
