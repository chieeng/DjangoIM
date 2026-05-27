from django import forms
from django.utils import timezone
from .models import Reservation, Booking
from rooms.models import Room


class CustomerReservationForm(forms.ModelForm):
    """Form for customers to create reservations"""
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_guests', 'special_request']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-select'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'special_request': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any special requests? (optional)',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room'].queryset = Room.objects.filter(status='available').select_related('room_type')
        self.fields['room'].empty_label = 'Select a room...'
        self.fields['special_request'].required = False

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')
        today = timezone.now().date()

        if check_in and check_in < today:
            self.add_error('check_in_date', 'Check-in date cannot be in the past.')

        if check_in and check_out:
            if check_out <= check_in:
                self.add_error('check_out_date', 'Check-out date must be after check-in date.')

        return cleaned_data


class ReservationForm(forms.ModelForm):
    """Form for staff/admin to create/edit reservations"""
    class Meta:
        model = Reservation
        fields = ['room', 'check_in_date', 'check_out_date', 'number_of_guests', 'reservation_status', 'special_request']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests',
                'min': '1'
            }),
            'reservation_status': forms.Select(attrs={'class': 'form-control'}),
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
            'reservation': forms.Select(attrs={'class': 'form-control'}),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total amount',
                'step': '0.01',
                'type': 'number'
            }),
            'booking_status': forms.Select(attrs={'class': 'form-control'}),
        }
