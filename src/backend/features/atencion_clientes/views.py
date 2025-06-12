from django.shortcuts import render
from django.http import HttpResponse

def atencion_clientes(request):
    return HttpResponse("Vista de atención a clientes")
