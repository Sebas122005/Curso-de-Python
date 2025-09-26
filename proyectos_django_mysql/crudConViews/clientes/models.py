from django.db import models

# Create your models here.


class Lenguaje(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Lenguaje')

    def __str__(self):
        fila = self.nombre
        return fila


class SO(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='SO')

    def __str__(self):
        fila = self.nombre
        return fila


Area = (('Front', 'Front'), ('Backend', 'Backend'), ('FullStack', 'FullStack'))

class Cliente(models.Model):
    nombre=models.CharField(max_length=50,verbose_name="Nombre")
    apellido_paterno=models.CharField(max_length=50,verbose_name="Apellido Paterno")
    apellido_materno=models.CharField(max_length=50,verbose_name="Apellido Materno")
    edad=models.IntegerField(max_length=4,verbose_name="Edad")
    foto = models.ImageField(upload_to='imagenes/',verbose_name="Foto",null=True)
    lenguaje=models.ForeignKey(Lenguaje,verbose_name="Lenguaje",on_delete=models.CASCADE)
    so=models.ForeignKey(SO,verbose_name="SO",on_delete=models.CASCADE)
    area= models.CharField(max_length=50,verbose_name="Area",choices=Area)

    def __str__(self):
        fila=str(self.id)+ " - "+self.nombre
        return fila
    
    def delete(self, using=None,Keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()
