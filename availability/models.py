from django.db import models

User = settings.AUTH_USER_MODEL


SLOT_STATE_CHOICES = (
    ("Vacant", "Vacant"),
    ("Partial", "Partial"),
    ("Occupied", "Occupied")
)

class GuardAvailability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guard_availability")

    date = models.DateField(null=True, blank=True)
    state = models.CharField(default="Vacant", choices=SLOT_STATE_CHOICES, max_length=255)

    is_recurring = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TimeSlot(models.Model):
    staff_availability = models.ForeignKey(GuardAvailability, on_delete=models.CASCADE, related_name="slot_times")
    #appointment = models.ForeignKey(GenericAppointment, null=True, blank=True, on_delete=models.SET_NULL, related_name="slot_appointment")
    booking_id = models.IntegerField(null=True, blank=True)

    time = models.TimeField(null=True, blank=True)


    occupied = models.BooleanField(default=False)
    occupant = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="booking_occupant")

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
