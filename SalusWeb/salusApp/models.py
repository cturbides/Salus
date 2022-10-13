from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

"""
5 models or tables:
    -User
    -Person -> oneToMany
    -Room -> oneToMany
    -Sensores -> manyToOne
    -Patient -> Use Person table
"""

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
    """
    PERSON DATA:
        -First name
        -Last name
        -Photo file
        -Address direction
        -Age
        -Sex
        -Phone number
        -ID number
        -isDoctor -> bool
        -isNurse -> bool
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo = models.ImageField(blank=True, null=False, upload_to='salusApp/static/media/')
    age = models.IntegerField()    
    address = models.CharField(max_length=100)
    sex_choices = [
        ('M', "Masculino"),
        ('F', "Femenino"),
        ('O', 'Otro'),
        ('NA', 'Prefiero no decirlo')
    ]
    sex = models.CharField(choices=sex_choices, max_length=2)
    phone = models.CharField(max_length=15)
    id_card_number = models.CharField(max_length=10) #Cedula
    is_doctor = models.BooleanField()
    is_nurse = models.BooleanField()


class Room(models.Model):
    """
    ROOM DATA:
        -Room name
        -isAvailable -> bool
    """
    room_name = models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)
    
class Sensors(models.Model):
    """
    SENSOR'S DATA:
        -Room -> Foreign Key
        -Room Temperature
        -Patient Temperature
        -Room Humidity
        -Room Dust level
        -Room Air Quality
        -Patient Pulse
        -Patient Electro
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_temperature = models.FloatField()
    room_humidity = models.FloatField()
    room_dust_level = models.IntegerField()
    room_air_quality = models.IntegerField()
    
    patient_temperature = models.FloatField()
    patient_pulse = models.FloatField()
    patient_electro = models.IntegerField()
    
class Patient(models.Model):
    """
    PATIENT'S DATA:
        -Person -> Foreign Key
        -Nurse -> Foreign Key
        -Doctor -> Foreign Key
        -Room -> Foreign Key
        -First name -> Patient's Reference (Parent, Friend or related)
        -Last name -> Patient's Reference ...
        -Kinship Reference -> Patient's Reference
        -Phone number -> Patient's Reference
        -BMI
        -Weight in pounds
        -Height in meters
        -Blood type
        -ARS
        -Joining date -> Patient's joining date
        -Illness -> Illness' name
        -Hospitalization type -> Urgent, Programmed and Intrahospitalary
    """
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    nurse = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="nurse")
    doctor = models.ForeignKey(Person, on_delete=models.DO_NOTHING, related_name="doctor")
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING)
    reference_first_name = models.CharField(max_length=15)
    reference_last_name = models.CharField(max_length=15)
    kindship_choices = [
        ('H', "Esposo"), #H -> Husband
        ('A', "Amigo"),
        ('F', "Familiar"),
        ('O', "Otro")
    ]
    reference_kindship = models.CharField(choices=kindship_choices, max_length=1)
    reference_phone = models.CharField(max_length=15)
    bmi = models.FloatField() #IMC
    weight_in_pounds = models.FloatField()
    height_in_meters = models.FloatField()
    blood_types = [
        ('O+', 'O Positivo'),
        ('O-', 'O Negativo'),
        ('A+', 'A Positivo'),
        ('A-', 'A Negativo'),
        ('B+', 'B Positivo'),
        ('B-', 'B Negativo'),
        ('AB+','AB Positivo'),
        ('AB-','AB Negativo')
    ]
    person_blood_type = models.CharField(choices=blood_types, max_length=3)
    ars = models.CharField(max_length=15)
    join_date = models.DateField()
    illness = models.CharField(max_length=50)
    hospitalization_choices = [
        ('U', "Urgente"),
        ('P', "Programado"),
        ('I', "Intrahospitalario")
    ]
    hospitalization = models.CharField(max_length=1, choices=hospitalization_choices)