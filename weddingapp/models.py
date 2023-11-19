from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.conf import settings
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
    is_booked = models.BooleanField(default=False) 
    

class SilverPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 

class PlatinumPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 

class CustomisePackage(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date_of_booking=models.DateField()
    destination_selected=models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255,null=True,blank=True)
    food=models.CharField(max_length=255)
    hotel=models.CharField(max_length=255)
    videography=models.CharField(max_length=255)
    location=models.CharField(max_length=255,null=True,blank=True)
    photography=models.CharField(max_length=255)
    guest=models.IntegerField()
    food=models.CharField(max_length=255)
    is_booked=models.BooleanField(default=False)
    billing_info=models.IntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    booked_package = models.CharField(max_length=100, default="Not booked")

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    document = models.FileField(upload_to='vendor_documents/')


class Package(models.Model):
    name = models.CharField(max_length=100)


class Booking(models.Model):
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
