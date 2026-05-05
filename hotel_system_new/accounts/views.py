from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm, CustomerProfileForm
from .models import CustomUser, CustomerProfile


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('reports:index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('reports:index')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def profile(request):
    """View user profile"""
    customer_profile = None
    if request.user.role_type == 'customer':
        try:
            customer_profile = request.user.customer_profile
        except CustomerProfile.DoesNotExist:
            customer_profile = CustomerProfile.objects.create(user=request.user)
    
    return render(request, 'accounts/profile.html', {'customer_profile': customer_profile})


@login_required(login_url='accounts:login')
def edit_profile(request):
    """Edit user profile"""
    try:
        customer_profile = request.user.customer_profile
    except CustomerProfile.DoesNotExist:
        customer_profile = CustomerProfile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = CustomUserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
    })


@login_required(login_url='accounts:login')
def user_list(request):
    """List all users (alternative to admin)"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin only.')
        return redirect('accounts:profile')
    
    users = CustomUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})
