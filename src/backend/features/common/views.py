from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.contrib import messages

def limpiar_mesas(request):
    sesiones = Session.objects.all()
    borradas = 0
    for s in sesiones:
        data = s.get_decoded()
        if 'mesa_id' in data or 'pedido_id' in data:
            s.delete()
            borradas += 1
    messages.success(request, f"✔ {borradas} sesiones de mesas/pedidos eliminadas.")
    return redirect('common')
