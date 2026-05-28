from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from .models import Room, RoomType, RoomAssignment
from reservations.models import Reservation
from .forms import RoomForm, RoomTypeForm, RoomAssignmentForm
from reservations.forms import ReservationForm


def staff_or_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role_type not in ['staff', 'admin']:
            messages.error(request, 'You do not have permission to access the rooms management system.')
            return redirect('common:index')
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.user.role_type not in ['staff', 'admin']:
        messages.error(request, 'You do not have permission to access the rooms management system.')
        return redirect('common:index')

    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='available').count()
    occupied_rooms = Room.objects.filter(status='occupied').count()
    maintenance_rooms = Room.objects.filter(status='maintenance').count()
    reserved_rooms = Room.objects.filter(status='reserved').count()
    cleaning_rooms = Room.objects.filter(status='cleaning').count()
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

    room_types = RoomType.objects.all()
    all_rooms = Room.objects.select_related('room_type').order_by('room_number')

    pending_qs = Reservation.objects.filter(
        reservation_status='pending'
    ).select_related('room', 'room__room_type', 'customer').order_by('room_id', 'reservation_date')

    room_priority_counter = defaultdict(int)
    pending_with_priority = []
    for res in pending_qs:
        room_priority_counter[res.room_id] += 1
        pending_with_priority.append((res, room_priority_counter[res.room_id]))

    recent_reservations = Reservation.objects.exclude(
        reservation_status='pending'
    ).select_related('room', 'customer').order_by('-reservation_date')[:10]

    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'maintenance_rooms': maintenance_rooms,
        'reserved_rooms': reserved_rooms,
        'cleaning_rooms': cleaning_rooms,
        'occupancy_rate': occupancy_rate,
        'room_types': room_types,
        'pending_with_priority': pending_with_priority,
        'recent_reservations': recent_reservations,
        'all_rooms': all_rooms,
        'status_choices': Room.STATUS_CHOICES,
    }
    return render(request, 'rooms/dashboard.html', context)


def room_list(request):
    rooms = Room.objects.select_related('room_type').all()
    room_types = RoomType.objects.all()

    if request.GET.get('room_type'):
        rooms = rooms.filter(room_type_id=request.GET.get('room_type'))

    if request.GET.get('status'):
        rooms = rooms.filter(status=request.GET.get('status'))
    elif not (request.user.is_authenticated and request.user.role_type in ['staff', 'admin']):
        rooms = rooms.filter(status='available')

    if request.GET.get('min_price'):
        try:
            rooms = rooms.filter(price_per_night__gte=float(request.GET.get('min_price')))
        except ValueError:
            pass

    if request.GET.get('max_price'):
        try:
            rooms = rooms.filter(price_per_night__lte=float(request.GET.get('max_price')))
        except ValueError:
            pass

    rooms = rooms.order_by('floor_number', 'room_number')

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'total_rooms': Room.objects.count(),
    }
    return render(request, 'rooms/room_listing.html', context)


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    context = {'room': room}
    return render(request, 'rooms/room_detail.html', context)


def room_type_list(request):
    room_types = RoomType.objects.all().prefetch_related('rooms')
    context = {'room_types': room_types}
    return render(request, 'rooms/room_type_list.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def add_room_type(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room type added successfully!')
            return redirect('rooms:index')
    else:
        form = RoomTypeForm()
    context = {'form': form, 'title': 'Add New Room Type'}
    return render(request, 'rooms/addNewRoomType.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room added successfully!')
            return redirect('rooms:index')
    else:
        form = RoomForm()
    context = {'form': form, 'title': 'Add New Room'}
    return render(request, 'rooms/addNewRoom.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def add_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.save()
            messages.success(request, 'Reservation created successfully!')
            return redirect('rooms:index')
    else:
        form = ReservationForm()
    context = {'form': form, 'title': 'Add New Reservation'}
    return render(request, 'rooms/addNewReservation.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def add_room_assignment(request):
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            assignment.room.status = 'occupied'
            assignment.room.save()
            assignment.reservation.reservation_status = 'checked_in'
            assignment.reservation.save()
            messages.success(request, 'Room assignment created. Guest checked in.')
            return redirect('rooms:index')
    else:
        form = RoomAssignmentForm()
    context = {'form': form, 'title': 'Add New Room Assignment'}
    return render(request, 'rooms/addNewRoomAssignment.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room {room.room_number} updated successfully!')
            return redirect('rooms:index')
    else:
        form = RoomForm(instance=room)
    context = {'form': form, 'title': f'Edit Room {room.room_number}', 'room': room}
    return render(request, 'rooms/editRoom.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def edit_room_type(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)
    if request.method == 'POST':
        form = RoomTypeForm(request.POST, instance=room_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room type "{room_type.type_name}" updated successfully!')
            return redirect('rooms:index')
    else:
        form = RoomTypeForm(instance=room_type)
    context = {'form': form, 'title': f'Edit Room Type: {room_type.type_name}', 'room_type': room_type}
    return render(request, 'rooms/editRoomType.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_number = room.room_number
        room.delete()
        messages.success(request, f'Room {room_number} deleted successfully!')
        return redirect('rooms:index')
    context = {'room': room}
    return render(request, 'rooms/confirmDeleteRoom.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def delete_room_type(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)
    if request.method == 'POST':
        name = room_type.type_name
        room_type.delete()
        messages.success(request, f'Room type "{name}" deleted successfully!')
        return redirect('rooms:index')
    context = {'room_type': room_type}
    return render(request, 'rooms/confirmDeleteRoomType.html', context)


@login_required(login_url='accounts:login')
@staff_or_admin_required
def update_room_status(request, pk):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=pk)
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in Room.STATUS_CHOICES]
        if new_status in valid_statuses:
            room.status = new_status
            room.save()
            messages.success(request, f'Room {room.room_number} status updated to "{room.get_status_display()}".')
        else:
            messages.error(request, 'Invalid status value.')
    return redirect('rooms:index')
