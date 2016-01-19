from django import forms
from django.contrib.auth.models import User
from rango.models import Tapas, Bares, PerfilUsuario

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ('web', 'imagen',)

class FormularioTapas(forms.ModelForm):
    nombre = forms.CharField(max_length=60,widget=forms.TextInput(attrs={'placeholder':'nombre de la tapa','class':'form-control'}))
    votos = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Tapas
        
        fields=('nombre',)