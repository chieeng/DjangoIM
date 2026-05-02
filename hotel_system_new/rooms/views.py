from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Room, RoomType, RoomAssignment
from reservations.models import Reservation
from .forms import RoomForm, RoomTypeForm, RoomAssignmentForm
from reservations.forms import ReservationForm


def staff_or_admin_required(view_func):
    """Decorator to ensure only staff or admin can access"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if request.user.role_type not in ['staff', 'admin']:
            messages.error(request, 'You do not have permission to access the rooms management system. Only staff and administrators can access this area.')
            return redirect('common:index')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required(login_url='accounts:login')
def index(request):
    """Rooms app dashboard - Staff/Admin only"""
    # Restrict to staff and admin only
    if request.user.is_authenticated and request.user.role_type not in ['staff', 'admin']:
        messages.error(request, 'You do not have permission to access the rooms management system.')
        return redirect('common:index')
    
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # Calculate room statistics
    total_rooms = Room.objects.count()
    available_rooms = Room.objects.filter(status='available').count()
    occupied_rooms = Room.objects.filter(status='occupied').count()
    maintenance_rooms = Room.objects.filter(status='maintenance').count()
    reserved_rooms = Room.objects.filter(status='reserved').count()
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Get data for display
    room_types = RoomType.objects.all()
    recent_reservations = Reservation.objects.all().order_by('-created_at')[:5]
    all_rooms = Room.objects.all().order_by('room_number')
    
    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'maintenance_rooms': maintenance_rooms,
        'reserved_rooms': reserved_rooms,
        'occupancy_rate': occupancy_rate,
        'room_types': room_types,
        'recent_reservations': recent_reservations,
        'all_rooms': all_rooms,
    }
    return render(request, 'rooms/dashboard.html', context)


@login_required(login_url='accounts:login')
def room_list(request):
    """List all rooms with filtering options"""
    # Start with all rooms
    rooms = Room.objects.all()
    room_types = RoomType.objects.filter(is_active=True)
    
    # Apply filters from GET parameters
    if request.GET.get('room_type'):
        rooms = rooms.filter(room_type_id=request.GET.get('room_type'))
    
    if request.GET.get('status'):
        rooms = rooms.filter(status=request.GET.get('status'))
    else:
        # By default, show only available rooms to guests
        if not (request.user.is_authenticated and request.user.role_type in ['staff', 'admin']):
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
    
    # Sort by room number
    rooms = rooms.order_by('room_number')
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
        'total_rooms': Room.objects.count(),
    }
    return render(request, 'rooms/room_listing.html', context)


@login_required(login_url='accounts:login')
def room_detail(request, pk):
    """Room detail view"""
    room = Room.objects.get(room_id=pk)
    context = {'room': room}
    return render(request, 'rooms/room_detail.html', context)


# Add New Records Views

@staff_or_admin_required
@login_required(login_url='accounts:login')
def add_room_type(request):
    """Add new room type (Staff/Admin only)"""
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


@staff_or_admin_required
@login_required(login_url='accounts:login')
def add_room(request):
    """Add new room (Staff/Admin only)"""
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


@staff_or_admin_required
@login_required(login_url='accounts:login')
def add_reservation(request):
    """Add new reservation (Staff/Admin only)"""
    # Need to import CustomUser from accounts
    from accounts.models import CustomUser
    
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


@staff_or_admin_required
@login_required(login_url='accounts:login')
def add_room_assignment(request):
    """Add new room assignment (Staff/Admin only)"""
    if request.method == 'POST':
        form = RoomAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room assignment created successfully!')
            return redirect('rooms:index')
    else:
        form = RoomAssignmentForm()
    
    context = {'form': form, 'title': 'Add New Room Assignment'}
    return render(request, 'rooms/addNewRoomAssignment.html', context)
