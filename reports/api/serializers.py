from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models import Client, ClientComplaint
from reports.models import Report

User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = "__all__"
