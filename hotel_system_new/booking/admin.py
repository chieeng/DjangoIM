from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'room_name', 'room_number', 'check_in_date', 'check_out_date', 'booking_status', 'created_at')
    list_filter = ('booking_status', 'check_in_date', 'created_at')
    search_fields = ('customer_name', 'customer__username', 'customer__email', 'room_name', 'room_number')
    actions = ('approve_bookings', 'cancel_bookings')

    @admin.action(description='Approve selected bookings')
    def approve_bookings(self, request, queryset):
        updated = queryset.filter(booking_status='pending').update(booking_status='confirmed')
        self.message_user(request, f'{updated} pending booking(s) approved.')

    @admin.action(description='Cancel selected bookings')
    def cancel_bookings(self, request, queryset):
        updated = queryset.exclude(booking_status='cancelled').update(booking_status='cancelled')
        self.message_user(request, f'{updated} booking(s) cancelled.')
