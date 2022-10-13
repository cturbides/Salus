"""Imports"""
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from requests import request
from .models import Person, Sensors, User, Patient, Room
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

#=======================DASHBOARD=======================
@login_required()
def dashboard(request):
    patient_counter = len(Patient.objects.all()) if Patient.objects.all() else 0
    member_team_counter = len(Person.objects.filter(is_nurse=True)) + len(Person.objects.filter(is_doctor=True))
    room_counter = abs(len(Room.objects.all()) - len(Patient.objects.all())) if Room.objects.all() else 0
    patients_list = Patient.objects.all()
    
    context = {
        "user_name":request.user,
        "patient_counter":patient_counter,
        "member_team_counter":member_team_counter,
        "room_counter": room_counter,
        "patients_list":patients_list,
    } 
    return render(request, 'salusApp/dashboard-Home.html', context=context)
#=======================DASHBOARD=======================


#=========================HOME==========================
def home(request):
    return render(request,'salusApp/home.html')
#=========================HOME==========================


#====================LOGIN & REGISTER===================
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
#====================LOGIN & REGISTER===================


#=======================CHANGE PASSWORD=======================
@login_required()
def change_password_success(request):
    return render(request, 'registration/password_change_complete.html')
#=======================CHANGE PASSWORD=======================


#==========================MI-CLINICA=========================
@login_required()
def dashboard_clinica(request):
    room_counter = len(Patient.objects.all())
    last_patient = None
    patients_list, rooms, sensors = list(), list(), list()

    if room_counter:
        patient_list = Patient.objects.all()
        last_patient = patients_list[room_counter-1]
    
    if Room.objects.filter(is_available=True):
        rooms =  Room.objects.filter(is_available=True)

    if len(Sensors.objects.all()):
        sensors = Sensors.objects.all()
        sensors = sensors[len(Sensor.objects.all())-1]

    team_members_counter = room_counter - len(Person.objects.filter(is_doctor=False, is_nurse=False))

    context = {
        "room_counter":room_counter,
        "team_members_counter":team_members_counter,
        "patients_list":patients_list,
        "rooms":rooms,
        "sensors":sensors,
        "last_patient":last_patient
    } 
    return render(request, 'salusApp/dashboard-miClinica.html', context)

@login_required()
def dashboard_clinica_room(request, room_id):
    room = Room.objects.filter(id=room_id)[0]
    patient = Patient.objects.filter(room=room)[0]
    context = {
        "patient":patient,
        "room_id":room_id,
    }
    return render(request, 'salusApp/dashboard-miClinica-room.html', context)
#==========================MI-CLINICA=========================


#=============================EQUIPO==========================
@login_required()
def dashboard_equipo(request):
    persons, nurses, doctors, patients = Person.objects.all(), \
        Person.objects.filter(is_nurse=True), \
        Person.objects.filter(is_doctor=True),\
        Patient.objects.all()

    last_person, last_nurse, last_doctor, last_patient = None, None, None, None

    if len(persons):
        last_person = persons[len(persons)-1]
    if len(nurses):
        last_nurse = nurses[len(nurses)-1]
    if len(doctors):
        last_doctor = doctors[len(doctors)-1]
    if len(patients):
        last_patient = patients[len(patients)-1]
    
    context = {
        "nurse":last_nurse,
        "person":last_person,
        "doc":last_doctor,
        "patient":last_patient 
    }

    return render(request, 'salusApp/dashboard-equipo.html', context)

#=============================EQUIPO==========================


#===========================PACIENTES==========================
@login_required()
def Pacientes(request):
    pacientes = Patient.objects.all()
    context = {"pacientes":pacientes}
    return render(request, 'salusApp/dashboard-equipo-pacientes.html', context)

