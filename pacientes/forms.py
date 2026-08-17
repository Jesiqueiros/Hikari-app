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


class FormularioRegistro(forms.ModelForm):
    class Meta:
        model = Paciente
        exclude = ["id", "activo", "familia", "factura"]

        labels = {
            # Datos del paciente
            "nombre": "Nombre(s)",
            "apellido": "Apellidos",
            "fecha_nacimiento": "Fecha de nacimiento",
            "escuela": "Nombre de la escuela a la que asiste",
            "domicilio": "Domicilio donde vive actualmente",

            # Datos médicos
            "diagnostico": "Diagnóstico",
            "enfermedad_alergia": "Enfermedades y/o alergias",
            "medicacion": "Medicamentos del paciente",

            # Padre (o tutor)
            "padre": "Nombre",
            "padre_telefono": "Número de teléfono",
            "padre_ocupacion": "Ocupación",

            # Madre (o tutora)
            "madre": "Nombre",
            "madre_telefono": "Número de teléfono",
            "madre_ocupacion": "Ocupación",
        }


