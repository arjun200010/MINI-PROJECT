from django.contrib import admin
from .models import User
from .models import GoldPackage,SilverPackage,PlatinumPackage

# Register your models here.
admin.site.register(User)
admin.site.register(GoldPackage)
admin.site.register(SilverPackage)
admin.site.register(PlatinumPackage)
