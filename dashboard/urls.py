from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("contable/", views.contable, name="contable"),
    path("semanal/", views.semanal, name="semanal"),
    path("terapeutas/", views.terapeutas, name="terapeutas")
    
]