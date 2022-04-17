from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from requests import request
from .models import Person, User, Patient, Room
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.contrib import messages

@login_required()
def dashboard(request):
    contador_pacientes = list(Patient.objects.all().values_list('last_nameReference', flat=True)).count() if Patient.objects.all() else 0
    contador_miembros_equipo = 0
    contador_habitaciones = 0
    #list(Patient.objects.all().values_list('last_nameReference', flat=True)).count() if Patient.objects.all() else 0

    context = {
        "name":request.user,
        "contador_pacientes":contador_pacientes,
        "contador_miembros_equipo":str(contador_miembros_equipo),
        "contador_habitaciones":str(contador_habitaciones)
        } 
    return render(request, 'salusApp/dashboard-Home.html', context=context)

def home(request):
    return render(request,'salusApp/home.html')

class register_view(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home')
    template_name = "registration/signup.html"

@login_required
def change_password_success(request):
    return render(request, 'registration/password_change_complete.html')

@login_required()
def dashboard_clinica(request):
    context = {"name":request.user} #Sending data from the request
    return render(request, 'salusApp/dashboard-miClinica.html', context)

@login_required()
def dashboard_equipo(request):
    context = {}
    return render(request, 'salusApp/dashboard-equipo.html', context)

@login_required()
def dashboard_equipo_doctores(request):
    context = {}
    return render(request, 'salusApp/dashboard-equipo-doctores.html', context)

@login_required()
def dashboard_equipo_pacientes(request):
    context = {}
    return render(request, 'salusApp/dashboard-equipo-pacientes.html', context)

@login_required()
def dashboard_equipo_enfermeros(request):
    context = {}
    return render(request, 'salusApp/dashboard-equipo-enfermeros.html', context)