from distutils.command.upload import upload
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email, username, password):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,username, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email address", max_length=300, unique=True, default=None)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_super = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()
    
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    
class Person(models.Model):
    first_name = models.CharField("Person's first name", max_length=30)
    last_name = models.CharField("Person's last name",max_length=30)
    photo = models.ImageField(blank=True, null=False)
    age = models.IntegerField("Person's age")    
    address = models.CharField("Person's address", max_length=100)
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
    roomName = models.CharField(max_length=30)
    isAvailable = models.BooleanField(default=True)
    
class Sensores(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    roomTemperature = models.FloatField("Room's Temperature")
    patientTemperature = models.FloatField("Patient's Temperature")
    roomHumidity = models.FloatField("Room's relative humidity %")
    roomDustLevel = models.IntegerField("Room's dust level in %")
    roomAirQuality = models.IntegerField("Room's AirQuality in %")
    patientPulse = models.FloatField("Patient's pulse value")
    
class Patient(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
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
    weight_in_pounds = models.FloatField("Perons's Weight")
    height_in_meters = models.FloatField("Perons's Height")
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
    
