from django.shortcuts import render, redirect
from .forms import ServiceForm, ServiceCategoryForm, ServiceRequestForm
from .models import Service

def index(request):
    return render(request, 'services/index.html')

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services:index')
    else:
        form = ServiceForm()
    return render(request, 'services/addNewService.html', {'form': form})

def add_service_category(request):
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services:index')
    else:
        form = ServiceCategoryForm()
    return render(request, 'services/addNewServiceCategory.html', {'form': form})

def add_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services:index')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/addNewServiceRequest.html', {'form': form})

def service_list(request):
    services = Service.objects.select_related('category').all()
    return render(request, 'services/service_list.html', {'services': services})