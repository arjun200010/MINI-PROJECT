from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        VENDOR = "VENDOR", "Vendor"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=50, choices=Role.choices)
    verification_code = models.CharField(max_length=32, blank=True)  # Field to store the verification code
    is_verified = models.BooleanField(default=False)

class GoldPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    # Other fields specific to the Gold package
    is_booked = models.BooleanField(default=False) 

class SilverPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 
    # Other fields specific to the Silver package

class PlatinumPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 
    # Other fields specific to the Platinum package
