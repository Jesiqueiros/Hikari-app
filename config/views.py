from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from pacientes.models import Paciente

@login_required
def inicio(request):
    # Fecha actual
    hoy = timezone.now()
    
    # Información de pacientes
    pacientes = Paciente.objects.filter(activo=True)
    
    # Cumpleañeros del mes
    cumpleaneros_mes = pacientes.filter(fecha_nacimiento__month=hoy.month).order_by("fecha_nacimiento__day")
    
    # Pacientes activos
    pacientes_activos = pacientes.count()
    
    context = {
        "cumpleaneros": cumpleaneros_mes,
        "pacientes_activos": pacientes_activos
    }
    
    return render(request, "inicio.html", context)

def home(request):
    if request.user.is_authenticated:
        return redirect("inicio")

    return redirect("accounts:login")