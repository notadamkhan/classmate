from django.contrib import admin
from .models import Profile, Class, StudySession, Message
# Register your models here.

class StudySessionAdmin(admin.ModelAdmin):
    def session_ID(self):
        return self
    list_display = ('title', session_ID, 'startTime', 'endTime')

admin.site.register(Profile)
admin.site.register(Class)
admin.site.register(StudySession, StudySessionAdmin)
admin.site.register(Message)