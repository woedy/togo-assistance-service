import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from clients.models import Client
from communications.models import PrivateChatRoom
from tas_project.utils import unique_letter_id_generator, unique_meeting_id_generator, unique_secretary_id_generator, unique_log_id_generator

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
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='client_logs')

    purpose = models.CharField(choices=PURPOSE_CHOICES, null=True, blank=True, max_length=200)
    contact_type = models.CharField(choices=CONTACT_TYPE_CHOICES, null=True, blank=True, max_length=200)

    status = models.CharField(choices=STATUS_CHOICES, null=True, blank=True, max_length=200)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.first_name


def pre_save_log_id_receiver(sender, instance, *args, **kwargs):
    if not instance.log_id:
        instance.log_id = unique_log_id_generator(instance)

pre_save.connect(pre_save_log_id_receiver, sender=LogBook)


MEETING_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Broadcast', 'Broadcast'),
    ('Ongoing', 'Ongoing'),
    ('Complete', 'Complete'),

)




class Meeting(models.Model):
    meeting_id = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=5000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=5000, blank=True, null=True)

    attendees = models.ManyToManyField(User, related_name='attendees', blank=True)
    meeting_attendees = models.ManyToManyField(User, related_name='meeting_attendees', blank=True)

    status = models.CharField(choices=MEETING_STATUS_CHOICES, null=True, blank=True, max_length=200)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def pre_save_meeting_id_receiver(sender, instance, *args, **kwargs):
    if not instance.meeting_id:
        instance.meeting_id = unique_meeting_id_generator(instance)

pre_save.connect(pre_save_meeting_id_receiver, sender=Meeting)



class MeetingReminder(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='meeting_reminders')
    subject = models.CharField(max_length=5000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    remninder_time = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





def upload_letter_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "letters/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



LETTER_STATUS_CHOICES = (
       ('Pending', 'Pending'),
    ('Sent', 'Sent'),
    ('Received', 'Received'),
    ('Not Sent', 'Not Sent')
)







class Letter(models.Model):
    letter_id = models.CharField(max_length=200, null=True, blank=True)

    letter_type = models.CharField(max_length=1000, null=True, blank=True)
    date_sent = models.DateTimeField(null=True, blank=True)
    date_received = models.DateTimeField(null=True, blank=True)

    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='letter_sender')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='letter_receiver')

    
    status = models.CharField(choices=LETTER_STATUS_CHOICES, null=True, blank=True, default='Pending', max_length=200)


    letter_file = models.FileField(upload_to=upload_letter_file_path, null=True, blank=True)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def pre_save_letter_id_receiver(sender, instance, *args, **kwargs):
    if not instance.letter_id:
        instance.letter_id = unique_letter_id_generator(instance)

pre_save.connect(pre_save_letter_id_receiver, sender=Letter)



