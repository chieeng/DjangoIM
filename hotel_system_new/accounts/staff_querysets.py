from django.contrib.auth import get_user_model


def staff_user_label(user):
    name = f'{user.first_name} {user.last_name}'.strip()
    return name or user.username


def get_staff_user_queryset():
    """Users who may be assigned operational tasks (housekeeping, maintenance, etc.)."""
    User = get_user_model()
    return User.objects.filter(role_type='staff', is_active=True).order_by(
        'first_name', 'last_name', 'username'
    )
