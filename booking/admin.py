from django.contrib import admin

from .models import (
    Booking,
    RoomType,
    Room,
    Reservation,
    RoomAssignment,
    Invoice,
    Payment,
    Discount,
    Review,
)


from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_id",
        "customer",
        "booking_date",
        "total_amount",
        "booking_status",
    )

    list_filter = (
        "booking_status",
        "booking_date",
    )

    search_fields = (
        "booking_id",
        "customer__user__email",
        "customer__user__first_name",
        "customer__user__last_name",
    )

    ordering = (
        "-booking_date",
    )

    list_per_page = 20

    actions = [
        "mark_pending",
        "mark_confirmed",
        "mark_cancelled",
    ]

    @admin.action(description="Mark selected bookings as Pending")
    def mark_pending(self, request, queryset):
        queryset.update(booking_status="Pending")

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(booking_status="Confirmed")

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(booking_status="Cancelled")


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = (
        "room_type_id",
        "type_name",
        "max_capacity",
        "price_per_night",
    )
    search_fields = ("type_name",)



@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "reservation_id",
        "booking",
        "room",
        "reservation_date",
        "check_in_date",
        "check_out_date",
        "number_of_guests",
        "reservation_status",
    )
    list_filter = ("reservation_status", "check_in_date", "check_out_date")
    search_fields = ("reservation_id", "room__room_number")


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "assignment_id",
        "booking",
        "room",
        "assigned_date",
        "check_in_time",
        "check_out_time",
    )
    search_fields = ("assignment_id", "room__room_number")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_id",
        "booking",
        "issue_date",
        "due_date",
        "total_amount",
        "invoice_status",
    )
    list_filter = ("invoice_status",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "booking",
        "payment_date",
        "amount_paid",
        "payment_method",
        "payment_status",
        "transaction_reference",
    )
    list_filter = ("payment_status", "payment_method")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "discount_id",
        "booking",
        "discount_name",
        "percentage",
        "start_date",
        "end_date",
    )
    search_fields = ("discount_name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "review_id",
        "booking",
        "customer",
        "rating",
        "review_date",
    )
    list_filter = ("rating",)

    @admin.register(Room)
    class RoomAdmin(admin.ModelAdmin):
        list_display = (
            "room_id",
            "room_number",
            "room_type",
            "floor_number",
            "status",
            "price_per_night",
        )

        actions = ["mark_occupied", "mark_available"]

        @admin.action(description="Mark selected rooms as Occupied")
        def mark_occupied(self, request, queryset):
            queryset.update(status="Occupied")

        @admin.action(description="Mark selected rooms as Available")
        def mark_available(self, request, queryset):
            queryset.update(status="Available")

