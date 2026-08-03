from django import forms
from django.utils import timezone

from .models import Cita
from pacientes.models import Paciente
from personal.models import Empleado

class CitaForm(forms.ModelForm):
    
    class Meta:
        model = Cita
        fields = ["fecha", "hora", "terapeuta", "liquidada", "paciente"]
        
        labels = {
            "fecha": "Fecha consulta",
            "hora": "Hora consulta",
            "paciente_id": "Nombre del paciente",
            "liquidada": "¿Sé te pago la consulta?",
            "terapeuta": "Nombre Terapeuta"
        }
        
        #Widgets
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "hora": forms.Select(attrs={"class": "input"}),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        

        self.fields["paciente"].queryset = Paciente \
            .objects.filter(activo=True) \
            .order_by("nombre")
        
        self.fields["terapeuta"].queryset = Empleado \
            .objects.filter( is_active=True) \
            .order_by("id")
            
        self.fields["fecha"].initial = timezone.localdate().isoformat()
        

        