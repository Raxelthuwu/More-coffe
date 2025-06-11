from django.urls import path
from . import views

urlspatterns = [
    path("", views.atencion_clientes,name="atencion clientes")
]