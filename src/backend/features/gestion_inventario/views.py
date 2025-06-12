from django.shortcuts import render
from django.http import HttpResponse

def gestion_inventario(request):
    return HttpResponse("Vista de gestión de inventario")
