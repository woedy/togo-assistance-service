import os
import random
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "reports/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reports")
    title = models.CharField(max_length=1000, null=True, blank=True)
    report = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=upload_image_path, null=True, blank=True,)

    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



