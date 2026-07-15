from django.db import models
from django.utils import timezone

# Create your models here.
class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    @property
    def edad_actual(self):
        hoy = timezone.now().date()

        return hoy.year - self.fecha_nacimiento.year - (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)

    def __str__(self):
        return f"{self.nombre_completo} | {self.edad_actual} años"
    
    class Meta:
        abstract = True