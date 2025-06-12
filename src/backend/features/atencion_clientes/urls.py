from django.urls import path
from . import views

urlpatterns = [
    path("", views.atencion_clientes,name="atencion clientes")
]