from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StaffAssignment
from .forms import StaffAssignmentForm


@login_required(login_url='accounts:login')
def staff_dashboard(request):
    """Staff dashboard view"""
    if request.user.is_authenticated and hasattr(request.user, 'staff_profile'):
        assignments = StaffAssignment.objects.filter(staff=request.user)
    else:
        assignments = []
    context = {'assignments': assignments}
    return render(request, 'staff/dashboard.html', context)


@login_required(login_url='accounts:login')
def staff_index(request):
    """View all staff assignments"""
    assignments = StaffAssignment.objects.all()
    return render(request, 'staff/index.html', {'assignments': assignments})


@login_required(login_url='accounts:login')
def add_staff_assignment(request):
    """Add new staff assignment"""
    if request.method == 'POST':
        form = StaffAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff:index')
    else:
        form = StaffAssignmentForm()
    return render(request, 'staff/addNewStaffAssignment.html', {'form': form})