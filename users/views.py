from django.shortcuts import render, redirect
from users.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("notetaking-home")

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form, 'hola': 100})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('notetaking-home')
