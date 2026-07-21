from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "citas"

urlpatterns = [
    path("", views.agenda, name="agenda"),
    ]