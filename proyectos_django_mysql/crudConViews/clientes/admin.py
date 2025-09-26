from django.contrib import admin
from .models import *

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre','apellido_paterno','apellido_materno','edad','lenguaje','so','area','foto']
    search_fields = ['nombre','apellido_paterno','apellido_materno']
    list_filter = ['lenguaje','area']
    list_per_page = 5

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Lenguaje)
admin.site.register(SO)
