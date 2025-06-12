from django.urls import path
from . import views

urlpatterns = [
    path("", views.gestion_personal,name="gestion personal")
]