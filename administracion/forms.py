
from django import forms
from django.utils import timezone

from administracion.models import Gasto, PagoSesion
from personal.models import Empleado

from pacientes.models import Paciente

class GastoForm(forms.ModelForm):
    
    class Meta:
        model = Gasto 
        fields = ["fecha", "categoria","descripcion", "estado_pago", "monto", "metodo_pago", "personal"]
        
        labels = {"fecha": "Fecha del gasto",
                  "categoria": "Categoría",
                  "personal": "Empleado",
                  "descripcion": "Descripción",
                  "monto": "Monto",
                  "metodo_pago": "Método de pago"}
        
        #Widgets
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "descripcion": forms.Textarea(attrs={"class":"textarea", 
                                               "rows":4, 
                                               "placeholder": "Breve descripcion del gasto..."}),
            "categoria": forms.Select(attrs={"class":"select"}),
            "metodo_pago": forms.Select(attrs={"class":"select"}),
            "monto": forms.NumberInput(attrs={"class":"input"}),
            "personal": forms.Select(attrs={"class":"select"}),
        }
        
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        # Personal
        self.fields["personal"].queryset = Empleado \
            .objects.filter( is_active=True) \
            .order_by("id")
        
        # Fecha actual
        self.fields["fecha"].initial = timezone.localdate().isoformat()
        
        
class PagoSesionForm(forms.ModelForm):
    class Meta:
        model = PagoSesion
        fields = (
            "fecha",
            "paciente",
            "paquete",
            "monto",
            "metodo_pago",
            "sesiones_cubiertas",
            "nota_pago",
        )

        labels = {
            "fecha": "Fecha de pago",
            "paciente": "Nombre del paciente",
            "paquete": "Paquete",
            "monto": "Monto",
            "metodo_pago": "Método de pago",
            "sesiones_cubiertas": "Sesiones cubiertas",
            "nota_pago": "Anotaciones",
        }

        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }
    
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        # Personal
        self.fields["paciente"].queryset = Paciente \
            .objects.filter(activo=True) \
            .order_by("nombre")
        
        # Fecha actual
        self.fields["fecha"].initial = timezone.localdate().isoformat()

        

