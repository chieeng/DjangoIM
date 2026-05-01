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
    next_url = request.POST.get('next') or request.GET.get('next')
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            messages.success(request, f'Welcome, {user.first_name or user.username}!')
            return redirect(next_url or 'index')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def profile(request):
    """View user profile"""
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'accounts/profile.html', {'customer_profile': customer_profile})


@login_required(login_url='accounts:login')
def edit_profile(request):
    """Edit user profile"""
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = CustomerProfileForm(instance=customer_profile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
