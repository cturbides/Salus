"""Imports"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from salusApp.models import Person, Sensors, User, Patient, Room
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from datetime import datetime
import uuid

#=======================DASHBOARD=======================
@login_required()
def show_dashboard(request):
    patient_counter, room_counter = 0, 0
    
    if len(Patient.objects.all()):
        patient_counter = len(Patient.objects.all()) 
    
    if len(Room.objects.all()):
        room_counter = len(Room.objects.all()) - len(Patient.objects.all())
        room_counter = 0 if room_counter < 0 else room_counter
        
    member_team_counter = len(Person.objects.filter(is_nurse=True)) + len(Person.objects.filter(is_doctor=True))
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
def show_clinic(request):
    active_room_counter = len(Patient.objects.all())
    last_patient = None
    patients_list, rooms, sensors = list(), list(), dict()

    if active_room_counter:
        patients_list = Patient.objects.all()
        last_patient = patients_list[active_room_counter-1]
        
        is_sensors_data = Sensors.objects.all()
        if len(is_sensors_data):
            for patient in patients_list:
                sensor_data = Sensors.objects.filter(room=patient.room)
                if sensor_data:
                    sensors[patient.room.id] = sensor_data[len(sensor_data)-1]
    
    if Room.objects.filter(is_available=True):
        rooms = Room.objects.filter(is_available=True)

    team_members_counter = len(Person.objects.filter(is_doctor=True)) + len(Person.objects.filter(is_nurse=True))

    context = {
        "active_room_counter":active_room_counter,
        "team_members_counter":team_members_counter,
        "patients_list":patients_list,
        "rooms":rooms,
        "sensors":sensors,
        "last_patient":last_patient
    } 
    return render(request, 'salusApp/dashboard-miClinica.html', context)

@login_required()
def show_clinic_room(request, room_uuid):
    try:
        room = Room.objects.get(uuid=room_uuid)
        sensor = Sensors.objects.get(room=room)
        patient = Patient.objects.get(room=room)
        
        context = {
            "patient":patient,
            "room_uuid":room_uuid,
        }
        return render(request, 'salusApp/dashboard-miClinica-room.html', context)
    except:
        return redirect('mi-clinica')
#==========================MI-CLINICA=========================


#=============================EQUIPO==========================
@login_required()
def show_team(request):
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
def show_patient_list(request):
    patients = Patient.objects.all()
    context = {"patients":patients}
    return render(request, 'salusApp/dashboard-equipo-pacientes.html', context)

@login_required()
def create_patient(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
    if request.method == "POST":
        try:
            person = Person(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                photo=request.FILES['photo'],
                age=request.POST['age'],
                address=request.POST['address'],
                sex=request.POST['sex'],
                phone=request.POST['phone'],
                id_card_number=request.POST['id_card_number'],
                is_doctor=False,
                is_nurse=False
            )
            nurse = Person.objects.filter(pk=request.POST['nurse'], is_nurse=True)[0]
            doctor = Person.objects.filter(pk=request.POST['doctor'], is_doctor=True)[0]
            room = Room.objects.filter(pk=request.POST['room'])[0]
            reference_first_name = request.POST['reference_first_name']
            reference_last_name = request.POST['reference_last_name']
            reference_phone = request.POST['reference_phone']
            reference_kindship = request.POST['reference_kindship']
            weight = float(request.POST['weight_in_pounds'])
            height = float(request.POST['height_in_meters'])
            weight_in_kg = weight*0.453592
            bmi = weight_in_kg/(height**2)
            person_blood_type = request.POST['person_blood_type']
            ars = request.POST['ars']
            joining_date = datetime.today().strftime('%Y-%m-%d')
            illness = request.POST['illness']
            hospitalization = request.POST['hospitalization']
            
            new_patient = Patient(
                uuid=str(uuid.uuid4()),
                person=person,
                nurse=nurse,
                doctor=doctor,
                room=room,
                reference_first_name=reference_first_name,
                reference_last_name=reference_last_name,
                reference_kindship=reference_kindship,
                reference_phone=reference_phone,
                bmi=bmi,
                weight_in_pounds=weight,
                height_in_meters=height,
                person_blood_type=person_blood_type,
                ars=ars,
                join_date=joining_date,
                illness=illness,
                hospitalization=hospitalization
            )

            person.save()
            new_patient.save()           
            room.is_available = False
            room.save()
            return redirect('pacientes')
        except Exception as e:
            return HttpResponse(e)
    
    nurses = Person.objects.filter(is_nurse=True)
    doctors = Person.objects.filter(is_doctor=True)
    rooms = Room.objects.filter(is_available=True)
    context = {
        "nurses":nurses, 
        "doctors":doctors, 
        "rooms":rooms
    }
    return render(request, 'registration/addPaciente.html', context)

@login_required()
def delete_patient(request, patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except:
        return redirect('pacientes')
    
    patient.room.is_available = True
    patient.room.save()
    patient.person.delete()
    return redirect('pacientes')

@login_required()
def update_patient(request, patient_uuid):
    try:
        patient = Patient.objects.get(uuid=patient_uuid)
    except:
        return redirect('pacientes')
    
    if request.method == "POST":
        try:
            patient.person.first_name=request.POST['first_name']
            patient.person.last_name=request.POST['last_name']
            photo = request.FILES.get('photo', None)
            if photo:
                    patient.person.photo=request.FILES['photo']                    
            patient.person.age=request.POST['age']
            patient.person.address=request.POST['address']
            patient.person.sex=request.POST['sex']
            patient.person.phone=request.POST['phone']
            patient.person.id_card_number=request.POST['id_card_number']
            
            patient.nurse = Person.objects.filter(pk=request.POST['nurse'], is_nurse=True)[0]
            patient.doctor = Person.objects.filter(pk=request.POST['doctor'], is_doctor=True)[0]
            
            if request.POST['room'] != 'None':
                patient.room.is_available = True
                patient.room.save()
                patient.room = Room.objects.filter(pk=request.POST['room'])[0]
                patient.room.is_available = False
                patient.room.save()
                
            patient.reference_first_name = request.POST['reference_first_name']
            patient.reference_last_name = request.POST['reference_last_name']
            patient.reference_phone = request.POST['reference_phone']
            patient.reference_kindship = request.POST['reference_kindship']
            patient.weight_in_pounds = float(request.POST['weight_in_pounds'])
            patient.height_in_meters = float(request.POST['height_in_meters'])
            weight_in_kg = patient.weight_in_pounds*0.453592
            patient.bmi = weight_in_kg/(patient.height_in_meters**2)
            patient.person_blood_type = request.POST['person_blood_type']
            patient.ars = request.POST['ars']
            patient.illness = request.POST['illness']
            patient.hospitalization = request.POST['hospitalization']
            
            patient.person.save()
            patient.save()           
            return redirect('pacientes')
        except:
            return redirect('pacientes')
    
    nurses = Person.objects.filter(is_nurse=True)
    doctors = Person.objects.filter(is_doctor=True)
    rooms = Room.objects.filter(is_available=True)
    kindship_types = [['H','Conyugue'], ['A','Amigo'],['F','Familiar'], ['O', 'Otro']]
    blood_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    hospitalization_types = [['U','Urgente'], ['P','Programado'],['I','Intrahospitalario']]
        
    context = {
        "nurses":nurses, 
        "doctors":doctors, 
        "rooms":rooms,
        "patient":patient,
        "kindship_types":kindship_types,
        "blood_types":blood_types,
        "hospitalization_types":hospitalization_types
    }
    return render(request, 'registration/editPaciente.html', context)
#===========================PACIENTES=======================



#===========================DOCTORES========================
@login_required()
def show_doctors_list(request):
    doctors = Person.objects.filter(is_doctor=True)
    context = {"doctors":doctors}
    return render(request, 'salusApp/dashboard-equipo-doctores.html', context)
  
@login_required()
def create_doctor(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
    context = {"is_doctor": True}
    if request.method == "POST":
        person = Person(
            uuid=str(uuid.uuid4()),
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            photo=request.FILES['photo'],
            age=request.POST['age'],
            address=request.POST['address'],
            sex=request.POST['sex'],
            phone=request.POST['phone'],
            id_card_number=request.POST['id_card_number'],
            is_doctor=True,
            is_nurse=False
        )
        person.save()
        return redirect('doctores')
    return render(request, 'registration/addPersona.html', context)

@login_required()
def delete_doctor(request, doctor_uuid):
    try:
        doctor = Person.objects.get(uuid=doctor_uuid)
        doctor.delete()
        return redirect('doctores')
    except:
        return redirect('equipo')

@login_required()
def update_doctor(request, doctor_uuid):
    try:
        person = Person.objects.get(uuid=doctor_uuid)
    except:
        return redirect('doctores')
        
    if request.method == "POST":
        person.first_name = request.POST['first_name']
        person.last_name = request.POST['last_name']
        person.age = request.POST['age']
        person.address = request.POST['address']
        person.sex = request.POST['sex']
        person.phone = request.POST['phone']
        person.id_card_number = request.POST['id_card_number']
        photo = request.FILES.get('photo', None)
        if photo:
            person.photo = request.FILES['photo']
        person.save()
        return redirect('doctores')

    context = {"person":person}
    return render(request, 'registration/editPersona.html', context)

#===========================DOCTORES========================


#===========================ENFERMEROS==========================
@login_required()
def show_nurses_list(request):
    nurses = Person.objects.filter(is_nurse=True)
    context = {"nurses":nurses}
    return render(request, 'salusApp/dashboard-equipo-enfermeros.html', context)
  
@login_required()
def create_nurses(request): #Mejorar el agregado de datos -> Convertirlo implementando el CreateView y Form
    context = {"is_nurse": True}
    if request.method == "POST":
        try:
            person = Person(
                uuid=str(uuid.uuid4()),
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                photo=request.FILES['photo'],
                age=request.POST['age'],
                address=request.POST['address'],
                sex=request.POST['sex'],
                phone=request.POST['phone'],
                id_card_number=request.POST['id_card_number'],
                is_doctor=False,
                is_nurse=True
            )
            person.save()
            return redirect('enfermeros')
        except:
            return redirect('equipo')
    return render(request, 'registration/addPersona.html', context)

@login_required()
def delete_nurses(request, nurse_uuid):
    try:
        nurse = Person.objects.get(uuid=nurse_uuid)
        nurse.delete()
    except:
        return redirect('enfermeros')

@login_required()
def update_nurses(request, nurse_uuid):
    try:
        person = Person.objects.get(uuid=nurse_uuid)
    except:
        return redirect('enfermeros')
    
    if request.method == "POST":
        person.first_name = request.POST['first_name']
        person.last_name = request.POST['last_name']
        person.age = request.POST['age']
        person.address = request.POST['address']
        person.sex = request.POST['sex']
        person.phone = request.POST['phone']
        person.id_card_number = request.POST['id_card_number']
        photo = request.FILES.get('photo', None)
        if photo:
            person.photo = request.FILES['photo']
        person.save()
        return redirect('enfermeros')
    
    context = {"person":person}
    return render(request, 'registration/editPersona.html', context)
#===========================ENFERMEROS=======================


#==========================CONFIGURACION=====================
@login_required()
def show_settings(request):
    context = {
        "name":request.user.username,
        "password":request.user.password,
        "is_admin":bool(request.user.is_super),
        "id":request.user.id
    }
    return render(request, 'salusApp/dashboard_configuracion.html', context)

@login_required()
def delete_user(request):
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

#===========================ROOMS & SENSORS==================
@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST['room_name']
        if name:
            new_room = Room(uuid=str(uuid.uuid4()), room_name=name)
            new_room.save()
            #Proof Sensors
            new_sensor_data = Sensors(room=new_room, room_temperature=18.5, room_humidity=60, room_dust_level=30, room_air_quality=79, patient_temperature=28, patient_pulse=83, patient_electro=34)
            new_sensor_data.save()
            return redirect('mi-clinica')
        else:
            None # Flash message
    return render(request, 'registration/addRoom.html')

@login_required
def edit_room(request, room_uuid):
    try:
        room = Room.objects.get(uuid=room_uuid)
    except:
        return redirect('mi-clinica')
    
    if request.method == 'POST':
        name = request.POST['room_name']
        if name:
            room.room_name = name
            room.save()
        else:
            None #Error message
        return redirect('mi-clinica')

    context = {'room_name':room.room_name}
    return render(request, 'registration/addRoom.html', context)

@login_required
def delete_room(request, room_uuid):
    try:
        room = Room.objects.get(uuid=room_uuid)
        
        if len(Patient.objects.filter(room=room)):
            raise Exception
    except:
        #Flash message
        return redirect('mi-clinica')
    
    sensors = Sensors.objects.filter(room=room)
    for sensor_data in sensors:
        sensor_data.delete()
    room.delete()
    return redirect('mi-clinica')