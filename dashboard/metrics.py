from citas.models import Cita
from administracion.models import PagoSesion, Gasto

from nucleo.choices import MetodoPago, EstadoPago

from django.db.models import ExpressionWrapper, Sum, Count, F, FloatField, Case, When, Q
from django.db.models.functions import Coalesce
from django.utils import timezone

def totales_por_metodo_pago(queryset):
    """ Regresa los totales por métodos de pago"""
    
    return queryset.aggregate(efectivo=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.EFECTIVO)),0.0, output_field=FloatField()),
                              transferencia=Coalesce(Sum("monto", filter=Q(metodo_pago=MetodoPago.TRANSFERENCIA)),0.0, output_field=FloatField()))
    
def resumen_totales(totales):
    return {
        "efectivo": totales["efectivo"],
        "transferencia": totales["transferencia"],
        "total": totales["efectivo"] + totales["transferencia"],
    }

def pago_sesiones_semanal():
    """ Regresa la sesiones pagadas en la semana actual"""
    # Calcula la semana y el año de la fecha actual
    year, week, _ = timezone.now().isocalendar()
    return PagoSesion.objects.filter(fecha__week=week, fecha__year=year)

def pagos_pendientes():
    """Regresa el gasto pendiente o parcialmente cubierto"""
    return Gasto.objects.filter(estado_pago__in=(EstadoPago.PARCIALMENTE_CUBIERTO, EstadoPago.PENDIENTE))

def calcular_comision(totales, porcentaje):
    return {
        "efectivo": totales["efectivo"] * porcentaje,
        "transferencia": totales["transferencia"] * porcentaje,
        "total": (totales["efectivo"] + totales["transferencia"]) * porcentaje,
    }

def citas_cobradas_terapeuta(terapeuta):
    return Cita.objects.filter(pago_id__isnull=False, liquidida=False)

def semanal():
    # Citas cobradas
    citas_cobradas = citas_cobradas_terapeuta()
    
    # Calcular ingreso por metodo de pago
    citas_cobradas = citas_cobradas.aggregate(efectivo=Coalesce(Sum("pago_id__monto", filter=Q(pago_id__metodo_pago=MetodoPago.EFECTIVO)),0.0, output_field=FloatField()),
                              transferencia=Coalesce(Sum("pago_id__monto", filter=Q(pago_id__metodo_pago=MetodoPago.TRANSFERENCIA)),0.0, output_field=FloatField()))

