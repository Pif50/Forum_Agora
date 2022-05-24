from multiprocessing import context
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from accounts.forms import FormRegistrazione
# Create your views here.

def registrazione_view(request):
    if request.method == 'POST':
        form = FormRegistrazione(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            #Creaiamo il nostro user che si registrerà:
            User.objects.create_user(
                username = username,
                password = password,
                email = email
            )
            #Autenticazione User:
            user = authenticate(username=username, passowrd=password)
            login(request, user)
            return HttpResponseRedirect("/")
    else: 
        form = FormRegistrazione()
    context = {"form" : form}
    return render(request, "accounts/registrazione.html", context)

