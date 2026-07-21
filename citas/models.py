from django.db import models
from uuid import uuid4
from administracion.models import PagoSesion
from personal.models import Empleado
from nucleo.choices import Horarios
from pacientes.models import Paciente


# Create your models here.
class Cita(models.Model):
    cita = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pago = models.ForeignKey(PagoSesion, on_delete=models.PROTECT, related_name="citas")
    fecha = models.DateField()
    hora = models.TimeField(null=True,  choices=Horarios)
    terapeuta = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="citas")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name="citas")
    pago_terapeuta = models.BooleanField(default=False)
    