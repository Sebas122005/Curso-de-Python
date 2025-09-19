from socket import fromshare
from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        fields='__all__'