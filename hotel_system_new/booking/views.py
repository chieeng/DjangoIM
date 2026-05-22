from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .forms import BookingForm
from .models import Booking

@never_cache
@login_required(login_url='accounts:login')
def index(request):
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'pending_count': bookings.filter(booking_status='pending').count(),
        'confirmed_count': bookings.filter(booking_status='confirmed').count(),
    }
    return render(request, 'booking/index.html', context)

@never_cache
@login_required(login_url='accounts:login')
def add_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.customer_name = request.user.get_full_name() or request.user.username
            booking.save()
            messages.success(request, 'Your booking has been created.')
            return redirect('booking:index')
    else:
        form = BookingForm()

    return render(request, 'booking/addNewBooking.html', {'form': form})
