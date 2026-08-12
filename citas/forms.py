from django import forms
from django.utils import timezone

from .models import Cita
from pacientes.models import Paciente
from personal.models import Empleado

class CitaForm(forms.ModelForm):

    class Meta:
        model = Cita
        fields = [
            "fecha",
            "hora",
            "terapeuta",
            "liquidada",
            "paciente",
            "nota",
        ]

        labels = {
            "fecha": "Fecha consulta",
            "hora": "Hora consulta",
            "paciente": "Nombre del paciente",
            "liquidada": "¿Se te pagó la consulta?",
            "terapeuta": "Nombre Terapeuta",
        }

        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input"
                }
            ),
            "hora": forms.Select(
                attrs={
                    "class": "input"
                }
            ),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        if usuario.rol == "SOCIO":
            self.fields.pop("terapeuta")
            self.fields.pop("liquidada")

        elif usuario.rol == "TERAPEUTA":
            self.fields.pop("terapeuta")

        self.fields["paciente"].queryset = (
            Paciente.objects
            .filter(activo=True)
            .order_by("nombre")
        )

        if "terapeuta" in self.fields:
            self.fields["terapeuta"].queryset = (
                Empleado.objects
                .filter(is_active=True)
                .order_by("id")
            )

        self.fields["fecha"].initial = timezone.localdate()

        