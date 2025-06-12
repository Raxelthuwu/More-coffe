from django.shortcuts import render
from django.http import HttpResponse

def gestion_personal(request):
    return HttpResponse("Vista de gestión de personal")
