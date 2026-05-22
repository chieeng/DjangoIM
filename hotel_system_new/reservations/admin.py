from django.contrib import admin
from .models import Reservation, Booking


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'reservation_id',
        'customer',
        'room',
        'check_in_date',
        'check_out_date',
        'reservation_status'
    )

    list_filter = ('reservation_status', 'check_in_date')
    search_fields = ('customer__username', 'room__room_number')

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_status = Reservation.objects.get(pk=obj.pk).reservation_status

        super().save_model(request, obj, form, change)

        # 🔥 Only update room if status changed
        if obj.reservation_status == 'confirmed':
            obj.room.status = 'occupied'

        elif obj.reservation_status == 'cancelled':
            obj.room.status = 'available'

        obj.room.save()