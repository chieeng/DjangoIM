from django.shortcuts import render
from .models import StaffAssignment


def staff_dashboard(request):
    """Staff dashboard view"""
    if request.user.is_authenticated and hasattr(request.user, 'staff_profile'):
        assignments = StaffAssignment.objects.filter(staff=request.user)
    else:
        assignments = []
    context = {'assignments': assignments}
    return render(request, 'staff/dashboard.html', context)
