from django.contrib.auth import get_user_model
from rest_framework import serializers

from security_team.models import SecurityGuard

User = get_user_model()


class SecurityGuardUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class SecurityGuardDetailsSerializer(serializers.ModelSerializer):
    user = SecurityGuardUserDetailSerializer(many=False)
    class Meta:
        model = SecurityGuard
        fields = "__all__"




