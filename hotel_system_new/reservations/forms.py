from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation, Booking

ACTIVE_RESERVATION_STATUSES = ('pending', 'confirmed', 'checked_in')


class ReservationForm(forms.ModelForm):
    """Form for creating/editing reservations"""
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_guests', 'reservation_status', 'special_request']
        widgets = {
            'room': forms.Select(attrs={
                'class': 'form-control'
            }),
            'check_in_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'check_out_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests',
                'min': '1'
            }),
            'reservation_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'special_request': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests? (optional)',
                'rows': 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        status = cleaned_data.get('reservation_status')

        if not room or not check_in or not check_out:
            return cleaned_data
        if check_out <= check_in:
            raise ValidationError('Check-out date must be after check-in date.')
        if status not in ACTIVE_RESERVATION_STATUSES:
            return cleaned_data

        overlapping = Reservation.objects.filter(
            room=room,
            reservation_status__in=ACTIVE_RESERVATION_STATUSES,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
        )
        if self.instance.pk:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise ValidationError(
                'This room already has a reservation for the selected dates.'
            )
        return cleaned_data


class BookingForm(forms.ModelForm):
    """Form for creating/editing bookings"""
    class Meta:
        model = Booking
        fields = ['reservation', 'total_amount', 'booking_status']
        widgets = {
            'reservation': forms.Select(attrs={
                'class': 'form-control'
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total amount',
                'step': '0.01',
                'type': 'number'
            }),
            'booking_status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
