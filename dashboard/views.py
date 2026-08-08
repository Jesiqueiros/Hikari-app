from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Consultar las metricicas
from .queries import metrica_gastos, metrica_ingresos, tabla_anexo_gastos, tabla_anexo_ingreso, consultas_cobradas
from .charts import grafico_contabilidad

from nucleo.choices import MetodoPago

from personal.models import Empleado

transferencia = MetodoPago.TRANSFERENCIA
efectivo = MetodoPago.EFECTIVO

import polars as pl

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def contable(request):
    """Funcion para calcular metricas del tablero de contabilidad"""
    _, week, _ = timezone.now().isocalendar()
    context = {
        "grafico_contabilidad": grafico_contabilidad(),
        "ingreso": metrica_ingresos(),
        "gasto" : metrica_gastos(),
        "ingresos_qs": tabla_anexo_ingreso(),
        "gastos_qs": tabla_anexo_gastos(),
       "week": week
    }
    return render(request, "dashboard/contable.html", context)
    
    

@login_required
def semanal(request):

    terapeutas = Empleado.objects.filter(
        id__in=(2, 3, 4)
    ).distinct()

    terapeuta_id = request.GET.get("terapeuta")
    
    citas = consultas_cobradas(terapeuta_id)
    
    context = {
        "terapeutas": terapeutas,
        "citas": citas,
        "terapeuta_id": terapeuta_id,
    }

    return render(request, "dashboard/semanal.html", context)

@login_required
def terapeutas(request):
    return render(request, "dashboard/terapeutas.html")