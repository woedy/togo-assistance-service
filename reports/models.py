from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reports")
    title = models.CharField(max_length=1000, null=True, blank=True)
    report = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



