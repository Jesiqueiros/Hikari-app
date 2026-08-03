from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from django.db import transaction
from .forms import GastoForm, PagoSesionForm

from .models import PagoSesion
from citas.models import Cita

from django.db.models import F

# Create your views here.
def administracion(request):
    return render(request, "administracion/administracion.html")


@login_required
def gastos(request):
    if request.method == "POST":
        form = GastoForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El gasto se registró correctamente.")
                return redirect("adminstracion:gastos")

            except Exception:
                messages.error(request, "Ocurrió un error al guardar la información. Inténtalo nuevamente.")
        else:
            messages.error(request, "Por favor corrige los errores señalados.")

    else:
        form = GastoForm()

    return render(request, "administracion/gastos.html", {"form": form})


@login_required
def pago_sesion(request):
    
    if request.method == "POST":
        form = PagoSesionForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se registro el pago correctamente.")
                return redirect("administracion:pago_sesion")
            except Exception:
                messages.error(request, "Ocurrio un error al guardar la información")
                
        else:
            messages.error(request, "Corrige los errores señalados")
    
    else:
        form = PagoSesionForm()
        
    context = {
        "form": form
    }
                
    
    return render(request, "administracion/pago_sesion.html", context)


@login_required
def pago_paquetes(request):
    """Carga los paquetes pagado para posteriomente realizar la asignacion de cada pago/paquete con su respectiva sesión."""
    referencia_pago = PagoSesion.objects.filter(sesiones_asignadas__lt=F("sesiones_cubiertas")).order_by("fecha", "paciente_id__nombre")
    
    return render(request, "administracion/pago_paquetes.html", context={"referencias": referencia_pago})


@login_required
def asignar_cita(request, id):
    # Toma el ID de del pago
    pago = get_object_or_404(PagoSesion, pk=id)
    
    citas = Cita.objects.filter(
        pago.paciente.filtro_familia(),
        pago_id__isnull=True,
        fecha__gte=timezone.now() - timedelta(days=60)
    ).order_by("fecha")
    
    if request.method == "POST":
        ids = request.POST.getlist("citas")

        cantidad = len(ids)

        if cantidad > pago.sesiones_cubiertas:
            messages.error(request, f"No puedes asignar más de {pago.sesiones_cubiertas} {"citas" if pago.sesiones_cubiertas > 1 else "cita"}")
            return redirect(
                "contabilidad:asignar_pago_cita",
                pago=id
            )

        with transaction.atomic():
            Cita.objects.filter(pk__in=ids).update(pago=pago)
            pago.sesiones_asignadas += cantidad
            pago.save()

        messages.success(request, "Citas asignadas correctamente.")

        return redirect("contabilidad:citas_pagadas")

    return render(request, "administracion/asignar_cita.html",
                  {"pago": pago,
                   "citas": citas})
    


