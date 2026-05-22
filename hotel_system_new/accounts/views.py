from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm
from .models import CustomUser, CustomerProfile

User = get_user_model()


def register(request):
    """User registration view"""
    if request.session.get('username'):
        return redirect('common:index')

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
    if request.session.get('username'):
        return redirect('common:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if form.is_valid():
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    request.session['username'] = user.username
                    request.session['user_type'] = user.role_type
                    messages.success(request, f'Welcome, {user.first_name or user.username}!')
                    return redirect('common:index')

                messages.error(request, 'Invalid credentials')
            except User.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """User logout view"""
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


def profile(request):
    """View user profile"""
    if not request.session.get('username'):
        return redirect('accounts:login')

    current_user = get_object_or_404(User, username=request.session['username'])

    try:
        customer_profile = current_user.customer_profile
    except CustomerProfile.DoesNotExist:
        customer_profile = None
    
    return render(
        request,
        'accounts/profile.html',
        {
            'customer_profile': customer_profile,
            'current_user': current_user,
        }
    )


def edit_profile(request):
    """Edit user profile fields required by specification."""
    if not request.session.get('username'):
        return redirect('accounts:login')

    user_instance = get_object_or_404(User, username=request.session['username'])

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_instance)
        if form.is_valid():
            updated_user = form.save(commit=False)
            password = form.cleaned_data.get('password', '').strip()
            if password:
                updated_user.set_password(password)
            updated_user.save()

            request.session['username'] = updated_user.username
            request.session['user_type'] = updated_user.role_type
            messages.success(request, 'Profile updated successfully!')
            return redirect('common:index')
    else:
        form = UserProfileForm(instance=user_instance)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})
