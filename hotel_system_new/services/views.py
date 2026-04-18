from django.shortcuts import render
from .models import Service, ServiceCategory


def service_list(request):
    """List all services"""
    services = Service.objects.all()
    categories = ServiceCategory.objects.all()
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/service_list.html', context)
