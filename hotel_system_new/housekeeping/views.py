from django.shortcuts import render
from .models import Housekeeping


def housekeeping_tasks(request):
    """View housekeeping tasks"""
    tasks = Housekeeping.objects.all()
    context = {'tasks': tasks}
    return render(request, 'housekeeping/tasks.html', context)
