import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from bookings.models import Booking
from communications.models import PrivateChatRoom
from tas_project.utils import unique_hr_id_generator, unique_legal_id_generator, unique_contract_id_generator

User = get_user_model()



class Legal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='legals')
    legal_id = models.CharField(max_length=200, null=True, blank=True)

    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="legals_user_room")


    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email

#def post_save_user_room(sender, instance, *args, **kwargs):
#    if not instance.room:
#        instance.room = PrivateChatRoom.objects.create(
#            user=instance.user
#        )
#
#post_save.connect(post_save_user_room, sender=Legal)

def pre_save_legal_id_receiver(sender, instance, *args, **kwargs):
    if not instance.legal_id:
        instance.legal_id = unique_legal_id_generator(instance)

pre_save.connect(pre_save_legal_id_receiver, sender=Legal)



def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "contracts/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

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




class Contract(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='booking_contracts')
    contract_id = models.CharField(max_length=200, null=True, blank=True)

    file = models.FileField(upload_to=upload_file_path, null=True, blank=True)

    sent = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



def pre_save_contract_id_receiver(sender, instance, *args, **kwargs):
    if not instance.contract_id:
        instance.contract_id = unique_contract_id_generator(instance)

pre_save.connect(pre_save_contract_id_receiver, sender=Contract)
