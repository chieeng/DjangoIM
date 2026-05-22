from django.shortcuts import render, redirect
from .forms import ServiceForm, ServiceCategoryForm, ServiceRequestForm

def index(request):
    return render(request, 'index.html')

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ServiceForm()
    return render(request, 'services/addNewService.html', {'form': form})

def add_service_category(request):
    if request.method == 'POST':
        form = ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ServiceCategoryForm()
    return render(request, 'services/addNewServiceCategory.html', {'form': form})

def add_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/addNewServiceRequest.html', {'form': form})

@login_required(login_url='accounts:login')
def service_list(request):
    return render(request, 'services/index.html')