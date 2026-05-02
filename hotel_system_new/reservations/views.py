from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Reservation, Booking
from .forms import UserReservationForm

User = get_user_model()


def reservation_list(request):
    """List reservations"""
    if not request.session.get('username'):
        return redirect('accounts:login')

    try:
        current_user = User.objects.get(username=request.session['username'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('accounts:login')

    reservations = Reservation.objects.filter(customer=current_user)

    context = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', context)


def my_bookings(request):
    """View user's bookings"""
    if not request.session.get('username'):
        return redirect('accounts:login')

    try:
        current_user = User.objects.get(username=request.session['username'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('accounts:login')

    bookings = Booking.objects.filter(reservation__customer=current_user)

    context = {'bookings': bookings}
    return render(request, 'reservations/my_bookings.html', context)


def add_record(request):
    """Create a new reservation record for the logged-in user."""
    if not request.session.get('username'):
        return redirect('accounts:login')

    try:
        current_user = User.objects.get(username=request.session['username'])
    except User.DoesNotExist:
        request.session.flush()
        return redirect('accounts:login')

    if request.method == 'POST':
        form = UserReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = current_user
            reservation.save()
            messages.success(request, 'New reservation record added successfully.')
            return redirect('common:index')
    else:
        form = UserReservationForm()

    return render(request, 'reservations/add_record.html', {'form': form})
