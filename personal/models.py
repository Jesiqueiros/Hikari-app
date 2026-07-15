from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.utils import timezone
from nucleo.models import Personal

class Personal(AbstractUser, Personal):

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(unique=True, db_index=True)

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        TERAPEUTA = "TERAPEUTA", "Terapeuta"

    rol = models.CharField(max_length=20, choices=Roles.choices)

    numero_personal = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')], help_text="El número debe incluir exactamente 10 dígitos.")

    fecha_ingreso = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'empleados'
    
    
