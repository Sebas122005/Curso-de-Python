from django.db import models

# Create your models here.
class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40,verbose_name='Nombre')
    apellido_paterno = models.CharField(max_length=40,verbose_name='Apellido Paterno')
    apellido_materno = models.CharField(max_length=40,verbose_name='Apellido Materno')
    direccion = models.CharField(max_length=100,null=True,verbose_name='Dirección')
    foto = models.ImageField(upload_to='imagenes/',verbose_name='Foto',null=True)

    def __str__(self):
        fila="Id: "+str(self.id)+" - "+"Nombre: "+self.nombre+" - "+"Apellido Paterno: "+self.apellido_paterno+" - "+"Apellido Materno: "+self.apellido_materno
        return fila
    
    def delete(self, using=None,Keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()

