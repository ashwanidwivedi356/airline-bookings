from django.utils import timezone
from .models import Booking, BookingState

# def expire_seat_holds():
#     now = timezone.now()

#     expired_bookings = Booking.objects.filter(
#         state=BookingState.SEAT_HELD,
#         expires_at__lt=now
#     )

#     for booking in expired_bookings:
#         booking.state = BookingState.EXPIRED
#         booking.seat.is_booked = False
#         booking.seat.save()
#         booking.save()

#     return expired_bookings.count()

from django.utils import timezone
from bookings.models import Booking, BookingState

def expire_seat_holds():
    now = timezone.now()
    Booking.objects.filter(
        state=BookingState.SEAT_HELD,
        expires_at__lt=now
    ).update(state=BookingState.EXPIRED)
