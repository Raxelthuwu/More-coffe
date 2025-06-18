from django.urls import path
from . import views

urlpatterns = [
    path('limpiar-mesas/', views.limpiar_mesas, name='limpiar_mesas'), 
]