@login_required()
def PacientesCreate(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
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
                id_card_number=request.POST['idNumber'],
                is_doctor=False,
                is_nurse=False
            )
            nurse = Person.objects.filter(pk=request.POST['nurse'], isNurse=True)[0]
            doctor = Person.objects.filter(pk=request.POST['doctor'], isDoctor=True)[0]
            room = Room.objects.filter(pk=request.POST['room'])[0]
            name_reference = request.POST['first_nameReference']
            lastName_reference = request.POST['last_nameReference']
            phone_reference = request.POST['phone_reference']
            kinship_reference = request.POST['kinshipReference']
            weight = float(request.POST['weight_in_pounds'])
            height = float(request.POST['height_in_meters'])
            weight_in_kg = weight*0.453592
            bmi = weight_in_kg/(height**2)
            blood = request.POST['bloodType']
            ars = request.POST['ars']
            joining_date = datetime.today().strftime('%Y-%m-%d')
            illness = request.POST['illness']
            hospitalization = request.POST['hospitalization']
            
            newPatient = Patient(
                person=person,
                nurse=nurse,
                doctor=doctor,
                room=room,
                first_nameReference=name_reference,
                last_nameReference=lastName_reference,
                kinshipReference=kinship_reference,
                phone_reference=phone_reference,
                bmi=bmi,
                weight_in_pounds=weight,
                height_in_meters=height,
                bloodType=blood,
                ars=ars,
                join_date=joining_date,
                illness=illness,
                hospitalization=hospitalization
            )
            person.save()
            newPatient.save()           
            room.isAvailable = False
            room.save()
            return redirect('pacientes')
        except Exception as e:
            return HttpResponse(e)
    else:
        enfermeras = Person.objects.filter(isNurse=True)
        doctores = Person.objects.filter(isDoctor=True)
        room = Room.objects.filter(isAvailable=True)
        context = {
            "enfermeras":enfermeras, 
            "doctors":doctores, 
            "rooms":room
        }
        return render(request, 'registration/addPaciente.html', context)

@login_required()
def PacientesDelete(request, pk):
    if request.method == "GET":
        paciente = Patient.objects.filter(pk=pk)[0]
        paciente.room.isAvailable = True
        paciente.room.save()
        paciente.persona.delete()
        return redirect('pacientes')

@login_required()
def PacientesUpdate(request, pk):
    if request.method == "POST":
        try:
            patient = Patient.objects.filter(pk=pk)[0]
            patient.person.first_name=request.POST['first_name']
            patient.person.last_name=request.POST['last_name']
            if len(request.POST['photo']) > 2:
                patient.person.photo=request.POST['photo']
            patient.person.age=request.POST['age']
            patient.person.address=request.POST['address']
            patient.person.sex=request.POST['sex']
            patient.person.phone=request.POST['phone']
            patient.person.idNumber=request.POST['idNumber']
            
            patient.nurse = Person.objects.filter(pk=request.POST['nurse'], isNurse=True)[0]
            patient.doctor = Person.objects.filter(pk=request.POST['doctor'], isDoctor=True)[0]
            
            if request.POST['room'] != 'None':
                patient.room.isAvailable = True
                patient.room.save()
                patient.room = Room.objects.filter(pk=request.POST['room'])[0]
                patient.room.isAvailable = False
                patient.room.save()
                
            patient.name_reference = request.POST['first_nameReference']
            patient.lastName_reference = request.POST['last_nameReference']
            patient.phone_reference = request.POST['phone_reference']
            patient.kinship_reference = request.POST['kinshipReference']
            patient.weight = float(request.POST['weight_in_pounds'])
            patient.height = float(request.POST['height_in_meters'])
            weight_in_kg = patient.weight*0.453592
            patient.bmi = weight_in_kg/(patient.height**2)
            patient.blood = request.POST['bloodType']
            patient.ars = request.POST['ars']
            patient.illness = request.POST['illness']
            patient.hospitalization = request.POST['hospitalization']
            
            patient.person.save()
            patient.save()           
            return redirect('pacientes')
        except Exception as e:
            return HttpResponse(e)
    else:
        enfermeras = Person.objects.filter(isNurse=True)
        doctores = Person.objects.filter(isDoctor=True)
        room = Room.objects.filter(isAvailable=True)
        paciente = Patient.objects.filter(pk=pk)[0]
        KinshipTypes = [['H','Conyugue'], ['A','Amigo'],['F','Familiar']]
        bloodTypes = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        hospitalizacionChoices = [['U','Urgente'], ['P','Programado'],['I','Intrahospitalario']]
        context = {
            "enfermeras":enfermeras, 
            "doctors":doctores, 
            "rooms":room,
            "patient":paciente,
            "KinshipTypes":KinshipTypes,
            "bloodTypes":bloodTypes,
            "hospitalizacionChoices":hospitalizacionChoices
        }
        return render(request, 'registration/editPaciente.html', context)

#===========================PACIENTES=======================



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