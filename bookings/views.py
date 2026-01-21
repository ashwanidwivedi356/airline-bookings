import random
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .models import Booking, Seat, Flight, Payment

from .models import Booking, Seat, BookingState
from .serializers import BookingCreateSerializer
from .state_machine import validate_state_transition
from rest_framework.exceptions import ValidationError

class BookingCreateAPIView(APIView):
    """
    POST /api/bookings/
    Creates a booking and locks seat safely
    """

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        seat_id = serializer.validated_data["seat"].id

        try:
            with transaction.atomic():
                # 🔒 Lock seat row
                seat = Seat.objects.select_for_update().get(id=seat_id)

                # ❌ Seat already booked
                if seat.is_booked:
                    return Response(
                        {"error": "Seat already booked"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # ✅ Create booking
                booking = serializer.save(
                    state=BookingState.SEAT_HELD
                )

                # ✅ Mark seat as booked (locked)
                seat.is_booked = True
                seat.save()

                return Response(
                    {
                        "booking_id": booking.id,
                        "state": booking.state
                    },
                    status=status.HTTP_201_CREATED
                )

        except Seat.DoesNotExist:
            return Response(
                {"error": "Seat not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class BookingPaymentAPIView(APIView):
    """
    POST /api/bookings/{id}/pay/
    """

    def post(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                # Move to PAYMENT_PENDING
                validate_state_transition(
                    booking.state,
                    BookingState.PAYMENT_PENDING
                )
                booking.state = BookingState.PAYMENT_PENDING
                booking.save()

                # 🔁 Mock payment
                payment_success = random.choice([True, False])

                if payment_success:
                    validate_state_transition(
                        booking.state,
                        BookingState.CONFIRMED
                    )
                    booking.state = BookingState.CONFIRMED
                    booking.save()

                    Payment.objects.create(
                        booking=booking,
                        amount=5000,
                        status="SUCCESS"
                    )

                    return Response(
                        {
                            "message": "Payment successful",
                            "state": booking.state
                        }
                    )

                else:
                    validate_state_transition(
                        booking.state,
                        BookingState.CANCELLED
                    )
                    booking.state = BookingState.CANCELLED
                    booking.save()

                    Payment.objects.create(
                        booking=booking,
                        amount=5000,
                        status="FAILED"
                    )

                    return Response(
                        {
                            "message": "Payment failed",
                            "state": booking.state
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class BookingCancelAPIView(APIView):
    """
    POST /api/bookings/{id}/cancel/
    """

    def post(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                validate_state_transition(
                    booking.state,
                    BookingState.CANCELLED
                )

                booking.state = BookingState.CANCELLED
                booking.save()

                # 🔓 Release seat
                seat = booking.seat
                seat.is_booked = False
                seat.save()

                return Response(
                    {
                        "message": "Booking cancelled",
                        "state": booking.state
                    }
                )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class BookingRefundAPIView(APIView):
    """
    POST /api/bookings/{id}/refund/
    """

    def post(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate state
        if booking.state != BookingState.CANCELLED:
            return Response(
                {
                    "error": "Refund allowed only for cancelled bookings"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent double refund
        if hasattr(booking, "payment") and booking.payment.status == "REFUNDED":
            return Response(
                {"error": "Refund already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Update state
            booking.state = BookingState.REFUNDED
            booking.save()

            # Update or create payment
            if hasattr(booking, "payment"):
                booking.payment.status = "REFUNDED"
                booking.payment.save()
            else:
                Payment.objects.create(
                    booking=booking,
                    amount=5000,
                    status="REFUNDED"
                )

        return Response(
            {
                "message": "Refund processed successfully",
                "state": booking.state
            }
        )
