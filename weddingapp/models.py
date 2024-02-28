from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db.models import Q
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        VENDOR = "VENDOR", "Vendor"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=50, choices=Role.choices)
    verification_code = models.CharField(max_length=32, blank=True)  # Field to store the verification code
    is_verified = models.BooleanField(default=False)

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    document = models.FileField(upload_to='vendor_documents/')

class GoldPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 
    is_confirmed=models.BooleanField(default=False)
    
    applicants = models.ManyToManyField(VendorProfile, related_name='gold_package_applicants', blank=True)

class SilverPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 
    is_confirmed=models.BooleanField(default=False)

    applicants = models.ManyToManyField(VendorProfile, related_name='silver_package_applicants', blank=True)

class PlatinumPackage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=255)
    honeymoon_destination=models.CharField(max_length=255)
    is_booked = models.BooleanField(default=False) 
    is_confirmed=models.BooleanField(default=False)

    applicants = models.ManyToManyField(VendorProfile, related_name='platinum_package_applicants', blank=True)

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
    is_booked=models.BooleanField(default=False)
    billing_info=models.IntegerField()
    is_confirmed=models.BooleanField(default=False)

    applicants = models.ManyToManyField(VendorProfile, related_name='customise_package_applicants', blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    booked_package = models.CharField(max_length=100, default="Not booked")
    profile_image = models.ImageField(default='default_avatar.jpeg', upload_to='profile_images/', blank=True, null=True)





class Package(models.Model):
    name = models.CharField(max_length=100)


class Booking(models.Model):
    date_of_booking = models.DateField()
    destination_selected = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# Chat Room Models
class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs
    
class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)