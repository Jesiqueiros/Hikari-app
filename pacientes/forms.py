from django import forms

from .models import Paciente


class ExpedienteForm(forms.Form):

    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.filter(activo=True).order_by("nombre"),
        label="Selecciona el paciente",
        widget=forms.Select(
            attrs={"class": "select is-fullwidth"}
        ),
    )
    
    general = forms.BooleanField(
        required=False, 
        label="Información General"
    )

    notas = forms.BooleanField(
        required=False,
        label="Notas",
    )

    citas = forms.BooleanField(
        required=False,
        label="Citas",
    )

    pagos = forms.BooleanField(
        required=False,
        label="Pagos",
    )