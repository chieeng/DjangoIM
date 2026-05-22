from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # check empty
        if not username or not password1 or not password2:
            messages.error(request, "All fields required")
            return redirect("accounts:register")

        # password match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("accounts:register")

        # 🔥 THIS PREVENTS YOUR ERROR
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:register")

        # create user safely
        User.objects.create_user(username=username, password=password1)

        messages.success(request, "Account created successfully")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")