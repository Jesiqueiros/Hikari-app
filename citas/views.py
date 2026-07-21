from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# cargar modelo
from citas.models import Cita


# Create your views here.
@login_required
def agenda(request):
    return render(request, "citas/agenda.html")

def citas_agendadas(request):
    """Extrae los objectos del modelo Cita"""
    citas = Cita.objects.select_related("paciente", "empleado").values("id", "fecha", "hora", "paciente__nombre", "empleado__nombre")
    lista_cita = []
    
    for cita in citas:
        lista_cita.append({
            "id":cita.id,
            "title": f"{cita.empleado__nombre} ------ {cita.paciente__nombre}",
        })