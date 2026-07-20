from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            usuario = authenticate(username=email, password=password)
            
            if usuario is not None:
                login(request, usuario)
                return redirect("inicio")
            messages.error(
                request,
                "Correo o contraseña incorrectos."
            )

    return render(request, "accounts/login.html", 
                  {"form": form})