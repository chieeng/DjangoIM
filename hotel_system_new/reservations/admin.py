from django.contrib import admin
from .models import Reservation, Booking


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_id', 'customer', 'room', 'check_in_date', 'check_out_date', 'reservation_status')
    list_filter = ('reservation_status', 'check_in_date')
    search_fields = ('customer__username', 'room__room_number')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'reservation', 'booking_date', 'total_amount', 'booking_status')
    list_filter = ('booking_status', 'booking_date')
