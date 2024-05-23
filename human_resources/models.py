import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from tas_project.utils import unique_hr_id_generator

User = get_user_model()



class HumanResource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='human_resources')
    hr_id = models.CharField(max_length=200, null=True, blank=True)

    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="human_recource_user_room")


    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def pre_save_hr_id_receiver(sender, instance, *args, **kwargs):
    if not instance.hr_id:
        instance.hr_id = unique_hr_id_generator(instance)

pre_save.connect(pre_save_hr_id_receiver, sender=HumanResource)


