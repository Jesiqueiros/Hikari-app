from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Consultar las metricicas
from .queries import *

from personal.models import Empleado

from .charts import grafico_semanal

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def contable(request):
    # cargar datos de queries.py
    tabla_ingreso = tabla_anexo_ingreso()
    tabla_gastos = tabla_anexo_gasto()
    
    # Métrica Ingreso
    ingresos = ingreso_por_metodo(tabla_ingreso)
    
    # Métrica Gasto
    gastos = gasto_por_metodo(tabla_gastos)

    """Funcion para calcular metricas del tablero de contabilidad"""
    _, week, _ = current_day()
    context = {
        "ingreso":{
            "efectivo": ingresos["efectivo"],
            "transferencia": ingresos["transferencia"],
            "total": ingresos["total"]
        },
        "gasto":{
            "efectivo": gastos["efectivo"],
            "transferencia": gastos["transferencia"],
            "total": gastos["total"]
        },
        "ingresos_qs": tabla_ingreso,
        "gastos_qs": tabla_gastos,
        "week": week
    }
    return render(request, "dashboard/contable.html", context)
    
    

@login_required
def semanal(request):
    
    _,semana,_ = current_day()

    terapeutas = Empleado.objects.filter(
        id__in=(2, 3, 4)
    ).distinct()

    terapeuta_id = request.GET.get("terapeuta")
    
    citas_qs = consultas_cobradas(terapeuta_id=terapeuta_id).order_by("fecha", "hora")
    
    # METRICAS DE CONSULTAS COBRADAS
    ingresos = metrica_consultas_cobradas(citas_qs)
    ingreso_efectivo, ingreso_transferencia, ingreso_total = ingresos["efectivo"], ingresos["transferencia"], ingresos["total"] 
    
    # METRICA GASTO POR TERAPEUTA
    gastos =  gasto_por_metodo(tabla_anexo_gasto())
    gasto_efectivo, gasto_transferencia, gasto_total = gastos["efectivo"], gastos["transferencia"], gastos["total"]
    
    # Porcentaje de pago por terapeuta
    porcentaje = 1/terapeutas.count()
    
    gasto_efectivo_terapeuta = gasto_efectivo * porcentaje
    gasto_transferencia_terapeuta = gasto_transferencia * porcentaje
    gasto_total_terapeuta = gasto_total * porcentaje
    
    
    # =========================
    # INGRESO NETO
    # =========================

    neto_efectivo = ingreso_efectivo - gasto_efectivo_terapeuta
    neto_transferencia = (
        ingreso_transferencia - gasto_transferencia_terapeuta
    )
    neto_total = ingreso_total - gasto_total_terapeuta
    
    # Total pacientes
    total_pacientes = citas_qs.count()
    
    # Grafico
    grafico = grafico_semanal(terapeuta_id)
    
    context = {
        "terapeutas": terapeutas,
        "citas": citas_qs,
        "terapeuta_id": terapeuta_id,
        "grafico": grafico,
        "semana": semana,
        "total_pacientes": total_pacientes,

        "ingreso_bruto": {
            "efectivo": ingreso_efectivo,
            "transferencia": ingreso_transferencia,
            "total": ingreso_total,
        },

        "gasto_terapeuta": {
            "efectivo": gasto_efectivo_terapeuta,
            "transferencia": gasto_transferencia_terapeuta,
            "total": gasto_total_terapeuta,
        },

        "ingreso_neto": {
            "efectivo": neto_efectivo,
            "transferencia": neto_transferencia,
            "total": neto_total,
        },
    }

    return render(request, "dashboard/semanal.html", context)

@login_required
def terapeutas(request):
    return render(request, "dashboard/terapeutas.html")