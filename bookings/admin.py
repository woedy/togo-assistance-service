from django.contrib import admin

from bookings.models import Booking, BookDate

admin.site.register(Booking)
admin.site.register(BookDate)
