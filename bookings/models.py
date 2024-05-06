from django.db import models

from clients.models import Client

STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Rescheduled', 'Rescheduled'),
    ('Approved', 'Approved'),
    ('Declined', 'Declined'),
    ('Started', 'Started'),
    ('Ongoing', 'Ongoing'),
    ('Review', 'Review'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)


class Booking(models.Model):
    booking_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, related_name='booking_chat_rooms')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='booking_client')

    booking_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    booking_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    re_scheduled = models.BooleanField(default=False)
    booking_rescheduled_at = models.DateTimeField(null=True, blank=True)

    amount_to_pay = models.CharField(null=True, blank=True, max_length=100)
    actual_price = models.CharField(null=True, blank=True, max_length=100)
    paid = models.BooleanField(default=False)

    confirm_payment = models.BooleanField(default=False)

    actual_duration = models.CharField(null=True, blank=True, max_length=100)

    notes = models.TextField(null=True, blank=True)

    review = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)

    booking_start = models.DateTimeField(null=True, blank=True)
    booking_end = models.DateTimeField(null=True, blank=True)

    booking_approved_at = models.DateTimeField(null=True, blank=True)
    booking_declined_at = models.DateTimeField(null=True, blank=True)
    booking_cancelled_at = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookedGuard(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_guards')
    payment_method = models.CharField(max_length=200,  null=True, blank=True)
    amount = models.CharField(max_length=200,  null=True, blank=True)



    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

EST_STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),
    ('Sent', 'Sent'),
    ('Unsent', 'Unsent'),
    ('Canceled', 'Canceled'),
)

class Estimate(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="post_site_tasks")
    estimate_id = models.CharField(max_length=200, null=True, blank=True)
    item = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    tax = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_estimates")

    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=EST_STATUS_CHOICE)
    amount = models.CharField(max_length=200,  null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)