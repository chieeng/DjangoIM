from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, CustomerProfile


class LoginForm(forms.Form):
    """Simple login form with username and password."""
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
    )
    phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username is None:
            raise forms.ValidationError('Username is required.')
        username = username.strip()
        if not username:
            raise forms.ValidationError('Username is required.')
        self.cleaned_data['username'] = username
        validated = super().clean_username()
        return validated if validated is not None else username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.role_type = 'customer'
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom form for user login"""
    username = forms.CharField(
        label="Email or Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email or Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Remember me'
    )

    error_messages = {
        'invalid_login': 'Please enter a valid email/username and password.',
        'inactive': 'This account is inactive.',
    }


class UserProfileForm(forms.ModelForm):
    """Form for editing basic user account details"""
    NAME_CHANGE_COOLDOWN_DAYS = 60

    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
    )
    phone = forms.CharField(
        max_length=17,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
    )
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current password'}),
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
    )
    confirm_new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
    )

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'phone', 'current_password', 'new_password', 'confirm_new_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_name = f"{self.instance.first_name} {self.instance.last_name}".strip()
        self.fields['full_name'].initial = initial_name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        existing_user = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if existing_user.exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        current_name = f"{self.instance.first_name} {self.instance.last_name}".strip()
        if not full_name:
            raise forms.ValidationError("Full name is required.")
        if full_name != current_name and self.instance.name_changed_at:
            next_allowed_change = self.instance.name_changed_at + timedelta(days=self.NAME_CHANGE_COOLDOWN_DAYS)
            if timezone.now() < next_allowed_change:
                formatted_date = timezone.localtime(next_allowed_change).strftime('%B %d, %Y')
                raise forms.ValidationError(
                    f"You can change your name again on {formatted_date}. Name changes are limited to once every 60 days."
                )
        return full_name

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if any([current_password, new_password, confirm_new_password]):
            if not current_password:
                self.add_error('current_password', 'Enter your current password to change your password.')
            elif not self.instance.check_password(current_password):
                self.add_error('current_password', 'Current password is incorrect.')

            if not new_password:
                self.add_error('new_password', 'Enter a new password.')

            if not confirm_new_password:
                self.add_error('confirm_new_password', 'Confirm your new password.')

            if new_password and confirm_new_password and new_password != confirm_new_password:
                self.add_error('confirm_new_password', 'New passwords do not match.')

            if new_password and not self.errors.get('new_password') and not self.errors.get('confirm_new_password'):
                validate_password(new_password, self.instance)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].strip()
        current_name = f"{self.instance.first_name} {self.instance.last_name}".strip()
        name_parts = full_name.split(None, 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '').strip()
        if full_name != current_name:
            user.name_changed_at = timezone.now()

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class CustomerProfileForm(forms.ModelForm):
    """Form for customer profile update"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id_number and instance.id_number.startswith('PENDING-ID-'):
            self.initial['id_number'] = ''

    class Meta:
        model = CustomerProfile
        fields = ('address', 'id_type', 'id_number')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'id_type': forms.Select(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if id_number in ('', None):
            if self.instance and self.instance.pk:
                return self.instance.id_number
            return None
        return id_number.strip()

class UserProfileForm(forms.ModelForm):
    """Form for updating required user fields."""
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Leave blank to keep current password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
