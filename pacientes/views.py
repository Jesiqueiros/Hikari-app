from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TokenRegistro
from citas.models import Cita
from administracion.models import PagoSesion
from .forms import ExpedienteForm, FormularioRegistro

from django.db import transaction

from django.urls import reverse

# Create your views here.
def pacientes(request):
    return render(request, "pacientes/pacientes.html")


@login_required
def expediente(request):

    form = ExpedienteForm()

    return render(
        request,
        "pacientes/expediente.html",
        {
            "form": form,
        },
    )


@login_required
def cargar_expediente(request):

    form = ExpedienteForm(request.GET)

    if not form.is_valid():
        return render(
            request,
            "pacientes/partials/expediente.html",
            {
                "form": form,
            },
        )

    paciente = form.cleaned_data["paciente"]

    context = {
        "paciente": paciente,
        "general": form.cleaned_data["general"],
        "notas": form.cleaned_data["notas"],
        "citas": form.cleaned_data["citas"],
        "pagos": form.cleaned_data["pagos"],
    }

    if context["notas"]:
        context["notas_paciente"] = (
            Cita.objects
            .filter(
                paciente=paciente,
            )
            .exclude(nota__isnull=True).exclude(nota="")
            .select_related("terapeuta")
            .order_by("-fecha")
        )

    if context["citas"]:
        context["citas_paciente"] = (
            Cita.objects
            .filter(paciente=paciente)
            .select_related("terapeuta")
            .order_by("-fecha")
        )

    if context["pagos"]:
        context["pagos_paciente"] = (
            PagoSesion.objects
            .filter(paciente=paciente)
            .order_by("-fecha")
        )

    return render(
        request,
        "pacientes/partials/expediente.html",
        context,
    )
    
@login_required
def generar_token(request):
    if request.method == "POST":
        # 1️⃣ Crear token asociado al usuarios
        token = TokenRegistro.objects.create(generado_por=request.user)

        # 2️⃣ Construir la URL dinámica del formulario con ese token
        url_registro = request.build_absolute_uri(
            reverse("pacientes:registro_con_token", args=[str(token.token)])
        )

        # 3️⃣ Mostrar token y enlace generado
        return render(request, "pacientes/generar_token.html", {
            "token": token.token,
            "url_registro": url_registro
        })

    # Si es GET → mostrar botón o formulario para generarlo
    return render(request, "pacientes/generar_token.html")


@transaction.atomic
def registro_con_token(request, token):
    token_registro = get_object_or_404(TokenRegistro,token=token)

    if token_registro.usado:
        return render(request,"pacientes/registro/error.html")

    if request.method == "POST":

        form = FormularioRegistro(request.POST)

        if form.is_valid():

            paciente = form.save()

            token_registro.marcar_usado()

            return render(request, 
                          "pacientes/registro/gracias.html",
                          {"paciente": paciente}
                          )
    else:

        form = FormularioRegistro()

    return render(request, "pacientes/registro/paciente.html",
        {
            "form": form,
        }
    )