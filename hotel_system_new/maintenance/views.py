from django.shortcuts import render
from .models import MaintenanceRequest


def maintenance_requests(request):
    """View maintenance requests"""
    requests = MaintenanceRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'maintenance/requests.html', context)
