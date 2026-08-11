from django.db import connection
from django.utils import timezone
from datetime import timedelta
from nucleo.choices import MetodoPago, EstadoPago
from administracion.models import PagoSesion, Gasto
from citas.models import Cita

from django.db.models import F,ExpressionWrapper, FloatField, IntegerField
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from math import ceil


# Valores para filtrar
transferencia = MetodoPago.TRANSFERENCIA
efectivo = MetodoPago.EFECTIVO

# Regresa la fecha actual para calcular semana, anio y fechas historicas
def current_day():
    
    today = timezone.now()
    
    year, week,_ = today.isocalendar()

    fecha_historica = today.date() - timedelta(weeks=4)
    
    return year, week, fecha_historica


# TABLERO DE CONTABILIDAD. INGRESOS Y GASTOS SEMANALES
def ingresos_historicos_qs():
    _,_,fecha_historica = current_day()
    return PagoSesion.objects.filter(fecha__gte=fecha_historica)

def gastos_historicos_qs():
    _,_,fecha_historica = current_day()
    return Gasto.objects.filter(fecha__gte=fecha_historica)

def tabla_anexo_ingreso():
    year, week, _ = current_day()
    return ingresos_historicos_qs().filter(fecha__week=week, fecha__year=year)

def tabla_anexo_gasto():
    return gastos_historicos_qs().exclude(estado_pago=EstadoPago.PAGADO)

def ingreso_por_metodo(ingreso_qs):
    return ingreso_qs.aggregate(
        efectivo=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.EFECTIVO)), 0, output_field=FloatField()),
        transferencia=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.TRANSFERENCIA)),0,output_field=FloatField()),
        total = Coalesce(Sum("monto"),0,output_field=FloatField()))
    
def gasto_por_metodo(gasto_qs):
    return gasto_qs.aggregate(
        efectivo=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.EFECTIVO)), 0, output_field=FloatField()),
        transferencia=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.TRANSFERENCIA)),0,output_field=FloatField()),
        total = Coalesce(Sum("monto"),0,output_field=FloatField()))

def consultas_cobradas(terapeuta_id):
    # Get objects
    consultas =  Cita.objects.filter(pago_id__isnull=False, liquidada=False, terapeuta_id__in=(2,3,4)) \
        .exclude(pago__sesiones_cubiertas=0).values(
            "fecha", 
            "hora", 
            "terapeuta_id",
            "pago__monto", 
            nombre_terapeuta=F("terapeuta__nombre"),
            nombre_paciente=F("paciente__nombre"),
            forma_pago=F("pago__metodo_pago"),
            sesiones_cubiertas=F("pago__sesiones_cubiertas")
            ) \
            .annotate(precio=ExpressionWrapper(F("pago__monto") / F("sesiones_cubiertas"), output_field=FloatField()))
    
    if terapeuta_id:
        consultas = consultas.filter(terapeuta_id=terapeuta_id)
    
    return consultas


def metrica_consultas_cobradas(qs):
    return qs.aggregate(
        efectivo=Coalesce(Sum("precio", filter=Q(forma_pago=MetodoPago.EFECTIVO)),0,output_field=IntegerField()),
        transferencia=Coalesce(Sum("precio", filter=Q(forma_pago=MetodoPago.TRANSFERENCIA)),0,output_field=IntegerField()),
        total=Coalesce(Sum("precio"), 0, output_field=FloatField())
    )