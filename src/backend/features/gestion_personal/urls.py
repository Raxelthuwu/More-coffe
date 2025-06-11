from django.urls import path
from . import views

urlspatterns = [
    path("", views.gestion_personal,name="gestion personal")
]