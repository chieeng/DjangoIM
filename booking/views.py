from django.shortcuts import render
from django.http import HttpResponse
from .forms import BookingForm


def index(request):
    """Display booking index page"""
    return render(request, 'booking/index.html')


def add_booking(request):
    """Handle adding a new booking"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process the form
            form.save()
            return render(request, 'booking/index.html', {'success': True})
    else:
        form = BookingForm()
    return render(request, 'booking/addNewBooking.html', {'form': form})
