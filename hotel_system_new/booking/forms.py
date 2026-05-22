from django import forms
from django.utils import timezone
from .models import Booking


class BookingForm(forms.ModelForm):
    room_name = forms.CharField(
        required=False,
        label='Room',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    room_number = forms.CharField(
        required=True,
        error_messages={'required': 'Room number is required.'},
        widget=forms.HiddenInput(),
    )
    check_in_date = forms.DateField(
        required=True,
        error_messages={'required': 'Check-in date is required.'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    check_out_date = forms.DateField(
        required=True,
        error_messages={'required': 'Check-out date is required.'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = Booking
        fields = ('room_name', 'room_number', 'check_in_date', 'check_out_date')

    def __init__(self, *args, selected_room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_room = selected_room
        if selected_room is not None:
            room_name = f"Room {selected_room.room_number}"
            self.fields['room_name'].initial = room_name
            self.fields['room_name'].disabled = True
            self.fields['room_number'].initial = selected_room.room_number
            self.fields['room_number'].disabled = True
        else:
            self.fields['room_name'].help_text = 'Choose a room from the room list to fill this automatically.'

    def clean_room_name(self):
        room_name = self.cleaned_data.get('room_name', '').strip()
        if self.selected_room is not None and not room_name:
            raise forms.ValidationError('Room is required.')
        return room_name

    def clean_room_number(self):
        room_number = self.cleaned_data.get('room_number', '').strip()
        if not room_number:
            raise forms.ValidationError('Room number is required.')
        return room_number

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        room_number = cleaned_data.get('room_number')

        if self.selected_room is not None:
            cleaned_data['room_name'] = self.selected_room.room_type.type_name if self.selected_room.room_type else f"Room {self.selected_room.room_number}"
            cleaned_data['room_number'] = self.selected_room.room_number
            room_number = self.selected_room.room_number

        if check_in_date and check_in_date < timezone.localdate():
            self.add_error('check_in_date', 'Check-in date cannot be in the past.')

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            self.add_error('check_out_date', 'Check-out date must be after check-in date.')
            return cleaned_data

        if room_number and check_in_date and check_out_date:
            overlapping_booking_exists = Booking.objects.filter(
                room_number__iexact=room_number,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date,
            ).exclude(booking_status='cancelled').exists()

            if overlapping_booking_exists:
                self.add_error(
                    'room_number',
                    'This room already has a booking that overlaps the selected dates.',
                )

        return cleaned_data
