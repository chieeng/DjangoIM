from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Exists, OuterRef

from .models import User, Customer
from .forms import RegisterForm, LoginForm

from booking.forms import AvailabilitySearchForm
from booking.models import Room, Reservation


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.password_hash = make_password(form.cleaned_data['password'])
            user.role_type = "Customer"
            user.status = "Active"
            user.save()

            Customer.objects.create(
                user=user,
                id_type="N/A",
                id_number="N/A"
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)

                if user.status != "Active":
                    messages.error(request, "Your account is not active.")
                    return redirect('accounts:login')

                if check_password(password, user.password_hash):
                    request.session['user_id'] = user.user_id
                    request.session['role_type'] = user.role_type

                    user.last_login = timezone.now()
                    user.save()

                    if user.role_type == "Admin":
                        return redirect('accounts:admin_dashboard')
                    elif user.role_type == "Staff":
                        return redirect('accounts:staff_dashboard')
                    else:
                        return redirect('accounts:customer_dashboard')
                else:
                    messages.error(request, "Invalid email or password.")

            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('accounts:login')


def admin_dashboard(request):
    if request.session.get('role_type') != "Admin":
        return redirect('accounts:login')

    return render(request, 'accounts/admin_dashboard.html')


def customer_dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('accounts:login')

    user = get_object_or_404(User, user_id=user_id)

    form = AvailabilitySearchForm(request.POST or None)
    available_rooms = None
    requested_check_in_date = None
    requested_check_out_date = None

    if request.method == "POST" and form.is_valid():
        requested_check_in_date = form.cleaned_data["check_in_date"]
        requested_check_out_date = form.cleaned_data["check_out_date"]

        # NOT EXISTS overlap (matches your SQL):
        # exclude rooms that have any reservation where:
        # requested_check_in < res.check_out_date AND requested_check_out > res.check_in_date
        overlap_qs = Reservation.objects.filter(
            room_id=OuterRef("room_id"),
            check_out_date__gt=requested_check_in_date,
            check_in_date__lt=requested_check_out_date,
        )

        available_rooms = (
            Room.objects.filter(status__iexact="Available")
            .annotate(_has_overlap=Exists(overlap_qs))
            .filter(_has_overlap=False)
            .select_related("room_type")
            .order_by("room_number")
        )

    return render(request, 'accounts/customer_dashboard.html', {
        'user': user,
        'form': form,
        'available_rooms': available_rooms,
        'requested_check_in_date': requested_check_in_date,
        'requested_check_out_date': requested_check_out_date,
    })


def staff_dashboard(request):
    if request.session.get('role_type') != "Staff":
        return redirect('accounts:login')

    return render(request, 'accounts/staff_dashboard.html')
