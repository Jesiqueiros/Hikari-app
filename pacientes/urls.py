from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.pacientes, name="pacientes"),
    path("expediente/", views.expediente, name="expediente"),
    path("cargar_expediente/", views.cargar_expediente, name="cargar_expediente"),
]