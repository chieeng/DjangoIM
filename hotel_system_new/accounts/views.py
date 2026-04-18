from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomerProfileForm
from .models import CustomUser, CustomerProfile


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            CustomerProfile.objects.create(user=user)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    """View user profile"""
    try:
        customer_profile = request.user.customer_profile
    except:
        customer_profile = None
    
    return render(request, 'accounts/profile.html', {'customer_profile': customer_profile})


@login_required(login_url='login')
def edit_profile(request):
    """Edit user profile"""
    try:
        customer_profile = request.user.customer_profile
    except:
        customer_profile = CustomerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=customer_profile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
