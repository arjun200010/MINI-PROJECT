from django.contrib import admin
from .models import User
from .models import GoldPackage,SilverPackage,PlatinumPackage,CustomisePackage,Booking
from .models import Thread, ChatMessage
# Register your models here.
admin.site.register(User)
admin.site.register(GoldPackage)
admin.site.register(SilverPackage)
admin.site.register(PlatinumPackage)
admin.site.register(CustomisePackage)
admin.site.register(Booking)
admin.site.register(ChatMessage)

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)