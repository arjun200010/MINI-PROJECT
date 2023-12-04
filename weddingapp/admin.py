from django.contrib import admin
from .models import User
from .models import GoldPackage,SilverPackage,PlatinumPackage,CustomisePackage,Booking

# Register your models here.
admin.site.register(User)
admin.site.register(GoldPackage)
admin.site.register(SilverPackage)
admin.site.register(PlatinumPackage)
admin.site.register(CustomisePackage)
admin.site.register(Booking)
