from django.contrib import admin

from bookings.models import Booking, BookDate, Estimate, BookedGuard, Deployment, DeploymentAttendance, ForwardingList, \
    FieldReport, BookingEmail

admin.site.register(Booking)
admin.site.register(ForwardingList)
admin.site.register(BookDate)
admin.site.register(BookedGuard)
admin.site.register(Estimate)
admin.site.register(Deployment)
admin.site.register(DeploymentAttendance)
admin.site.register(FieldReport)
admin.site.register(BookingEmail)
