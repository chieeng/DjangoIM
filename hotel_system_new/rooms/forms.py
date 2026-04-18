from django import forms
from .models import Room, RoomType, RoomAssignment


class RoomTypeForm(forms.ModelForm):
    """Form for creating/editing room types"""
    class Meta:
        model = RoomType
        fields = ['type_name', 'description', 'capacity', 'price_per_night']
        widgets = {
            'type_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room type name (e.g., Standard, Deluxe)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room description',
                'rows': 3
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests (e.g., 2)',
                'min': '1'
            }),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per night (e.g., 150.00)',
                'step': '0.01',
                'type': 'number'
            }),
        }


class RoomForm(forms.ModelForm):
    """Form for creating/editing rooms"""
    class Meta:
        model = Room
        fields = ['room_number', 'floor_number', 'room_type', 'status', 'price_per_night']
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room number (e.g., 101, A-201)'
            }),
            'floor_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Floor number',
                'min': '1'
            }),
            'room_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price_per_night': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price per night',
                'step': '0.01',
                'type': 'number'
            }),
        }


class RoomAssignmentForm(forms.ModelForm):
    """Form for creating/editing room assignments"""
    class Meta:
        model = RoomAssignment
        fields = ['room', 'check_in_time', 'check_out_time']
        widgets = {
            'room': forms.Select(attrs={
                'class': 'form-control'
            }),
            'check_in_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'check_out_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }
