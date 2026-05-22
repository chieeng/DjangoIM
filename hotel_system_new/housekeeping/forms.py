from django import forms
from accounts.staff_querysets import get_staff_user_queryset, staff_user_label
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = get_staff_user_queryset()
        self.fields['staff'].label_from_instance = staff_user_label