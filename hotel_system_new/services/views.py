from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Service, ServiceCategory


@login_required(login_url='accounts:login')
def service_list(request):
    """List all services"""
    services = Service.objects.all()
    categories = ServiceCategory.objects.all()
    context = {
        'services': services,
        'categories': categories,
    }
    return render(request, 'services/service_list.html', context)
