from django.db import models
from django.db.models.signals import pre_save

from clients.models import Client
from communications.models import PrivateChatRoom
from operations.models import Operation
from post_sites.models import ClientPostSite
from security_team.models import SecurityGuard
from tas_project.utils import unique_booking_id_generator, unique_estimate_id_generator, unique_deployment_id_generator, \
    unique_attendance_id_generator

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


DURATION = (
    ('Temporal', 'Temporal'),
    ('Permanent', 'Permanent')

)


GUARD_TYPE = (
    ('Armed Guard', 'Armed Guard'),
    ('Unarmed Guard', 'Unarmed Guard'),

)


class Booking(models.Model):
    booking_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, related_name='booking_chat_rooms')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='booking_client')

    re_scheduled = models.BooleanField(default=False)
    booking_rescheduled_at = models.DateTimeField(null=True, blank=True)

    estimate = models.CharField(null=True, blank=True, max_length=100)
    actual_price = models.CharField(null=True, blank=True, max_length=100)
    amount_paid = models.CharField(null=True, blank=True, max_length=100)
    paid = models.BooleanField(default=False)

    confirm_payment = models.BooleanField(default=False)
    special_instruction = models.TextField(null=True, blank=True)

    review = models.TextField(null=True, blank=True)
    equipment_requirements = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)
    contact_duration = models.CharField(max_length=255, default="Temporal", null=True, blank=True, choices=DURATION)

    guard_type = models.CharField(max_length=255, default="Armed Guard", null=True, blank=True, choices=GUARD_TYPE)

    booking_start = models.DateTimeField(null=True, blank=True)
    booking_end = models.DateTimeField(null=True, blank=True)

    booking_approved_at = models.DateTimeField(null=True, blank=True)
    booking_declined_at = models.DateTimeField(null=True, blank=True)
    booking_cancelled_at = models.DateTimeField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_booking_id_receiver(sender, instance, *args, **kwargs):
    if not instance.booking_id:
        instance.booking_id = unique_booking_id_generator(instance)

pre_save.connect(pre_save_booking_id_receiver, sender=Booking)


DEPARTMENT = (
    ('SECRETARY', 'SECRETARY'),
    ('HUMAN RESOURCES', 'HUMAN RESOURCES'),
    ('ADMIN', 'ADMIN'),
('LOGISTICS', 'LOGISTICS'),
('BILLING', 'BILLING'),
('OPERATIONS', 'OPERATIONS'),
('COMMERCIAL', 'COMMERCIAL'),
('CLIENT', 'CLIENT'),
('GUARD', 'GUARD'),
('LEGAL', 'LEGAL'),

)



class ForwardingList(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='forwarding_list')

    department = models.CharField(max_length=100, choices=DEPARTMENT, blank=True, null=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookDate(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='book_dates')

    booking_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    from_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    to_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookedGuard(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booked_guard_booking')
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name='booked_guards')


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

    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=EST_STATUS_CHOICE)
    amount = models.CharField(max_length=200,  null=True, blank=True)
    expires_on = models.DateTimeField(null=True, blank=True)

    #estimator = models.ForeignKey(Commercial, on_delete=models.SET_NULL, related_name="estimate_commercial")

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_estimate_id_receiver(sender, instance, *args, **kwargs):
    if not instance.estimate_id:
        instance.estimate_id = unique_estimate_id_generator(instance)

pre_save.connect(pre_save_estimate_id_receiver, sender=Estimate)




class Service(models.Model):
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)





class Deployment(models.Model):
    deployment_id = models.CharField(max_length=200, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_deployment")
    supervisor = models.ForeignKey(Operation, on_delete=models.SET_NULL, null=True, blank=True, related_name="deployment_supervisor")
    #sub_supervisor = models.ForeignKey(Operation, on_delete=models.SET_NULL, null=True, blank=True, related_name="deployment_sub_supervisor")
    guards = models.ManyToManyField(SecurityGuard, null=True, blank=True, related_name="deployed_guards")
    site = models.ForeignKey(ClientPostSite, on_delete=models.SET_NULL, null=True, blank=True, related_name="deployed_site")
    deployed = models.BooleanField(default=False)
    deployed_at = models.DateTimeField(null=True, blank=True)



    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




def pre_save_deployment_id_receiver(sender, instance, *args, **kwargs):
    if not instance.deployment_id:
        instance.deployment_id = unique_deployment_id_generator(instance)

pre_save.connect(pre_save_deployment_id_receiver, sender=Deployment)






class DeploymentAttendance(models.Model):
    attendance_id = models.CharField(max_length=200, null=True, blank=True)

    deployment = models.ForeignKey(Deployment, on_delete=models.CASCADE, related_name="deployments")
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    guard = models.ForeignKey(SecurityGuard, on_delete=models.SET_NULL, null=True, blank=True, related_name="guard_attendances")
    clock_in_note = models.TextField(null=True, blank=True)
    clock_out_note = models.TextField(null=True, blank=True)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def pre_save_attendance_id_receiver(sender, instance, *args, **kwargs):
    if not instance.attendance_id:
        instance.attendance_id = unique_attendance_id_generator(instance)

pre_save.connect(pre_save_attendance_id_receiver, sender=DeploymentAttendance)





class FieldReport(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='field_reports')

    title = models.CharField(max_length=1000, null=True, blank=True)
    report = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class BookingEmail(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_emails')

    title = models.CharField(max_length=1000, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
