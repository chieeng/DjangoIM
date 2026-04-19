from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_date', 'total_bookings', 'revenue', 'occupancy_rate', 'notes']
        widgets = {
            'report_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'total_bookings': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            'revenue': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
            }),
            'occupancy_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional notes about this report',
            }),
        }
