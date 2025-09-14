
from django import forms
from .models import Clientes

class ClientesForm(forms.ModelForm):
    class Meta:
        model=Clientes
        fields='__all__'