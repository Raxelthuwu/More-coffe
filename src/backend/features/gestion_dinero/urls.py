from django.urls import path
from . import views

urlpatterns = [
    path("", views.gestion_dinero,name = "gestion dinero")
]