import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from post_sites.models import ClientPostSite
from tas_project.utils import unique_operations_id_generator, unique_panic_report_id_generator, unique_site_alert_id_generator

User = get_user_model()



ROLE_CHOICES = (
    ('Supervisor', 'Supervisor'),
    ('Post Managers', 'Post Managers'),
    ('Inspectors', 'Inspectors'),
    ('Trainers', 'Trainers'),
    ('Controllers', 'Controllers'),
    ('Operations Department Managers', 'Operations Department Managers'),
    ('Administrative Assistant', 'Administrative Assistant'),
    ('Director of operations', 'Director of operations'),
    ('Deputy Director of operations', 'Deputy Director of operations'),
)



class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')
    operations_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="operations_user_room")

    profile_complete = models.BooleanField(default=False)

    role = models.CharField(choices=ROLE_CHOICES, null=True, blank=True, max_length=200)

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)


    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email



def pre_save_operations_id_receiver(sender, instance, *args, **kwargs):
    if not instance.operations_id:
        instance.operations_id = unique_operations_id_generator(instance)

pre_save.connect(pre_save_operations_id_receiver, sender=Operation)


PANIC_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Resolved', 'Resolved'),
    ('Unresolved', 'Unresolved'),
)



class PanicReport(models.Model):
    panic_report_id = models.CharField(max_length=200, null=True, blank=True)

    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="panic_alert")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='panic_sender')

    is_archived = models.BooleanField(default=False)

    status = models.CharField(default='Pending',choices=PANIC_STATUS_CHOICES, null=True, blank=True, max_length=200)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_panic_report_id_receiver(sender, instance, *args, **kwargs):
    if not instance.panic_report_id:
        instance.panic_report_id = unique_panic_report_id_generator(instance)

pre_save.connect(pre_save_panic_report_id_receiver, sender=PanicReport)


ALERT_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Responded', 'Responded'),
    ('Late Response', 'Late Response'),
)



class SiteAlert(models.Model):
    site_alert_id = models.CharField(max_length=200, null=True, blank=True)

    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="site_alert")
    send_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='site_send_to')
    reponse_time = models.DateTimeField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)

    status = models.CharField(default='Pending',choices=ALERT_STATUS_CHOICES, null=True, blank=True, max_length=200)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_site_alert_id_receiver(sender, instance, *args, **kwargs):
    if not instance.site_alert_id:
        instance.site_alert_id = unique_site_alert_id_generator(instance)

pre_save.connect(pre_save_site_alert_id_receiver, sender=SiteAlert)



