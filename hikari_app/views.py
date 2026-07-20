from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def inicio(request):
    return render(request, "inicio.html")

def home(request):

    if request.user.is_authenticated:
        return redirect("inicio")

    return redirect("accounts:login")