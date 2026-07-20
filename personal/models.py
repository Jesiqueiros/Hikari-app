from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from nucleo.models import Personal
from django.contrib.auth.models import UserManager

# Administracion para personal de Hikari
class EmpleadoManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Personal(Personal, AbstractUser):

    username = None
    first_name = None
    last_name = None
    date_joined = None

    email = models.EmailField(unique=True, db_index=True)

    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Administrador"
        TERAPEUTA = "TERAPEUTA", "Terapeuta"

    rol = models.CharField(max_length=20, choices=Roles.choices)

    numero_personal = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'El número debe tener exactamente 10 dígitos.')], help_text="El número debe incluir exactamente 10 dígitos.")

    fecha_ingreso = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = EmpleadoManager
    
    class Meta:
        db_table = 'empleados'