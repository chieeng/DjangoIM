from django import forms
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