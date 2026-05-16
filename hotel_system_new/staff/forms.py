from django import forms
from accounts.staff_querysets import get_staff_user_queryset, staff_user_label
from .models import StaffAssignment


class StaffAssignmentForm(forms.ModelForm):
    class Meta:
        model = StaffAssignment
        fields = ['staff', 'assignment_status', 'order']
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'assignment_status': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter order details'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = get_staff_user_queryset()
        self.fields['staff'].label_from_instance = staff_user_label