from django import forms
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from .models import Reservation, Booking


class ReservationAdminForm(forms.ModelForm):
    """Custom form for Reservation to display room price"""
    
    class Meta:
        model = Reservation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    list_display = ('reservation_id', 'customer', 'room_display', 'check_in_date', 'check_out_date', 'nights_display', 'room_price_display', 'status_display')
    list_filter = ('reservation_status', 'check_in_date', 'check_out_date')
    search_fields = ('customer__username', 'room__room_number', 'reservation_id')
    readonly_fields = ('reservation_id', 'reservation_date', 'room_details', 'calculated_total')
    fieldsets = (
        ('Reservation Details', {
            'fields': ('reservation_id', 'customer', 'reservation_date')
        }),
        ('Room Selection', {
            'fields': ('room', 'room_details')
        }),
        ('Booking Dates', {
            'fields': ('check_in_date', 'check_out_date')
        }),
        ('Guest Information', {
            'fields': ('number_of_guests', 'special_request')
        }),
        ('Booking Cost', {
            'fields': ('calculated_total',),
            'description': '<strong>This will be used to calculate booking total amount</strong>'
        }),
        ('Status', {
            'fields': ('reservation_status',)
        })
    )

    def room_display(self, obj):
        """Display room number with price"""
        if obj.room:
            price_fmt = f'{obj.room.price_per_night:.2f}'
            return format_html(
                '{} (₱{}/night)',
                obj.room.room_number,
                price_fmt
            )
        return 'N/A'
    room_display.short_description = 'Room'

    def nights_display(self, obj):
        """Display number of nights"""
        nights = obj.get_number_of_nights()
        return format_html(
            '<strong>{} nights</strong>',
            nights if nights > 0 else 0
        )
    nights_display.short_description = 'Nights'

    def room_price_display(self, obj):
        """Display room nightly price"""
        price = obj.get_room_price()
        formatted = f'{price:.2f}'
        return format_html(
            '<span style="color: green; font-weight: bold;">₱{}/night</span>',
            formatted
        )
    room_price_display.short_description = 'Room Price'

    def status_display(self, obj):
        """Display reservation status with color coding"""
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'checked_in': 'green',
            'checked_out': 'gray',
            'cancelled': 'red'
        }
        color = colors.get(obj.reservation_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_reservation_status_display()
        )
    status_display.short_description = 'Status'

    def room_details(self, obj):
        """Display comprehensive room and pricing details"""
        if not obj.room:
            return mark_safe('<span style="color: red;">No room selected</span>')
        
        room_price = obj.get_room_price()
        price_formatted = f'₱{room_price:.2f}'
        
        return format_html(
            '<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">'
            '<p><strong>Room:</strong> {}</p>'
            '<p><strong>Room Type:</strong> {}</p>'
            '<p><strong>Price per Night:</strong> {}</p>'
            '<p><strong>Floor:</strong> {}</p>'
            '</div>',
            obj.room.room_number,
            obj.room.room_type.type_name if obj.room.room_type else 'N/A',
            price_formatted,
            obj.room.floor_number
        )
    room_details.short_description = 'Room Details'

    def calculated_total(self, obj):
        """Display calculated total amount for the booking"""
        if not obj.room:
            return mark_safe('<span style="color: red;">Select a room first</span>')
        
        nights = obj.get_number_of_nights()
        room_price = obj.get_room_price()
        total = obj.calculate_total_amount()
        
        if nights <= 0:
            return mark_safe('<span style="color: orange;">Set check-in and check-out dates</span>')
        
        rate_formatted = f'₱{room_price:.2f}'
        total_formatted = f'₱{total:.2f}'
        
        return format_html(
            '<div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px;">'
            '<p><strong>Nights:</strong> {}</p>'
            '<p><strong>Rate per Night:</strong> {}</p>'
            '<p style="margin-top: 10px; border-top: 1px solid #ccc; padding-top: 10px;">'
            '<strong style="font-size: 16px; color: green;">Total: {}</strong></p>'
            '</div>',
            nights,
            rate_formatted,
            total_formatted
        )
    calculated_total.short_description = 'Calculated Total Amount'


