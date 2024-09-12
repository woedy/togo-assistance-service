from django.contrib import admin

from secretary.models import Letter, Meeting, MeetingReminder, Secretary, LogBook

admin.site.register(Secretary)
admin.site.register(LogBook)

admin.site.register(Meeting)
admin.site.register(MeetingReminder)


admin.site.register(Letter)
