from django.urls import path
from .views import BookingCreateAPIView,BookingPaymentAPIView,BookingCancelAPIView
from .views import BookingRefundAPIView

urlpatterns = [
    path("bookings/", BookingCreateAPIView.as_view(), name="create-booking"),
    path("bookings/<int:id>/", BookingCreateAPIView.as_view()),
   
    path("bookings/<int:id>/pay/", BookingPaymentAPIView.as_view()),
    path("bookings/<int:id>/cancel/", BookingCancelAPIView.as_view()),
    path("bookings/<int:id>/refund/", BookingRefundAPIView.as_view()),
]
