from django import forms
from .models import Room, RoomType, RoomAssignment
from reservations.models import Reservation


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['type_name', 'description', 'max_capacity', 'price_per_night']
        widgets = {
            'type_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Standard, Deluxe, Suite'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the amenities and features',
                'rows': 3
            }),
            'max_capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Max guests (e.g. 2)',
                'min': '1',
                'max': '10'
            }),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Base price (e.g. 150.00)',
                'step': '0.01',
                'min': '0'
            }),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'floor_number', 'room_type', 'status', 'price_per_night']
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 101, A-201'
            }),
            'floor_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Floor number',
                'min': '1',
                'max': '50'
            }),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per night',
                'step': '0.01',
                'min': '0'
            }),
        }


class RoomAssignmentForm(forms.ModelForm):
    class Meta:
        model = RoomAssignment
        fields = ['reservation', 'room', 'check_in_time', 'check_out_time']
        widgets = {
            'reservation': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'check_out_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assigned_ids = RoomAssignment.objects.values_list('reservation_id', flat=True)
        self.fields['reservation'].queryset = Reservation.objects.filter(
            reservation_status='confirmed'
        ).exclude(pk__in=assigned_ids).select_related('customer', 'room')
        self.fields['room'].queryset = Room.objects.filter(
            status='reserved'
        ).select_related('room_type')
