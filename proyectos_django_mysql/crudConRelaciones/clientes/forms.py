from socket import fromshare
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model=Cliente
        fields='__all__'
        labels={
            'nombre':'Dame tu nombre',
            'foto':'Ingresa tu foto'
        }

    def __init__(self, *args,**kwargs):
        super(ClienteForm,self).__init__(*args,**kwargs)
        self.fields['lenguaje'].empty_label="Selecciona"
        self.fields['so'].empty_label="Selecciona"
        self.fields['apellido_paterno'].required=True
        self.fields['apellido_materno'].required=False


