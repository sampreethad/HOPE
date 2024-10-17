from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(userProfile)


admin.site.register(Blog)
admin.site.register(Appointment)
admin.site.register(Time)
admin.site.register(Chat)

admin.site.register(Doctor)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(videoSolution)
admin.site.register(YogaClass)
admin.site.register(Enrollment)
admin.site.register(Leave)
admin.site.register(faq)