from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "administracion"

urlpatterns = [
    path("", views.administracion, name="administracion"),
    path("gastos/", views.gastos, name="gastos" ),
    path("pago_sesion/", views.pago_sesion, name="pago_sesion" )
    ]