from django import forms
from .models import Service, ServiceCategory, ServiceRequest

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = '__all__'

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = '__all__'