class BookingAdminForm(forms.ModelForm):
    """Custom form for Booking to auto-calculate total_amount"""
    
    class Meta:
        model = Booking
        fields = ['reservation', 'booking_status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if self.instance.reservation:
                self.instance.total_amount = self.instance.reservation.calculate_total_amount()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    form = BookingAdminForm
    list_display = ('booking_id', 'reservation_info', 'booking_date', 'nights_display', 'rate_display', 'amount_display', 'status_display')
    list_filter = ('booking_status', 'booking_date')
    search_fields = ('booking_id', 'reservation__reservation_id', 'reservation__customer__username')
    readonly_fields = ('booking_id', 'booking_date', 'total_amount', 'booking_info', 'cost_breakdown')
    fieldsets = (
        ('Booking Details', {
            'fields': ('booking_id', 'reservation', 'booking_date', 'booking_info')
        }),
        ('Cost Breakdown', {
            'fields': ('cost_breakdown',),
            'description': '<strong>Total amount is automatically calculated based on room price and reservation dates</strong>'
        }),
        ('Financial Information', {
            'fields': ('total_amount',),
        }),
        ('Status', {
            'fields': ('booking_status',)
        })
    )

    def reservation_info(self, obj):
        """Display reservation information"""
        if not obj.reservation:
            return 'N/A'
        res = obj.reservation
        return format_html(
            'Res #{} - {}<br/><small>Room: {} | Guest: {}</small>',
            res.reservation_id,
            res.get_reservation_status_display(),
            res.room.room_number if res.room else 'N/A',
            res.customer.username
        )
    reservation_info.short_description = 'Reservation'

    def nights_display(self, obj):
        """Display number of nights"""
        if obj.reservation:
            nights = obj.reservation.get_number_of_nights()
            return format_html('<strong>{}</strong>', nights)
        return 'N/A'
    nights_display.short_description = 'Nights'

    def rate_display(self, obj):
        """Display room nightly rate"""
        if obj.reservation and obj.reservation.room:
            rate = obj.reservation.get_room_price()
            rate_formatted = f'₱{rate:.2f}'
            return format_html(
                '<span style="color: blue;">{}</span>',
                rate_formatted
            )
        return 'N/A'
    rate_display.short_description = 'Rate/Night'

    def amount_display(self, obj):
        """Display amount with currency formatting"""
        amount_formatted = f'₱{obj.total_amount:,.2f}'
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 16px;">{}</span>',
            amount_formatted
        )
    amount_display.short_description = 'Total Amount'

    def status_display(self, obj):
        """Display booking status with color coding"""
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.booking_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_booking_status_display()
        )
    status_display.short_description = 'Status'

    def booking_info(self, obj):
        """Display comprehensive booking information"""
        if not obj.reservation:
            return 'Select a reservation first'
        
        res = obj.reservation
        return format_html(
            '<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">'
            '<p><strong>Customer:</strong> {}</p>'
            '<p><strong>Room:</strong> {} (Floor {})</p>'
            '<p><strong>Check-in:</strong> {}</p>'
            '<p><strong>Check-out:</strong> {}</p>'
            '<p><strong>Number of Guests:</strong> {}</p>'
            '</div>',
            res.customer.get_full_name() or res.customer.username,
            res.room.room_number if res.room else 'N/A',
            res.room.floor_number if res.room else 'N/A',
            res.check_in_date,
            res.check_out_date,
            res.number_of_guests
        )
    booking_info.short_description = 'Booking Information'

    def cost_breakdown(self, obj):
        """Display cost breakdown with calculation"""
        if not obj.reservation:
            return mark_safe('<span style="color: red;">Select a reservation to see cost breakdown</span>')
        
        res = obj.reservation
        nights = res.get_number_of_nights()
        rate = res.get_room_price()
        total = res.calculate_total_amount()
        rate_fmt = f'{rate:.2f}'
        total_fmt = f'{total:.2f}'

        return format_html(
            '<div style="background-color: #e3f2fd; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;">'
            '<table style="width: 100%; font-size: 14px;">'
            '<tr><td><strong>Room:</strong></td><td style="text-align: right;">{}</td></tr>'
            '<tr><td><strong>Nightly Rate:</strong></td><td style="text-align: right;">₱{}</td></tr>'
            '<tr><td><strong>Number of Nights:</strong></td><td style="text-align: right;"><strong>{}</strong></td></tr>'
            '<tr style="border-top: 2px solid #2196F3; margin-top: 10px;">'
            '<td><strong style="font-size: 16px;">TOTAL:</strong></td>'
            '<td style="text-align: right;"><strong style="font-size: 16px; color: green;">₱{}</strong></td>'
            '</tr>'
            '</table>'
            '</div>',
            res.room.room_number if res.room else 'N/A',
            rate_fmt,
            nights if nights > 0 else 0,
            total_fmt
        )
    cost_breakdown.short_description = 'Cost Breakdown'

    def save_model(self, request, obj, form, change):
        """Override save to auto-calculate total_amount from reservation"""
        if obj.reservation:
            obj.total_amount = obj.reservation.calculate_total_amount()
        super().save_model(request, obj, form, change)