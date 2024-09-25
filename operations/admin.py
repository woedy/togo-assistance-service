from django.contrib import admin

from operations.models import Operation, PanicReport, SiteAlert

admin.site.register(Operation)

admin.site.register(PanicReport)

admin.site.register(SiteAlert)