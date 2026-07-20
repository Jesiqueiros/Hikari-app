from django.db import models
from pacientes.models import Pacientes
from uuid import uuid4
from nucleo.choices import MetodoPago, TipoPaquete, CategoriaGasto, EstadoPago
from personal.models import Personal

# Create your models here.
class PagoSesiones(models.Model):
    
    id_pago = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    id_paciente = models.ForeignKey(Pacientes, on_delete=models.PROTECT, db_column="id_paciente")
    
    fecha_pago = models.DateField()
    
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, default=MetodoPago.TRANSFERENCIA)
    
    paquete =  models.CharField(max_length=100, choices=TipoPaquete.choices, null=True, blank=True)
    
    sesiones_cubiertas = models.SmallIntegerField(default=0, help_text="Número máximo de sesiones que cubre este pago", null=True, blank=True)
    
    nota_pago = models.TextField(null=True, blank=True,)
    
    sesiones_asignadas = models.SmallIntegerField(default=0, null=True, blank=True, help_text="Citas asignadas al paquete", editable=True,)
    
    class Meta:
        db_table = "pago_sesiones"
        ordering = ["-fecha_pago"]

class Gastos(models.Model):
    id_gasto = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    fecha_registro = models.DateField()
    
    categoria = models.CharField(choices=CategoriaGasto.choices, max_length=40)
    
    descripcion = models.TextField()
    
    estado_pago = models.CharField(choices=EstadoPago.choices, default=EstadoPago.PENDIENTE, max_length=22)
    
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    
    metodo_pago = models.CharField(choices=MetodoPago.choices, max_length=20, null=True, blank=True)
    
    id_terapeuta = models.ForeignKey(Personal, null=True, blank=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = "gastos"
        ordering = ["-fecha_registro"]