from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from nucleo.models import Personal

# create your model here.
class Paciente(Personal):
    # ---Datos del paciente---
    id = models.AutoField(primary_key=True)
    diagnostico = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente tiene algún diagnostico")
    alergias = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente es alergico a algún médicamento, alimento, etc.")
    medicamentos = models.CharField(max_length=100, blank=True, null=True, help_text="Indique si el paciente toma actualmente algún medicamento.")
    escuela = models.CharField(max_length=70, help_text="Indique el nombre de la escuela a la que asiste actualmente")

    # ---Datos del padre---
    nombre_padre = models.CharField(max_length=100, blank=True, null=True)
    edad_padre = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(80)])
    telefono_padre = models.CharField(max_length=10, blank=True,null=True, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')])
    ocupacion_padre = models.CharField(max_length=100, blank=True, null=True)

    # ---Datos de la madre---
    nombre_madre = models.CharField(max_length=100, blank=True, null=True)
    edad_madre = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(120)])
    telefono_madre = models.CharField(max_length=10,blank=True, null=True, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')])
    ocupacion_madre = models.CharField(max_length=100, blank=True, null=True)

    # Domicilio donde vive el paciente
    domicilio_paciente = models.CharField(max_length=150)
    
    id_familia = models.IntegerField(
        null=True,
        blank=True,
        help_text="Identificador de hermanos"
    )
    
    # Paciente asiste a consulta
    paciente_activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'pacientes'
    
    
