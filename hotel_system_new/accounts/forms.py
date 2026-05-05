from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser, CustomerProfile


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=17, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        user.email = self.cleaned_data['email']
        user.role_type = 'staff'
        user.is_staff = True
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


class CustomUserUpdateForm(forms.ModelForm):
    """Form for editing user profile information"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=17, required=False)
    role_type = forms.CharField(required=False, disabled=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phone', 'role_type')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role_type': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['role_type'].initial = self.instance.get_role_type_display()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerProfileForm(forms.ModelForm):
    """Form for customer profile update"""
    class Meta:
        model = CustomerProfile
        fields = ('address', 'id_type', 'id_number')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'id_type': forms.Select(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
