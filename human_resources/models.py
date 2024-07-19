import os
import random

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save

from communications.models import PrivateChatRoom
from tas_project.utils import unique_hr_id_generator, unique_staff_complaint_id_generator, \
    unique_staff_payroll_id_generator

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



class StaffComplaint(models.Model):
    staff_complaint_id = models.CharField(max_length=200, null=True, blank=True)

    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_complaints")
    representative = models.CharField(max_length=1000, null=True, blank=True)

    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField(null=True, blank=True)

    forward_to = models.CharField(max_length=100, choices=DEPARTMENT, blank=True, null=True)

    status = models.CharField(max_length=255, default="Pending", null=True, blank=True, choices=STATUS_CHOICE)

    is_archived = models.BooleanField(default=False)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




def pre_save_staff_complaint_id_receiver(sender, instance, *args, **kwargs):
    if not instance.staff_complaint_id:
        instance.staff_complaint_id = unique_staff_complaint_id_generator(instance)

pre_save.connect(pre_save_staff_complaint_id_receiver, sender=StaffComplaint)









############################# STAFF PAYROLL #######################

class StaffPayPeriod(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

class StaffPayrollEntry(models.Model):
    staff_payroll_id = models.CharField(max_length=200, null=True, blank=True)

    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    staff_pay_period = models.ForeignKey(StaffPayPeriod, on_delete=models.CASCADE)
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
        return f'{self.staff.first_name} - {self.staff_pay_period}'


def pre_save_staff_payroll_id_receiver(sender, instance, *args, **kwargs):
    if not instance.staff_payroll_id:
        instance.staff_payroll_id = unique_staff_payroll_id_generator(instance)

pre_save.connect(pre_save_staff_payroll_id_receiver, sender=StaffPayrollEntry)

