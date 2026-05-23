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
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        request_date = cleaned_data.get('request_date')
        quantity = cleaned_data.get('quantity')
        status = cleaned_data.get('status')
        notes = cleaned_data.get('notes', '')

        if not service:
            return cleaned_data

        qs = ServiceRequest.objects.filter(
            service=service,
            request_date=request_date,
            quantity=quantity,
            status=status,
            notes=notes,
        )
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This service request already exists.')
        return cleaned_data
