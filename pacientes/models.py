from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from nucleo.models import Personal
from uuid import uuid4

from django.db.models import Q

from personal.models import Empleado

from django.utils import timezone

class Familia(models.Model):
    familia = models.AutoField(primary_key=True, editable=False)
    nombre_familia = models.CharField(max_length=100)

    class Meta:
        db_table = 'familias'

class Paciente(Personal):
    id = models.AutoField(primary_key=True)
    diagnostico = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente tiene algún diagnostico")
    enfermedad_alergia = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente es alergico a algún médicamento, alimento, etc.")
    medicacion = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente toma actualmente algún medicamento.")
    escuela = models.CharField(max_length=70, help_text="Indique el nombre de la escuela a la que asiste actualmente", blank=True, null=True)
    padre = models.CharField(max_length=100,blank=True, null=True)
    padre_telefono = models.CharField(max_length=10,blank=True, null=True, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')])
    padre_ocupacion =  models.CharField(max_length=100, blank=True, null=True)
    madre = models.CharField(max_length=100,blank=True, null=True)
    madre_telefono = models.CharField(max_length=10,blank=True, null=True, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')])
    madre_ocupacion =  models.CharField(max_length=100, blank=True, null=True)
    domicilio = models.CharField(max_length=150, help_text="Indique el domicilio en el que actualmente vive el paciente", blank=True, null=True)
    activo = models.BooleanField(default=True)
    factura = models.BooleanField(default=False, help_text="Indique si requiere facturar las citas del paciente")
    familia = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name="pacientes", blank=True, null=True)
    
    def filtro_familia(self):

        if self.familia_id:
            return Q(paciente__familia_id=self.familia_id)

        return Q(paciente=self)

    class Meta:
        db_table = 'pacientes'
        

class TokenRegistro(models.Model):
    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    creado_en = models.DateTimeField(default=timezone.now)
    usado = models.BooleanField(default=False)
    usado_en = models.DateTimeField(null=True, blank=True)
    
    # Opcional: puedes registrar quién generó el token
    generado_por = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True
    )

    def marcar_usado(self):
        """Marcar el token como usado y registrar la fecha."""
        self.usado = True
        self.usado_en = timezone.now()
        self.save()

    def __str__(self):
        return f"Token {self.token} - {'Usado' if self.usado else 'Activo'}"
    
    class Meta:
        db_table = 'token_registro'
    
    
    
    
