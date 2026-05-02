from django import forms
from .models import Reservation, Booking


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


class UserReservationForm(forms.ModelForm):
    """Form used by customers to add a new reservation record."""
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_guests', 'special_request']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
