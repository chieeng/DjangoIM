from django.shortcuts import render
from .models import Reservation, Booking


def reservation_list(request):
    """List reservations"""
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(customer=request.user)
    else:
        reservations = Reservation.objects.none()
    context = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', context)


def my_bookings(request):
    """View user's bookings"""
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(reservation__customer=request.user)
    else:
        bookings = Booking.objects.none()
    context = {'bookings': bookings}
    return render(request, 'reservations/my_bookings.html', context)
