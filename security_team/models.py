import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save

from clients.models import Client
from communications.models import PrivateChatRoom
from tas_project.utils import unique_guard_id_generator, unique_payroll_id_generator

User = get_user_model()


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_guard_id_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "card_id/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_guard_files_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "guard_files/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "guards/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



def get_default_profile_image():
    return "defaults/default_profile_image.png"


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),

)




class SecurityGuard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_guards')
    guard_id = models.CharField(max_length=200, null=True, blank=True)

    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="guards_user_room")

    profile_complete = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(max_digits=30, decimal_places=15, null=True, blank=True)

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email


def pre_save_guard_id_receiver(sender, instance, *args, **kwargs):
    if not instance.guard_id:
        instance.guard_id = unique_guard_id_generator(instance)

pre_save.connect(pre_save_guard_id_receiver, sender=SecurityGuard)




class SecurityGuardID(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name='guard_id_cards')
    card_id = models.CharField(max_length=500, blank=True, null=True)

    valid = models.BooleanField(default=False)


    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardIDImage(models.Model):
    guard_id = models.ForeignKey(SecurityGuardID, on_delete=models.CASCADE, related_name='guard_id_card_images')
    image = models.ImageField(upload_to=upload_guard_id_image_path, null=True, blank=True)

    active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SecurityGuardContact(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name='guard_contacts')

    email = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact_1 = models.CharField(max_length=500, blank=True, null=True)
    emergency_contact_2 = models.CharField(max_length=500, blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardDeviceInfo(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name='guard_devices')

    device_name = models.CharField(max_length=500, blank=True, null=True)
    device_type = models.CharField(max_length=500, blank=True, null=True)
    device_model = models.CharField(max_length=500, blank=True, null=True)

    is_deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SecurityGuardActivity(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name='guard_activities')

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




class SecurityGuardFile(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name="guard_files")
    file = models.FileField(upload_to=upload_guard_files_path, null=True, blank=True)
    file_name = models.CharField(max_length=1000, null=True, blank=True)
    file_ext = models.CharField(max_length=255, null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardNote(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name="guard_notes")
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class SecurityGuardSkill(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name="guard_skills")
    skill = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardAccess(models.Model):
    guard = models.OneToOneField(SecurityGuard, on_delete=models.CASCADE, related_name="guard_access")

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





class SecurityGuardSetting(models.Model):
    guard = models.OneToOneField(SecurityGuard, on_delete=models.CASCADE, related_name="guard_settings")

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardSettingGeneral(models.Model):
    guard_settings = models.OneToOneField(SecurityGuardSetting, on_delete=models.CASCADE, related_name="guard_general_settings")

    auto_approve = models.BooleanField(default=False)
    enable_gps_tracking = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardSettingTimeClock(models.Model):
    guard_settings = models.OneToOneField(SecurityGuardSetting, on_delete=models.CASCADE, related_name="guard_time_clock_settings")

    auto_update_recurring = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardSettingScheduler(models.Model):
    guard_settings = models.OneToOneField(SecurityGuardSetting, on_delete=models.CASCADE, related_name="guard_schedule_settings")

    auto_schedule = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardSettingNotification(models.Model):
    guard_settings = models.OneToOneField(SecurityGuardSetting, on_delete=models.CASCADE, related_name="guard_notification_settings")

    auto_schedule = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SecurityGuardTask(models.Model):
    guard = models.OneToOneField(SecurityGuard, on_delete=models.CASCADE, related_name="guard_tasks")
    item = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)











######################## GUARD AVAILABILITY


SLOT_STATE_CHOICES = (
    ("Vacant", "Vacant"),
    ("Partial", "Partial"),
    ("Occupied", "Occupied")
)

class GuardAvailability(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE, related_name="guard_availabilities")

    slot_date = models.DateField(null=True, blank=True)
    state = models.CharField(default="Vacant", choices=SLOT_STATE_CHOICES, max_length=255)

    is_recurring = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class TimeSlot(models.Model):
    guard_slot = models.ForeignKey(GuardAvailability, on_delete=models.CASCADE, related_name="availability_time_slots")
    booking_id = models.IntegerField(null=True, blank=True)

    time = models.TimeField(null=True, blank=True)

    occupied = models.BooleanField(default=False)
    occupant = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="booking_occupant")

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)








############################# PAYROLL #######################

class PayPeriod(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

class PayrollEntry(models.Model):
    payroll_id = models.CharField(max_length=200, null=True, blank=True)

    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE)
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0, null=True, blank=True)
    overtime_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    gross_pay = models.DecimalField(default=0.0, max_digits=10, decimal_places=2,null=True, blank=True )
    net_pay = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True, blank=True)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_gross_pay(self):
        return self.basic_salary + (self.overtime_hours * self.overtime_rate)
    def calculate_net_pay(self):
        return self.gross_pay - self.deductions
    def save(self, *args, **kwargs):
        self.gross_pay = self.calculate_gross_pay()
        self.net_pay = self.calculate_net_pay()
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.guard.user.first_name} - {self.pay_period}'


def pre_save_payroll_id_receiver(sender, instance, *args, **kwargs):
    if not instance.payroll_id:
        instance.payroll_id = unique_payroll_id_generator(instance)

pre_save.connect(pre_save_payroll_id_receiver, sender=PayrollEntry)
