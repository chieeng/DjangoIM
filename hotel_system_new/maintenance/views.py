from django.shortcuts import render, redirect
from .models import MaintenanceRequest
from .forms import MaintenanceRequestForm


def maintenance_requests(request):
    """View maintenance requests"""
    requests = MaintenanceRequest.objects.all()
    context = {'requests': requests}
    return render(request, 'maintenance/requests.html', context)


def maintenance_index(request):
    """View all maintenance requests"""
    requests = MaintenanceRequest.objects.all()
    return render(request, 'maintenance/index.html', {'requests': requests})


def add_maintenance_request(request):
    """Add new maintenance request"""
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance:index')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/addNewMaintenanceRequest.html', {'form': form})