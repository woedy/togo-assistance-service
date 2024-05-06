import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from tas_project.utils import unique_hr_id_generator

User = get_user_model()


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "hr/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_default_profile_image():
    return "defaults/default_profile_image.png"


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)

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

def post_save_user_room(sender, instance, *args, **kwargs):
    if not instance.room:
        instance.room = PrivateChatRoom.objects.create(
            user=instance.user
        )

post_save.connect(post_save_user_room, sender=HumanResource)

def pre_save_hr_id_receiver(sender, instance, *args, **kwargs):
    if not instance.hr_id:
        instance.hr_id = unique_hr_id_generator(instance)

pre_save.connect(pre_save_hr_id_receiver, sender=HumanResource)


