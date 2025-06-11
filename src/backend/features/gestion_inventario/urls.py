from django.urls import path
from . import views

urlspatterns = [
    path("", views.gestion_inventario,name="gestion inventario")
]