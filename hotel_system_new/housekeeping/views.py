from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Housekeeping
from .forms import HousekeepingForm


@login_required(login_url='accounts:login')
def housekeeping_tasks(request):
    """View housekeeping tasks"""
    tasks = Housekeeping.objects.all()
    context = {'tasks': tasks}
    return render(request, 'housekeeping/tasks.html', context)


@login_required(login_url='accounts:login')
def housekeeping_index(request):
    """View all housekeeping tasks"""
    tasks = Housekeeping.objects.all()
    return render(request, 'housekeeping/index.html', {'tasks': tasks})


@login_required(login_url='accounts:login')
def add_housekeeping(request):
    """Add new housekeeping task"""
    if request.method == 'POST':
        form = HousekeepingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('housekeeping:index')
    else:
        form = HousekeepingForm()
    return render(request, 'housekeeping/addNewHousekeeping.html', {'form': form})