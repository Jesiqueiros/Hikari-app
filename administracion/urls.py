from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "administracion"

urlpatterns = [
    path("", views.administracion, name="administracion"),
    ]