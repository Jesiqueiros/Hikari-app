from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import GastoForm, PagoSesionForm

# Create your views here.
def administracion(request):
    return render(request, "administracion/administracion.html")


@login_required
def gastos(request):
    if request.method == "POST":
        form = GastoForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El gasto se registró correctamente.")
                return redirect("adminstracion:gastos")

            except Exception:
                messages.error(request, "Ocurrió un error al guardar la información. Inténtalo nuevamente.")
        else:
            messages.error(request, "Por favor corrige los errores señalados.")

    else:
        form = GastoForm()

    return render(request, "administracion/gastos.html", {"form": form})


@login_required
def pago_sesion(request):
    
    if request.method == "POST":
        form = PagoSesionForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Se registro el pago correctamente.")
                return redirect("administracion:pago_sesion")
            except Exception:
                messages.error(request, "Ocurrio un error al guardar la información")
                
        else:
            messages.error(request, "Corrige los errores señalados")
    
    else:
        form = PagoSesionForm()
        
    context = {
        "form": form
    }
                
    
    return render(request, "administracion/pago_sesion.html", context)



