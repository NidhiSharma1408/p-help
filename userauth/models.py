from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .validators import validate_name
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username     = models.CharField(blank=True, null=True, max_length = 30)
    first_name   = models.CharField(blank=True, null=True,max_length=30)
    last_name    = models.CharField(blank=True, null=True,max_length=30)
    email        = models.EmailField('email address', unique=True)
    is_active    = models.BooleanField(default=False)
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()
    def __str__(self):
        return self.email
        

class UserProfile(models.Model):
    user         = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='profile')
    name         = models.CharField(max_length = 30,blank=False,validators=[validate_name])
    picture      = models.ImageField(upload_to = 'images/', blank = True, null = True, max_length = 1500)
    address      = models.CharField(max_length=50, blank=True,null=True)
    city         = models.CharField(max_length=50,blank=True,null=True)
    state        = models.CharField(max_length=30,blank=True,null=True)
    phone        = models.CharField(max_length=10,blank=True,null=True)
    covid_patient= models.BooleanField(default=False)
    recovered    = models.BooleanField(default=False)
    got_help     = models.BooleanField(default=False)
    when_recovered=models.DateField(blank=True,null=True)
    want_to_donate=models.BooleanField(default=False)
    blood_grp     =models.CharField(max_length=3,blank=False)
    age = models.PositiveIntegerField(blank=False)
    def can_donate(self):
        return self.covid_patient and self.recovered and timezone.localdate() >= self.when_recovered+timedelta(days=28) and self.age>=18 and self.age<45
    def available_as_donor(self):
        return self.want_to_donate and self.can_donate()
    def needs_help(self):
        return self.covid_patient and not self.recovered and not self.got_help
    def __str__(self):
        return self.user.email
    

class OtpModel(models.Model):
    otp          = models.CharField(max_length = 6)
    otp_email    = models.EmailField()
    time_created = models.IntegerField()
    def __str__(self):
        return f"{self.otp_email} : {self.otp}"