import os
import random

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from tas_project.utils import unique_client_id_generator, unique_complaint_id_generator

User = get_user_model()

def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "clients/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_client_files_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "client_files/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



def get_default_profile_image():
    return "defaults/default_profile_image.png"


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)



PURPOSE_CHOICES = (
    ('Guard Request', 'Guard Request'),
    ('Visit', 'Visit'),
    ('Complain', 'Complain'),
    ('Payment', 'Payment'),
)


CLIENT_TYPE_CHOICES = (
    ('Physical', 'Physical'),
    ('Moral', 'Moral')
)

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    client_id = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=500, null=True, blank=True)
    purpose = models.CharField(choices=PURPOSE_CHOICES, null=True, blank=True, max_length=200)
    client_type = models.CharField(choices=CLIENT_TYPE_CHOICES, null=True, blank=True, max_length=200)
    person_in_charge = models.CharField(null=True, blank=True, max_length=500)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email



def pre_save_client_id_receiver(sender, instance, *args, **kwargs):
    if not instance.client_id:
        instance.client_id = unique_client_id_generator(instance)

pre_save.connect(pre_save_client_id_receiver, sender=Client)




class ClientContact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_contacts')

    email = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact_1 = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact_2 = models.CharField(max_length=500, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ClientGuardFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_files")
    file = models.FileField(upload_to=upload_client_files_path, null=True, blank=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ClientNote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_notes")
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


DEPARTMENT = (
    ('SECRETARY', 'SECRETARY'),
    ('HUMAN RESOURCES', 'HUMAN RESOURCES'),
    ('ADMIN', 'ADMIN'),
('LOGISTICS', 'LOGISTICS'),
('BILLING', 'BILLING'),
('OPERATIONS', 'OPERATIONS'),
('COMMERCIAL', 'COMMERCIAL'),
('CLIENT', 'CLIENT'),
('GUARD', 'GUARD'),
('LEGAL', 'LEGAL'),

)


STATUS_CHOICE = (

    ('Created', 'Created'),
    ('Pending', 'Pending'),

    ('Approved', 'Approved'),
    ('Declined', 'Declined'),

    ('Unresolved', 'Unresolved'),
    ('Resolved', 'Resolved'),

    ('Review', 'Review'),

    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
)



class ClientComplaint(models.Model):
    complaint_id = models.CharField(max_length=200, null=True, blank=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_complaints")
    representative = models.CharField(max_length=1000, null=True, blank=True)

    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    forward_to = models.CharField(max_length=100, choices=DEPARTMENT, blank=True, null=True)

    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




def pre_save_complaint_id_receiver(sender, instance, *args, **kwargs):
    if not instance.complaint_id:
        instance.complaint_id = unique_complaint_id_generator(instance)

pre_save.connect(pre_save_complaint_id_receiver, sender=ClientComplaint)





