import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from tas_project.utils import unique_operations_id_generator

User = get_user_model()


class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operations')
    operations_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="operations_user_room")

    profile_complete = models.BooleanField(default=False)

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)


    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def post_save_user_room(sender, instance, *args, **kwargs):
    if not instance.room:
        instance.room = PrivateChatRoom.objects.create(
            user=instance.user
        )

post_save.connect(post_save_user_room, sender=Operation)


def pre_save_operations_id_receiver(sender, instance, *args, **kwargs):
    if not instance.operations_id:
        instance.operations_id = unique_operations_id_generator(instance)

pre_save.connect(pre_save_operations_id_receiver, sender=Operation)


