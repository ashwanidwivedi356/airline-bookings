from rest_framework.exceptions import ValidationError
from .models import BookingState

ALLOWED_TRANSITIONS = {
    BookingState.INITIATED: [BookingState.SEAT_HELD],
    BookingState.SEAT_HELD: [
        BookingState.PAYMENT_PENDING,
        BookingState.EXPIRED,
    ],
    BookingState.PAYMENT_PENDING: [
        BookingState.CONFIRMED,
        BookingState.CANCELLED,
    ],
    BookingState.CONFIRMED: [BookingState.CANCELLED],
    BookingState.CANCELLED: [BookingState.REFUNDED],
}

def validate_state_transition(current_state, next_state):
    allowed = ALLOWED_TRANSITIONS.get(current_state, [])

    if next_state not in allowed:
        raise ValidationError(
            f"Invalid state transition from {current_state} to {next_state}"
        )
