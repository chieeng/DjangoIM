from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ReportForm
from .models import Report


@login_required(login_url='accounts:login')
def index(request):
    reports = Report.objects.all()
    summary = {
        'total_reports': reports.count(),
        'total_revenue': sum(report.revenue for report in reports),
        'average_occupancy': round(
            (sum(report.occupancy_rate for report in reports) / reports.count())
            if reports.count() else 0,
            2,
        ),
    }
    return render(request, 'reports/index.html', {
        'reports': reports,
        'summary': summary,
        'title': 'Reports Dashboard',
    })


@login_required(login_url='accounts:login')
def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reports:index')
    else:
        form = ReportForm()

    return render(request, 'reports/addNewReport.html', {
        'form': form,
        'title': 'Add New Booking Report',
    })
