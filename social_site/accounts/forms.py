from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormRegistrazione(UserCreationForm):
    #Campo email, per eventuale reset della password
    email = forms.CharField(max_length=30, required=True, widget=forms.EmailInput())

    class Meta:
        #Selezione modello che andiamo a creare
        model = User
        #Specificazione campi: 
        fields = ['username', 'email', 'password1', 'password2']