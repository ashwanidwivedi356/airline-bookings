from rest_framework import serializers
from .models import Booking, Seat, Flight, BookingState


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "user_id", "flight", "seat", "state"]
        read_only_fields = ["id", "state"]


def validate(self, data):
    if data["seat"].flight_id != data["flight"].id:
        raise serializers.ValidationError(
            "Seat does not belong to this flight"
        )
    return data
