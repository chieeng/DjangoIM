from django.shortcuts import render, redirect
from .models import Housekeeping
from .forms import HousekeepingForm


def housekeeping_tasks(request):
    """View housekeeping tasks"""
    tasks = Housekeeping.objects.all()
    context = {'tasks': tasks}
    return render(request, 'housekeeping/tasks.html', context)


def housekeeping_index(request):
    """View all housekeeping tasks"""
    tasks = Housekeeping.objects.all()
    return render(request, 'housekeeping/index.html', {'tasks': tasks})


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