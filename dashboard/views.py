from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Consultar las metricicas
from .metrics import *

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


def contable(request):
    """Funcion para calcular metricas del tablero de contabilidad"""
    
    # --- Ingresos ---
    ingresos_qs = pago_sesiones_semanal()
    ingresos_totales = totales_por_metodo_pago(ingresos_qs)
    
    # --- Gastos --- 
    gastos_qs = pagos_pendientes()
    gastos_totales = totales_por_metodo_pago(gastos_qs)
    
    # --- Gastos por terapeuta ---
    gastos_por_terapeutas = calcular_comision(gastos_totales, 1/3)
    
    context = {
        "ingresos_qs":ingresos_qs,
        "gastos_qs": gastos_qs,
        "ingresos":resumen_totales(ingresos_totales),
        "gastos": resumen_totales(gastos_totales),
        "gasto_terapeuta": resumen_totales(gastos_por_terapeutas),
    }
    
    return render(request, "dashboard/contable.html", context=context)


def semanal(request):
    return render(request, "dashboard/semanal.html")


def terapeutas(request):
    return render(request, "dashboard/terapeutas.html")