from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from .forms import BookingForm
from .models import Booking
from rooms.models import Room

@never_cache
@login_required(login_url='accounts:login')
def index(request):
    bookings = Booking.objects.filter(customer=request.user)
    context = {
        'bookings': bookings,
        'total_count': bookings.count(),
        'pending_count': bookings.filter(booking_status='pending').count(),
        'confirmed_count': bookings.filter(booking_status='confirmed').count(),
        'cancelled_count': bookings.filter(booking_status='cancelled').count(),
    }
    return render(request, 'booking/index.html', context)

@never_cache
@login_required(login_url='accounts:login')
def add_booking(request, room_id=None):
    if room_id is None:
        messages.info(request, 'Please choose a room before submitting a booking request.')
        return redirect('rooms:room_list')

    selected_room = get_object_or_404(Room, pk=room_id) if room_id is not None else None

    if request.method == 'POST':
        form = BookingForm(request.POST, selected_room=selected_room)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.customer_name = request.user.get_full_name() or request.user.username
            booking.room = selected_room
            booking.room_name = selected_room.room_type.type_name if selected_room.room_type else f"Room {selected_room.room_number}"
            booking.room_number = selected_room.room_number
            booking.booking_status = 'pending'
            booking.save()
            messages.success(request, 'Your booking request has been submitted for admin approval.')
            return redirect('booking:index')
    else:
        form = BookingForm(selected_room=selected_room)

    return render(request, 'booking/addNewBooking.html', {
        'form': form,
        'selected_room': selected_room,
    })


@never_cache
@staff_member_required(login_url='accounts:login')
def admin_dashboard(request):
    bookings = Booking.objects.select_related('customer', 'room')
    status_filter = request.GET.get('status', 'pending')
    if status_filter != 'all':
        bookings = bookings.filter(booking_status=status_filter)

    all_bookings = Booking.objects.all()
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'pending_count': all_bookings.filter(booking_status='pending').count(),
        'confirmed_count': all_bookings.filter(booking_status='confirmed').count(),
        'cancelled_count': all_bookings.filter(booking_status='cancelled').count(),
        'total_count': all_bookings.count(),
    }
    return render(request, 'booking/admin_dashboard.html', context)


@require_POST
@staff_member_required(login_url='accounts:login')
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.booking_status != 'pending':
        messages.warning(request, f'Booking #{booking.id} is already {booking.get_booking_status_display().lower()}.')
    else:
        booking.booking_status = 'confirmed'
        booking.save(update_fields=['booking_status'])
        messages.success(request, f'Booking #{booking.id} has been approved.')
    return redirect('booking:admin_dashboard')


@require_POST
@staff_member_required(login_url='accounts:login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.booking_status == 'cancelled':
        messages.warning(request, f'Booking #{booking.id} is already cancelled.')
    else:
        booking.booking_status = 'cancelled'
        booking.save(update_fields=['booking_status'])
        messages.success(request, f'Booking #{booking.id} has been cancelled.')
    return redirect('booking:admin_dashboard')
