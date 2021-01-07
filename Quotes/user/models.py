from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models

class User(AbstractUser):
    name = models.CharField(blank=True, max_length=255, null=True)
    # uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=500, unique=True)
    nickname = models.CharField(max_length=50,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='images/',blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verfiied=models.BooleanField(default=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.email