from django import forms
from django.core.exceptions import ValidationError
from .models import Service, ServiceCategory, ServiceRequest


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    def clean_service_name(self):
        name = self.cleaned_data['service_name'].strip()
        qs = Service.objects.filter(service_name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('A service with this name already exists.')
        return name


class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

    def clean_category_name(self):
        name = self.cleaned_data['category_name'].strip()
        qs = ServiceCategory.objects.filter(category_name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('A category with this name already exists.')
        return name


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['service', 'request_date', 'quantity', 'status', 'notes']
        labels = {
            'service': 'Service ID',
        }
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'request_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].required = True
        self.fields['service'].queryset = Service.objects.order_by('service_name')

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        request_date = cleaned_data.get('request_date')
        quantity = cleaned_data.get('quantity')
        status = cleaned_data.get('status')

        if not service or not request_date:
            return cleaned_data

        qs = ServiceRequest.objects.filter(
            service=service,
            request_date=request_date,
            quantity=quantity,
            status=status,
        )
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError(
                'A service request with this service, date, quantity, and status already exists.'
            )
        return cleaned_data
