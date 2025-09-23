from django.shortcuts import render, redirect
from .models import Cliente
from .forms import ClienteForm


# Create your views here.
def inicio(request):
    return render(request,'pages/inicio.html')

def lista(request):
    client = Cliente.objects.all()
    return render(request,'crud/listado.html',{'clientes':client})

def crear_editar(request, id=0):
    if(request.method=='GET'):
        if(id==0):
            formulario=ClienteForm()
        else:
            clienteId=Cliente.objects.get(pk=id)
            formulario=ClienteForm(instance=clienteId)
        return render(request,'crud/crear.html',{'formulario':formulario})
    else:
        if id== 0:
            formulario=ClienteForm(request.POST or None, request.FILES or None)
        else:
            clienteId=Cliente.objects.get(pk=id)
            formulario=ClienteForm(request.POST or None, request.FILES or None,instance=clienteId)
        if(formulario.is_valid()):
            formulario.save()
        return redirect('lista')

def eliminar_cliente(request, id=0):
    bc=Cliente.objects.get(pk=id)
    bc.delete()
    return redirect('lista')