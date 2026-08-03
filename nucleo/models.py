from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Create your models here.
class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def edad_actual(self):
        hoy = timezone.now().date()
        return relativedelta(hoy, self.fecha_nacimiento).years

    def __str__(self):
        return f"{self.nombre_completo}"
    
    class Meta:
        abstract = True