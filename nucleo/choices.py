from django.db import models
from datetime import time

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

class estado_cita(models.TextChoices):
    CONSULTADO = "Consultado", "Consultado"
    CONFIRMO = "Confirmo", "Confirmó"
    INNASISTENCIA = "Confirmo pero no asistio", "Confirmó pero no asistió "
    
ESTATUS_CONSULTA_CHOICES = [
    ("Consultado", "Consultado"),
    ("Ausente", "Ausente",
     "Confirmado", "Confirmado",
     "Agendado", "Agendado")]

class Horarios(models.TextChoices):
    HORA_0950 = "09:50", "09:50 A.M."
    HORA_1040 = "10:40", "10:40 A.M."
    HORA_1130 = "11:30", "11:30 A.M."
    HORA_1215 = "12:15", "12:15 P.M."
    HORA_1530 = "15:30", "03:30 P.M."
    HORA_1620 = "16:20", "04:20 P.M."
    HORA_1710 = "17:10", "05:10 P.M."
    HORA_1800 = "18:00", "06:00 P.M."
    HORA_1845 = "18:45", "06:45 P.M."

    @classmethod
    def as_time_choices(cls):
        """Devuelve las opciones como objetos datetime.time."""
        return [
            (time.fromisoformat(valor), etiqueta)
            for valor, etiqueta in cls.choices
        ]