from django.contrib import admin
from .models import User
from .models import GoldPackage,SilverPackage,PlatinumPackage,CustomisePackage,Booking,VendorProfile,Review,Payment_silver,Payment_customise,Payment_platinum,Payment_gold
from .models import Thread, ChatMessage
# Register your models here.
admin.site.register(User)
admin.site.register(GoldPackage)
admin.site.register(SilverPackage)
admin.site.register(PlatinumPackage)
admin.site.register(CustomisePackage)
admin.site.register(Booking)
admin.site.register(ChatMessage)
admin.site.register(VendorProfile)
admin.site.register(Review)
admin.site.register(Payment_silver)
admin.site.register(Payment_gold)
admin.site.register(Payment_platinum)
admin.site.register(Payment_customise)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)