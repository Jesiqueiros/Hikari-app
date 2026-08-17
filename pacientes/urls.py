from django.urls import path
from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.pacientes, name="pacientes"),
    path("expediente/", views.expediente, name="expediente"),
    path("cargar_expediente/", views.cargar_expediente, name="cargar_expediente"),
    path("generar_token/", views.generar_token, name="generar_token"),
    path("registro/<uuid:token>", views.registro_con_token, name="registro_con_token"),   
]