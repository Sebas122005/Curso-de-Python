from django.db import models

# Create your models here.

class Lenguaje(models.Model):
    nombre=models.CharField(max_length=100,verbose_name='Lenguaje')
    def __str__(self):
        fila=self.nombre
        return fila

class SO(models.Model):
    nombre=models.CharField(max_length=100,verbose_name='SO')

    def __str__(self):
        fila=self.nombre
        return fila
    
class Cliente(models.Model):
    nombre=models.CharField(max_length=50,verbose_name='Nombre')
    apellido_paterno=models.CharField(max_length=50,verbose_name='Apellido Paterno')
    apellido_materno=models.CharField(max_length=50,verbose_name='Apellido Materno')
    foto=models.ImageField(upload_to='imagenes/',verbose_name='Foto',null=True)
    lenguaje=models.ForeignKey(Lenguaje, verbose_name="Lenguaje", on_delete=models.CASCADE)
    so=models.ForeignKey(SO, verbose_name="Sistema Operativo", on_delete=models.CASCADE)

    def __str__(self):
        fila= "Id: "+ str(self.id)+' - Nombre: '+self.nombre+' - Apellidos: '+self.apellido_paterno+self.apellido_materno
        return fila
    
    def delete(self, using = ..., keep_parents = ...):
        self.foto.storage.delete(self.foto.name)
        return super().delete()
