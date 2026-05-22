from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomerProfileForm, UserProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm
from .models import CustomUser, CustomerProfile

User = get_user_model()


@never_cache
def register(request):
    """User registration view"""
    if request.session.get('username'):
        return redirect('common:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create customer profile
            CustomerProfile.objects.create(
                user=user,
                id_number=CustomerProfile.generate_pending_id_number(user.user_id),
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@never_cache
def login_view(request):
    """User login view"""
    if request.session.get('username'):
        return redirect('common:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if form.is_valid():
            credential = form.cleaned_data.get('username', '').strip()
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=credential, password=password)
            if user is None:
                try:
                    matched_user = CustomUser.objects.get(email__iexact=credential)
                except CustomUser.DoesNotExist:
                    matched_user = None

                if matched_user is not None:
                    user = authenticate(request, username=matched_user.username, password=password)

            if user is not None:
                login(request, user)
                request.session['user_id'] = user.pk
                request.session['user_email'] = user.email
                request.session['user_display_name'] = user.get_full_name() or user.username
                request.session['login_time'] = timezone.now().isoformat()
                request.session['last_activity'] = 'login'
                messages.success(request, f'Welcome, {user.first_name}!')
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect(reverse('index'))

            form.add_error(None, 'Please enter a valid email/username and password.')
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
    
    return render(request, 'accounts/login.html', {'form': form, 'next': request.GET.get('next', '')})
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """User logout view"""
    request.session.flush()
    logout(request)
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
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


@never_cache
@login_required(login_url='accounts:login')
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('new_password'):
                update_session_auth_hash(request, user)
            request.session['user_email'] = user.email
            request.session['user_display_name'] = user.get_full_name() or user.username
            request.session['last_activity'] = 'edit_profile'
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
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
