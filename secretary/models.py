import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from clients.models import Client
from communications.models import PrivateChatRoom
from tas_project.utils import unique_secretary_id_generator, uniqu_log_id_generator

User = get_user_model()


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "secretary/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_default_profile_image():
    return "defaults/default_profile_image.png"


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)

class Secretary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='secretaries')
    secretary_id = models.CharField(max_length=200, null=True, blank=True)

    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="secretary_user_room")

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def pre_save_secretary_id_receiver(sender, instance, *args, **kwargs):
    if not instance.secretary_id:
        instance.secretary_id = unique_secretary_id_generator(instance)

pre_save.connect(pre_save_secretary_id_receiver, sender=Secretary)




PURPOSE_CHOICES = (
    ('Guard Request', 'Guard Request'),
    ('Visit', 'Visit'),
    ('Complain', 'Complain'),
    ('Payment', 'Payment'),
)

STATUS_CHOICES = (
    ('Company', 'Company'),
    ('Individual', 'Individual')
)

CONTACT_TYPE_CHOICES = (
    ('Visit', 'Visit'),
    ('Call', 'Call')
)


class LogBook(models.Model):
    log_id = models.CharField(max_length=200, null=True, blank=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_logs')



    purpose = models.CharField(choices=PURPOSE_CHOICES, null=True, blank=True, max_length=200)
    contact_type = models.CharField(choices=CONTACT_TYPE_CHOICES, null=True, blank=True, max_length=200)

    status = models.CharField(choices=STATUS_CHOICES, null=True, blank=True, max_length=200)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def pre_save_log_id_receiver(sender, instance, *args, **kwargs):
    if not instance.log_id:
        instance.log_id = uniqu_log_id_generator(instance)

pre_save.connect(pre_save_log_id_receiver, sender=LogBook)

