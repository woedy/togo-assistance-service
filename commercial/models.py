import os
import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from bookings.models import Booking
from communications.models import PrivateChatRoom
from tas_project.utils import unique_commercial_id_generator, unique_contract_id_generator

User = get_user_model()

class Commercial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commercial')
    commercial_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="commercial_user_room")

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)


    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email



def pre_save_commercial_id_receiver(sender, instance, *args, **kwargs):
    if not instance.commercial_id:
        instance.commercial_id = unique_commercial_id_generator(instance)

pre_save.connect(pre_save_commercial_id_receiver, sender=Commercial)
