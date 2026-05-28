from django import forms
from .models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_date', 'notes']
        widgets = {
            'report_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'reportDateInput',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional notes about this report',
            }),
        }
