from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Consultar las metricicas
from .queries import metrica_gastos, metrica_ingresos, tabla_anexo_gastos, tabla_anexo_ingreso
from .charts import grafico_contabilidad

from nucleo.choices import MetodoPago

transferencia = MetodoPago.TRANSFERENCIA
efectivo = MetodoPago.EFECTIVO

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")


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
    
    


def semanal(request):
    return render(request, "dashboard/semanal.html")


def terapeutas(request):
    return render(request, "dashboard/terapeutas.html")