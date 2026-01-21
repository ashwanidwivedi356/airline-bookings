from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Flight, Seat, Booking, Payment


admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Booking)
admin.site.register(Payment)
