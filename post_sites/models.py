from django.db import models

from clients.models import Client
from security_team.models import SecurityGuard


# Create your models here.
class ClientPostSite(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_post_sites')
    site_name = models.CharField(max_length=5000, blank=True, null=True)

    is_client = models.BooleanField(default=False)

    assigned_guards = models.IntegerField(default=0)
    guards_on_site = models.IntegerField(default=0)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostSiteActivity(models.Model):
    guard = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name='post_site_activities')

    subject = models.CharField(max_length=500, blank=True, null=True)
    action = models.TextField(blank=True, null=True)

    task_completed = models.BooleanField(default=False)
    hours_worked = models.BooleanField(default=False)
    submitted_reports = models.BooleanField(default=False)
    no_show = models.BooleanField(default=False)
    late = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
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




class PostSiteFile(models.Model):
    post_site = models.ForeignKey(ClientPostSite, on_delete=models.CASCADE, related_name="post_site_file")
    file = models.FileField(upload_to=upload_guard_files_path, null=True, blank=True)
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