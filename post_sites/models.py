import os
import random

from django.db import models
from django.db.models.signals import pre_save

from clients.models import Client
from security_team.models import SecurityGuard
from tas_project.utils import unique_site_id_generator, unique_zone_id_generator


class ClientZone(models.Model):
    zone_id = models.CharField(max_length=200, null=True, blank=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_zones')
    zone_name = models.CharField(max_length=5000, blank=True, null=True)

    description = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_zone_id_receiver(sender, instance, *args, **kwargs):
    if not instance.zone_id:
        instance.zone_id = unique_zone_id_generator(instance)

pre_save.connect(pre_save_zone_id_receiver, sender=ClientZone)




class ClientZoneCoordinate(models.Model):
    client_zone = models.ForeignKey(ClientZone, on_delete=models.CASCADE, related_name='zone_coordinates')

    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


GENDER_CHOICES = (
    ('Male Only', 'Male Only'),
    ('Female Only', 'Female Only'),
    ('Both', 'Both'),

)



SITE_TYPE = (
    ('Industrial', 'Industrial'),
    ('Commercial', 'Commercial'),
    ('Residential', 'Residential'),
    ('Personal', 'Personal'),

)

class ClientPostSite(models.Model):
    site_id = models.CharField(max_length=200, null=True, blank=True)

    client_zone = models.ForeignKey(ClientZone, on_delete=models.CASCADE, related_name='zone_post_sites')
    site_name = models.CharField(max_length=5000, blank=True, null=True)


    no_of_guards = models.IntegerField(default=0)
    guards_on_site = models.IntegerField(default=0)
    guards_gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, null=True)
    site_type = models.CharField(max_length=100, choices=SITE_TYPE, blank=True, null=True)
    description = models.TextField(null=True, blank=True)


    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_site_id_receiver(sender, instance, *args, **kwargs):
    if not instance.site_id:
        instance.site_id = unique_site_id_generator(instance)

pre_save.connect(pre_save_site_id_receiver, sender=ClientPostSite)




class PostSiteActivity(models.Model):
    guard = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name='post_site_activities')

    subject = models.CharField(max_length=500, blank=True, null=True)
    action = models.TextField(blank=True, null=True)

    task_completed = models.BooleanField(default=False)
    hours_worked = models.BooleanField(default=False)
    submitted_reports = models.BooleanField(default=False)
    no_show = models.BooleanField(default=False)
    late = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class PostOrder(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="client_post_orders")
    subject = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class PostSiteNote(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="post_site_notes")
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_post_site_files_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "client_files/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

class PostSiteFile(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="post_site_file")
    file = models.FileField(upload_to=upload_post_site_files_path, null=True, blank=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostSiteAssignedGuard(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="post_site_assigned_guards")
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name="assigned_guards")
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostSiteTask(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="post_site_tasks")
    item = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)