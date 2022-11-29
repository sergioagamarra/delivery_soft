from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    barrio = models.CharField(max_length=50, null=True, default="")
    calle = models.CharField(max_length=50, null=True, default="")
    numero = models.IntegerField(null=True, default=0)
    is_admin = models.BooleanField(null=False, default=False)