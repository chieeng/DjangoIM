from accounts.models import CustomUser

# Delete existing test users if they exist
CustomUser.objects.filter(username__in=['admin', 'staff']).delete()

# Create Admin
admin = CustomUser.objects.create_user(
    username='admin',
    email='eragritchiegg@gmail.com',
    password='123',
    first_name='Admin',
    last_name='User',
    role_type='admin',
    is_staff=True,
    is_superuser=True
)
print(f"✓ Admin created: {admin.email} / 123")

# Create Staff
staff = CustomUser.objects.create_user(
    username='staff',
    email='ritchieerag@gmail.com',
    password='123',
    first_name='Staff',
    last_name='User',
    role_type='staff',
    is_staff=True
)
print(f"✓ Staff created: {staff.email} / 123")

print("\n✅ Test Accounts Created Successfully!")
print("Email: eragritchiegg@gmail.com | Password: 123 | Role: Admin")
print("Email: ritchieerag@gmail.com | Password: 123 | Role: Staff")
print("Guests can register via the website")
