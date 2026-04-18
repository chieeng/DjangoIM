from django import forms
from .models import Housekeeping

class HousekeepingForm(forms.ModelForm):
    class Meta:
        model = Housekeeping
        fields = ['room', 'staff', 'cleaning_date', 'status', 'remarks']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'cleaning_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }