from django import forms
from accounts.staff_querysets import get_staff_user_queryset, staff_user_label
from maintenance.models import MaintenanceRequest
from .models import StaffAssignment


class StaffAssignmentForm(forms.ModelForm):
    class Meta:
        model = StaffAssignment
        fields = [
            'staff',
            'maintenance_request',
            'assigned_date',
            'completion_date',
            'assignment_status',
        ]
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_request': forms.Select(attrs={'class': 'form-control'}),
            'assigned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'assignment_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = get_staff_user_queryset()
        self.fields['staff'].label_from_instance = staff_user_label
        self.fields['maintenance_request'].queryset = MaintenanceRequest.objects.select_related(
            'room'
        ).order_by('-report_date', '-maintenance_id')
        self.fields['maintenance_request'].empty_label = 'Select maintenance request'