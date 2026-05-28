from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Reservation, Booking
from .forms import CustomerReservationForm
from rooms.models import Room


def reservation_list(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(
            customer=request.user
        ).select_related('room', 'room__room_type').order_by('-reservation_date')
    else:
        reservations = Reservation.objects.none()
    context = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', context)


def my_bookings(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(reservation__customer=request.user)
    else:
        bookings = Booking.objects.none()
    context = {'bookings': bookings}
    return render(request, 'reservations/my_bookings.html', context)


@login_required(login_url='accounts:login')
def create_reservation(request):
    selected_room = None
    room_id = request.GET.get('room')
    if room_id:
        selected_room = Room.objects.filter(pk=room_id, status='available').select_related('room_type').first()

    if request.method == 'POST':
        form = CustomerReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.reservation_status = 'pending'
            reservation.save()
            messages.success(
                request,
                f'Reservation #{reservation.reservation_id} submitted! '
                'We will review and confirm it shortly.'
            )
            return redirect('reservations:reservation_list')
    else:
        initial = {'room': selected_room} if selected_room else {}
        form = CustomerReservationForm(initial=initial, user=request.user)

    context = {
        'form': form,
        'selected_room': selected_room,
    }
    return render(request, 'reservations/create_reservation.html', context)


@login_required(login_url='accounts:login')
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, customer=request.user)
    context = {'reservation': reservation}
    return render(request, 'reservations/reservation_detail.html', context)


@login_required(login_url='accounts:login')
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, customer=request.user)
    if request.method == 'POST':
        if reservation.reservation_status in ['pending', 'confirmed']:
            was_confirmed = reservation.reservation_status == 'confirmed'
            reservation.reservation_status = 'cancelled'
            reservation.save()
            if was_confirmed and reservation.room and reservation.room.status == 'reserved':
                reservation.room.status = 'available'
                reservation.room.save()
            messages.success(request, f'Reservation #{reservation.reservation_id} has been cancelled.')
        else:
            messages.error(request, 'This reservation cannot be cancelled.')
    return redirect('reservations:reservation_list')


@login_required(login_url='accounts:login')
def confirm_reservation(request, pk):
    if request.user.role_type not in ['staff', 'admin']:
        messages.error(request, 'You do not have permission to confirm reservations.')
        return redirect('common:index')

    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=pk)

        if reservation.reservation_status != 'pending':
            messages.warning(request, 'Only pending reservations can be confirmed.')
            return redirect('rooms:index')

        reservation.reservation_status = 'confirmed'
        reservation.save()

        if reservation.room:
            reservation.room.status = 'reserved'
            reservation.room.save()

            competing = Reservation.objects.filter(
                room=reservation.room,
                reservation_status='pending'
            ).exclude(pk=reservation.pk)
            cancelled_count = competing.count()
            competing.update(reservation_status='cancelled')

            if cancelled_count:
                messages.info(
                    request,
                    f'{cancelled_count} other pending reservation(s) for Room '
                    f'{reservation.room.room_number} were automatically cancelled.'
                )

        guest = reservation.customer.get_full_name() or reservation.customer.username
        messages.success(
            request,
            f'Reservation #{reservation.reservation_id} confirmed for {guest}.'
        )

    return redirect('rooms:index')
