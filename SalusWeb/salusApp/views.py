from cmath import polar
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from requests import request
from .models import Person, User, Patient, Room
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from .forms import PersonCreateForm, PersonUpdateForm


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

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST["email"]
        if password == password2:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.is_active = True
            user.save()
            return redirect('home')
        else:
            return redirect('signup') 
    else:
        return render(request, 'registration/signup.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')
    else:
        return render(request, 'registration/login.html')
        
#=======================CHANGE PASSWORD=======================
@login_required()
def change_password_success(request):
    return render(request, 'registration/password_change_complete.html')
#=======================CHANGE PASSWORD=======================


#==========================MI-CLINICA=========================
@login_required()
def dashboard_clinica(request):
    context = {"name":request.user} #Sending data from the request
    return render(request, 'salusApp/dashboard-miClinica.html', context)
#==========================MI-CLINICA=========================


#=============================EQUIPO==========================
@login_required()
def dashboard_equipo(request):
    personas =  Person.objects.all()
    ultima_persona = personas[len(personas)-1]
    nurses = Person.objects.filter(isNurse=True)
    ultima_nurse = nurses[len(nurses)-1]
    doctors = Person.objects.filter(isDoctor=True)
    ultimo_doc = doctors[len(doctors)-1]
    context = {
        "nurse":ultima_nurse,
        "persona":ultima_persona,
        "doc":ultimo_doc
               }
    return render(request, 'salusApp/dashboard-equipo.html', context)

@login_required()
def dashboard_equipo_pacientes(request):
    context = {}
    return render(request, 'salusApp/dashboard-equipo-pacientes.html', context)
#=============================EQUIPO==========================


#===========================DOCTORES========================
@login_required()
def Doctores(request):
    doctores = Person.objects.filter(isDoctor=True)
    context = {"doctors":doctores}
    return render(request, 'salusApp/dashboard-equipo-doctores.html', context)
  
@login_required()
def DoctoresCreate(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
    context = {"isDoctor":True}
    if request.method == "POST":
        try:
            person = Person(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                photo=request.POST['photo'],
                age=request.POST['age'],
                address=request.POST['address'],
                sex=request.POST['sex'],
                phone=request.POST['phone'],
                idNumber=request.POST['idNumber'],
                isDoctor=True,
                isNurse=False
            )
            person.save()
            return redirect('doctores')
        except:
            return redirect('home')
    else:
        return render(request, 'registration/addPersona.html', context)

@login_required()
def DoctoresDelete(request, pk):
    if request.method == "GET":
        doctor = Person.objects.filter(pk=pk)
        doctor.delete()
        return redirect('doctores')

@login_required()
def DoctoresUpdate(request, pk):
    if request.method == "POST":
        person = Person.objects.filter(pk=pk)[0]
        person.first_name = request.POST['first_name']
        person.last_name = request.POST['last_name']
        person.age = request.POST['age']
        person.address = request.POST['address']
        person.sex = request.POST['sex']
        person.phone = request.POST['phone']
        person.idNumber = request.POST['idNumber']
        if len(request.POST['photo']) > 2:
            person.photo = request.POST['photo']
        person.save()
        return redirect('doctores')
    else:
        doctor = Person.objects.filter(pk=pk)[0]
        context = {"person":doctor}
        return render(request, 'registration/editPersona.html', context)

#===========================DOCTORES========================


#===========================ENFERMEROS==========================
@login_required()
def Enfermeros(request):
    nurses = Person.objects.filter(isNurse=True)
    context = {"nurses":nurses}
    return render(request, 'salusApp/dashboard-equipo-enfermeros.html', context)
  
@login_required()
def EnfermerosCreate(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
    context = {"isEnfermera":True}
    if request.method == "POST":
        try:
            person = Person(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                photo=request.POST['photo'],
                age=request.POST['age'],
                address=request.POST['address'],
                sex=request.POST['sex'],
                phone=request.POST['phone'],
                idNumber=request.POST['idNumber'],
                isDoctor=False,
                isNurse=True
            )
            person.save()
            return redirect('enfermeros')
        except:
            return redirect('home')
    else:
        return render(request, 'registration/addPersona.html', context)

@login_required()
def EnfermerosDelete(request, pk):
    if request.method == "GET":
        nurse = Person.objects.filter(pk=pk)
        nurse.delete()
        return redirect('enfermeros')

@login_required()
def EnfermerosUpdate(request, pk):
    if request.method == "POST":
        person = Person.objects.filter(pk=pk)[0]
        person.first_name = request.POST['first_name']
        person.last_name = request.POST['last_name']
        person.age = request.POST['age']
        person.address = request.POST['address']
        person.sex = request.POST['sex']
        person.phone = request.POST['phone']
        person.idNumber = request.POST['idNumber']
        if len(request.POST['photo']) > 2:
            person.photo = request.POST['photo']
        person.save()
        return redirect('enfermeros')
    else:
        nurse = Person.objects.filter(pk=pk)[0]
        context = {"person":nurse}
        return render(request, 'registration/editPersona.html', context)

#===========================ENFERMEROS=======================


#==========================CONFIGURACION=====================
@login_required()
def dashboard_configuracion(request):
    context = {
        "name":request.user.username,
        "password":request.user.password,
        "isAdmin":bool(request.user.is_super),
        "id":request.user.id
    }
    return render(request, 'salusApp/dashboard_configuracion.html', context)

@login_required()
def delete_user(request, pk):
    context = {"id":request.user.id}
    return render(request, 'registration/delete.html', context)

@login_required
def confirm_delete(request,pk):
    try:
        user = User.objects.get(id=pk)
        user.delete()
        return redirect('home')
    except:
        context = {"message":"You can't do that!"} #Sending an error message!
        return render(request, 'registration/delete.html', context)
    
#==========================CONFIGURACION=====================