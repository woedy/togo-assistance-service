from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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

class Notification(models.Model):
    english_title = models.CharField(max_length=1000, null=True, blank=True)
    french_title = models.CharField(max_length=1000, null=True, blank=True)

    english_subject = models.TextField(null=True, blank=True)
    french_subject = models.TextField(null=True, blank=True)

    read = models.BooleanField(default=False)

    department = models.CharField(max_length=100, choices=DEPARTMENT, blank=True, null=True)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



