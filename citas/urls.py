from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "citas"

urlpatterns = [
    path("", views.citas, name="citas"),
    path("datos/", views.citas_json, name="citas_json"),
    path("agendar/", views.agendar, name="agendar")
]