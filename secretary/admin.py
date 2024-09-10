from django.contrib import admin

from secretary.models import Meeting, MeetingReminder, Secretary, LogBook

admin.site.register(Secretary)
admin.site.register(LogBook)

admin.site.register(Meeting)
admin.site.register(MeetingReminder)
