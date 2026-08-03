from django.db import models
from uuid import uuid4
from administracion.models import PagoSesion
from personal.models import Empleado
from nucleo.choices import Horarios, EstadoCita
from pacientes.models import Paciente


# Create your models here.
class Cita(models.Model):
    cita = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pago = models.ForeignKey(PagoSesion, on_delete=models.PROTECT, related_name="citas", null=True, blank=True)
    fecha = models.DateField(null=True)
    hora = models.CharField(null=True,  choices=Horarios)
    nota = models.TextField(null=True, blank=True)
    terapeuta = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="citas", null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="citas", null=True, blank=True)
    liquidada = models.BooleanField(default=False)
    status = models.CharField(max_length=22, choices=EstadoCita.choices, null=True, blank=True)
    
    class Meta:
        db_table = 'citas'
    