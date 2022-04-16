from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Person(models.Model):
    first_name = models.CharField("Person's first name", max_length=30)
    last_name = models.CharField("Person's last name",max_length=30)
    photo = models.CharField("Person's photo direction",max_length=100)
    age = models.IntegerField("Person's age")    
    residence = models.CharField("Person's residence direction", max_length=100)
    sexoChoices = [
        ('M', "Masculino"),
        ('F', "Femenino")
    ]
    sex = models.CharField("Person's sex", choices=sexoChoices, max_length=1)
    phone = models.CharField("Person's phone", max_length=15)
    idNumber = models.CharField("Person's id", max_length=10) #Cedula
    isDoctor = models.BooleanField("Is this Person a doctor?")
    isNurse = models.BooleanField("Is this Person a nurse?")


class Room(models.Model):
    roomTemperature = models.FloatField("Room's Temperature")
    patientTemperature = models.FloatField("Patient's Temperature")
    roomHumidity = models.FloatField("Room's relative humidity %")
    roomDustLevel = models.IntegerField("Room's dust level in %")
    roomAirQuality = models.IntegerField("Room's AirQuality in %")
    patientPulse = models.FloatField("Patient's pulse value")
    #emc -> unconfirmed
    
class Patient(models.Model):
    person = models.ManyToManyField(Person)
    nurse = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="nurse")
    doctor = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="doctor")
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    first_nameReference = models.CharField("Reference Person's first name", max_length=15)
    last_nameReference = models.CharField("Reference Person's last name", max_length=15)
    KinshipChoices = [
        ('H', "Esposo"), #H -> Husband
        ('A', "Amigo"),
        ('F', "Familiar")
    ]
    kinshipReference = models.CharField("Reference Person's kinshipness", choices=KinshipChoices, max_length=1)
    phone_reference = models.CharField("Reference person's phone number", max_length=15)
    bmi = models.FloatField("Person's BMI") #IMC
    bloodTypes = [
        ('O+', 'O Positivo'),
        ('O-', 'O Negativo'),
        ('A+', 'A Positivo'),
        ('A-', 'A Negativo'),
        ('B+', 'B Positivo'),
        ('B-', 'B Negativo'),
        ('AB+','AB Positivo'),
        ('AB-','AB Negativo')
    ]
    bloodType = models.CharField(choices=bloodTypes, max_length=3)
    ars = models.CharField("Person's ARS type", max_length=15)
    join_date = models.DateField("Person's joining date")
    illness = models.CharField("Persons's illness", max_length=50)
    hospitalizationChoices = [
        ('U', "Urgente"),
        ('P', "Programado"),
        ('I', "Intrahospitalario")
    ]
    hospitalization = models.CharField("Patient's type of hospitalization", max_length=1, choices=hospitalizationChoices)
    
