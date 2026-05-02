from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    room_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
    )
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = Booking
        fields = ('room_number', 'check_in_date', 'check_out_date')

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if check_in_date and check_out_date and check_out_date <= check_in_date:
            self.add_error('check_out_date', 'Check-out date must be after check-in date.')

        return cleaned_data
