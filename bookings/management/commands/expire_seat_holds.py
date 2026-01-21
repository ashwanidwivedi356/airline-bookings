from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.db import transaction

from bookings.models import Booking, BookingState
class Command(BaseCommand):
    help = "Expire seat-held bookings after 10 minutes"

    def handle(self, *args, **kwargs):
        expiry_time = now() - timedelta(minutes=10)

        expired_bookings = Booking.objects.filter(
            state=BookingState.SEAT_HELD,
            created_at__lt=expiry_time
        )

        count = expired_bookings.count()

        with transaction.atomic():
            for booking in expired_bookings:
                booking.state = BookingState.EXPIRED
                booking.save()

                # Release seat
                seat = booking.seat
                seat.is_booked = False
                seat.save()

        self.stdout.write(
            self.style.SUCCESS(f"{count} bookings expired successfully")
        )
