import os
import random

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from tas_project.utils import unique_user_id_generator



def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "operation/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_user_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "users/file/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def get_default_profile_image():
    return "defaults/default_profile_image.png"


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("user must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )
        return user



    def create_superuser(self, email, first_name=None, last_name=None, password=None, ):
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_admin=True
        )
        return user


    def search(self, query=None):
        qs = self.get_queryset()

        if query is not None:
            or_lookup = (Q(email__icontains=query) | Q(full_name__icontains=query))
            qs = qs.filter(or_lookup).distinct()

        return qs


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


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)




EMPLOYMENT_STATUS = (
    ('Employed', 'Employed'),
    ('Resigned', 'Resigned'),
    ('Dismissed', 'Dismissed'),
    ('Retired', 'Retired'),
    ('Death', 'Death'),

)



class User(AbstractBaseUser):
    user_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True,  null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    department = models.CharField(max_length=100, choices=DEPARTMENT, blank=True, null=True)
    employment_status = models.CharField(max_length=100, choices=EMPLOYMENT_STATUS, blank=True, null=True)
    fcm_token = models.TextField(blank=True, null=True)

    otp_code = models.CharField(max_length=10, blank=True, null=True)
    email_token = models.CharField(max_length=10, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_image_path, null=True, blank=True, default=get_default_profile_image)
    dob = models.DateTimeField(null=True, blank=True)
    marital_status = models.BooleanField(default=False, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(default="English", max_length=255, null=True, blank=True)
    about_me = models.TextField(blank=True, null=True)


    profile_complete = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)


    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        if self.email is None:
            return 'No Email'
        return self.email


    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff


    @property
    def is_admin(self):
        return self.admin




@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def pre_save_user_id_receiver(sender, instance, *args, **kwargs):
    if not instance.user_id:
        instance.user_id = unique_user_id_generator(instance)

pre_save.connect(pre_save_user_id_receiver, sender=User)


def post_save_user_info(sender, instance, *args, **kwargs):
    if not instance.photo:
        instance.photo = get_default_profile_image()

post_save.connect(post_save_user_info, sender=User)





class UserContact(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




class UserEmergencyContact(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_emergency_contacts')
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)





class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_files')
    user_file_id = models.CharField(max_length=200, null=True, blank=True)

    file = models.FileField(upload_to=upload_user_file_path, null=True, blank=True)

    file_name = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

