from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from nucleo.func import ColorCita
from django.contrib import messages

# cargar modelo
from citas.models import Cita

# cargar formularios
from citas.forms import CitaForm

from nucleo.choices import EstadoCita

# Create your views here.
@login_required
def citas(request):
    return render(request, "citas/citas.html")

@login_required
def citas_json(request):
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    citas = Cita.objects.values(
        "cita",
        "fecha",
        "hora",
        "status",
        "paciente_id__nombre",
        "terapeuta_id__nombre",
        )

    eventos = []

    for c in citas:
        eventos.append({
            "id": c["cita"],
            "title": f'{c["terapeuta_id__nombre"]} - {c["paciente_id__nombre"]}',
            "start": f'{c["fecha"]}T{c["hora"]}',
            "color": ColorCita(c["status"]),
        })

    return JsonResponse(eventos, safe=False)

@login_required
def agendar(request):
    if request.method == "POST":
        form = CitaForm(request.POST)
        
        if form.is_valid():
            datos = form.cleaned_data
            existe = Cita.objects.filter(
                fecha=datos["fecha"],
                hora=datos["hora"],
                terapeuta=datos["terapeuta"],
                paciente=datos["paciente"]).exists()
            if existe:
                form.add_error(
                    None,
                    "Esta cita ya se encuentra registrada.")
            else:
                cita = form.save(commit=False)
                cita.status = EstadoCita.CONSULTADO
                
                if request.user.rol != "SISTEMA":
                    cita.terapeuta = request.user
                    
                cita.save()
                
                messages.success(request, "Consulta registrada exitosamente.")
                return redirect("citas:citas")
            
    else:
        form = CitaForm()
        
    return render(request, "citas/agendar.html", {"citaForm": form})

