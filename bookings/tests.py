

from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient
from django.utils.timezone import now
from datetime import timedelta
from bookings.services import expire_seat_holds

from bookings.models import Flight

from .models import Flight, Seat, Booking, BookingState
class BookingExpiryTest(TestCase):

    def setUp(self):
        self.flight = Flight.objects.create(
            source="Delhi",
            destination="Bhopal"
        )

        self.seat = Seat.objects.create(
            flight=self.flight,
            seat_number="A1",
            is_booked=False
        )

        self.booking = Booking.objects.create(
            flight=self.flight,
            seat=self.seat,
            state=BookingState.SEAT_HELD,
            expires_at=timezone.now() - timedelta(minutes=5)
        )

    def test_seat_hold_expiry(self):
        expire_seat_holds()

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.state,
            BookingState.EXPIRED
        )

class RefundTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.flight = Flight.objects.create(
            flight_number="AI-202",
            source="DEL",
            destination="BOM",
            departure_time=now()
        )
        self.seat = Seat.objects.create(
            flight=self.flight,
            seat_number="B1"
        )
        self.booking = Booking.objects.create(
            user_id=2,
            flight=self.flight,
            seat=self.seat,
            state=BookingState.CANCELLED
        )
    def test_refund_once(self):
        url = f"/api/bookings/{self.booking.id}/refund/"
        response1 = self.client.post(url)
        response2 = self.client.post(url)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 400)


class BookingExpiryTest(TestCase):

    def test_seat_hold_expiry(self):
        self.booking.expires_at = timezone.now() - timedelta(minutes=1)
        self.booking.save()

        expire_seat_holds()

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.state, BookingState.EXPIRED)

########
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from bookings.models import Booking, BookingState, Seat, Flight
from bookings.services import expire_seat_holds


class BookingExpiryTest(TestCase):

    def setUp(self):
        self.flight = Flight.objects.create(
            source="Delhi",
            destination="Bhopal"
        )

        self.seat = Seat.objects.create(
            flight=self.flight,
            seat_number="A1",
            is_booked=False
        )

        self.booking = Booking.objects.create(
            flight=self.flight,
            seat=self.seat,
            state=BookingState.SEAT_HELD,
            expires_at=timezone.now() - timedelta(minutes=5)
        )

    def test_seat_hold_expiry(self):
        expire_seat_holds()

        self.booking.refresh_from_db()

        self.assertEqual(
            self.booking.state,
            BookingState.EXPIRED
        )
