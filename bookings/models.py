from django.db import models
from rest_framework.exceptions import ValidationError
# Create your models here.
class BookingState(models.TextChoices):
    INITIATED = "INITIATED", "Initiated"
    SEAT_HELD = "SEAT_HELD", "Seat Held"
    PAYMENT_PENDING = "PAYMENT_PENDING", "Payment Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    EXPIRED = "EXPIRED", "Expired"
    REFUNDED = "REFUNDED", "Refunded"

class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()

    def __str__(self):
        return f"{self.flight_number} ({self.source} → {self.destination})"

class Seat(models.Model):
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="seats"
    )
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("flight", "seat_number")

    def __str__(self):
        return f"{self.flight.flight_number} - {self.seat_number}"

ALLOWED_TRANSITIONS = {
    BookingState.SEAT_HELD: [BookingState.PAYMENT_PENDING, BookingState.EXPIRED],
    BookingState.PAYMENT_PENDING: [BookingState.CONFIRMED, BookingState.CANCELLED],
    BookingState.CONFIRMED: [BookingState.CANCELLED],
    BookingState.CANCELLED: [BookingState.REFUNDED],
}






class Booking(models.Model):
    user_id = models.IntegerField()  # mocked user
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.OneToOneField(
        Seat,
        on_delete=models.CASCADE,
        related_name="booking"
    )
    state = models.CharField(
        max_length=20,
        choices=BookingState.choices,
        default=BookingState.INITIATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} - {self.state}"
    
    def transition_to(self, new_state):
        allowed = ALLOWED_TRANSITIONS.get(self.state, [])
        if new_state not in allowed:
            raise ValidationError(
                f"Invalid state transition from {self.state} to {new_state}"
            )
        self.state = new_state
        self.save()

class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("SUCCESS", "Success"),
            ("FAILED", "Failed"),
            ("REFUNDED", "Refunded"),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
