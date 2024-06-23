from django.contrib import admin

from bookings.models import Booking, BookDate, Estimate, BookedGuard, Deployment, DeploymentAttendance

admin.site.register(Booking)
admin.site.register(BookDate)
admin.site.register(BookedGuard)
admin.site.register(Estimate)
admin.site.register(Deployment)
admin.site.register(DeploymentAttendance)
