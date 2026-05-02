from django.shortcuts import render, redirect
from .forms import BookingForm

def index(request):
    return render(request, 'booking/index.html')

def add_booking(request):
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'booking/addNewBooking.html', {'form': form})