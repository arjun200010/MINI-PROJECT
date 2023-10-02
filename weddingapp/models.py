from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN",'Admin'
        VENDOR="VENDOR",'Vendor'
        CUSTOMER="CUSTOMER",'Customer'
    role=models.CharField(max_length=50,choices=Role.choices)