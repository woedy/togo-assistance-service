from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking
from clients.models import Client, ClientComplaint

User = get_user_model()


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"




class AllBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

