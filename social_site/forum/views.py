from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from .forms import DiscussioneModelForm, PostModelForm
from .mixins import StaffMixin
from .models import Discussione, Post, Sezione

class CreaSezione(StaffMixin, CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "forum/crea_sezione.html"
    success_url = "/"


def visualizza_sezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    discussioni_sezione = Discussione.objects.filter(
        sezione_appartenenza = sezione
    ).order_by("-data_creazione")
    context = {"sezione": sezione, "discussioni": discussioni_sezione}
    return render(request, "forum/singola_sezione.html", context) 

@login_required
def crea_discussione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == 'POST': 
        form = DiscussioneModelForm(request.POST)
        if form.is_valid():
            discussione = form.save(commit=False) #commit=False, ti sospende il salavataggio del form per andare ad aggiungere altri dati
            discussione.sezione_appartenenza = sezione
            discussione.autore_discussione = request.user
            discussione.save() #Qui viene richiamato il save
            primo_post = Post.objects.create( #Qui vado a creare anche il post
                discussione = discussione,
                autore_post = request.user,
                contenuto = form.cleaned_data["contenuto"]
            )
            return HttpResponseRedirect(discussione.get_absolute_url())
    else:
        form = DiscussioneModelForm()
    context = {"form": form, "sezione": sezione}
    return render(request, "forum/crea_discussione.html", context) 


def visualizza_discussione(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    posts_discussione = Post.objects.filter(discussione = discussione)
    form_risposta = PostModelForm()
    context = {
        "discussione": discussione,
        "posts_discussione": posts_discussione,
        "form_risposta": form_risposta
        }
    return render(request, "forum/singola_discussione.html", context)

@login_required
def aggiungi_risposta(request, pk): #Pk, chiave pirmaria che si riferisce al post che staimo rispondendo
    discussione = get_object_or_404(Discussione, pk=pk) 
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.discussione = discussione
            form.instance.autore_post = request.user
            form.save()
            url_discussione = reverse("visualizza_discussione", kwargs={"pk": pk})
            return HttpResponseRedirect(url_discussione)
    else:
        return HttpResponseBadRequest()


