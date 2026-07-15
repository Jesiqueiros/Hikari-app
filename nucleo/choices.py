from django.db import models
from django.utils import timezone

class MetodoPago(models.TextChoices):
    EFECTIVO = "Efectivo", "Efectivo"
    TRANSFERENCIA = "Transferencia", "Transferencia"
    
class TipoPaquete(models.TextChoices):
    INDIVIDUAL = "Individual", "Individual"
    EVALUACION = "Evaluacion", "Evaluación"
    CUATRO_SESIONES = "4 sesiones", "4 sesiones"
    OCHO_SESIONES = "8 sesiones", "8 sesiones"
    DOCE_SESIONES = "12 sesiones", "12 sesiones"
    PAQUETE_COMPARTIDO = "Paquete compartido", "Paquete compartido"

class CategoriaGasto(models.TextChoices):
    HONORARIOS_TERAPEUTAS = "Pago terapeutas", "Pago terapeutas"
    SERVICIOS = "Servicios", "Servicios"
    MATERIAL_TERAPEUTICO = "Material terapéutico", "Material terapéutico"
    PAPELERIA_OFICINA = "Papelería y oficina", "Papelería y oficina"
    LIMPIEZA = "Limpieza", "Limpieza"
    MANTENIMIENTO = "Mantenimiento", "Mantenimiento"
    EQUIPO_MOBILIARIO = "Equipo y mobiliario", "Equipo y mobiliario"
    HERRAMIENTAS_DIGITALES = "Herramientas digitales", "Herramientas digitales"
    MARKETING_PUBLICIDAD = "Marketing y publicidad", "Marketing y publicidad"
    EVENTOS_CELEBRACIONES = "Eventos y celebraciones", "Eventos y celebraciones"
    CONTABILIDAD_ASESORIA_LEGAL = (
        "Contabilidad y asesoría legal",
        "Contabilidad y asesoría legal",
    )
    IMPUESTOS = "Impuestos", "Impuestos"
    OTROS = "Otros", "Otros"

class EstadoPago(models.TextChoices):
    PAGADO = "PAGADO", "Pagado"
    PENDIENTE = "PENDIENTE", "Pendiente"
    PARCIALMENTE_CUBIERTO = "PARCIALMENTE CUBIERTO", "Parcialmente cubierto"


class Hora
HORA_CITAS = [
    (timezone.time(9, 50),  "09:50 A.M."),
    (timezone.time(10, 40), "10:40 A.M."),
    (timezone.time(11, 30), "11:30 A.M."),
    (timezone.time(12, 15), "12:15 P.M."),
    (timezone.time(15, 30), "03:30 P.M."),
    (timezone.time(16, 20), "04:20 P.M."),
    (timezone.time(17, 10), "05:10 P.M."),
    (timezone.time(18, 0),  "06:00 P.M."),
    (timezone.time(18, 45), "06:45 P.M."),
    ]

class estado_cita(models.TextChoices):
    CONSULTADO = "Consultado", "Consultado"
    CONFIRMO = "Confirmo", "Confirmó"
    INNASISTENCIA = "Confirmo pero no asistio", "Confirmó pero no asistió "
    
ESTATUS_CONSULTA_CHOICES = [
    ("Consultado", "Consultado"),
    ("Ausente", "Ausente",
     "Confirmado", "Confirmado",
     "Agendado", "Agendado")]