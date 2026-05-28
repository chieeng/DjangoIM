from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime

from .forms import ReportForm
from .models import Report


@login_required(login_url='accounts:login')
def index(request):
    reports = Report.objects.all()
    date_filter = request.GET.get('date', '')
    if date_filter:
        try:
            d = datetime.strptime(date_filter, '%Y-%m-%d').date()
            reports = reports.filter(report_date=d)
        except ValueError:
            date_filter = ''

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
        'date_filter': date_filter,
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


@login_required(login_url='accounts:login')
@require_http_methods(["GET"])
def get_report_data(request):
    """API endpoint to fetch calculated report data for a given date"""
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)

    try:
        report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)

    # Create a temporary report object to calculate data
    temp_report = Report(report_date=report_date)
    temp_report.calculate_data()

    return JsonResponse({
        'total_bookings': temp_report.total_bookings,
        'revenue': float(temp_report.revenue),
        'occupancy_rate': float(temp_report.occupancy_rate),
    })


@login_required(login_url='accounts:login')
def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'reports/report_detail.html', {
        'report': report,
        'title': f'Report {report.report_date}',
    })


@login_required(login_url='accounts:login')
def edit_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('reports:index')
    else:
        form = ReportForm(instance=report)

    return render(request, 'reports/editReport.html', {
        'form': form,
        'report': report,
        'title': 'Edit Booking Report',
    })


@login_required(login_url='accounts:login')
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.delete()
        return redirect('reports:index')
    return render(request, 'reports/confirm_delete.html', {
        'report': report,
        'title': 'Delete Booking Report',
    })
