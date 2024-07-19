from django.contrib import admin

from human_resources.models import HumanResource, StaffPayrollEntry, StaffPayPeriod

admin.site.register(HumanResource)
admin.site.register(StaffPayPeriod)
admin.site.register(StaffPayrollEntry)
