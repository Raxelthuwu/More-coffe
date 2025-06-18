from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from atencion_clientes.models import Pedidos
from gestion_personal.models import Empleados 
from django.contrib import messages


class NotificacionesMesasView(View):
    def get(self, request):
        mesero = Empleados.objects.get(usuario=request.user)

        pedidos_nuevos = Pedidos.objects.filter(
            id_empleado_mesero__isnull=True,
            estado='nuevo'
        ).order_by('fecha_hora_creacion')

        pedidos_listos = Pedidos.objects.filter(
            id_empleado_mesero=mesero,
            estado='listo'
        ).order_by('fecha_hora_creacion')

        return render(request, 'atencion_clientes/mesero/notificaciones.html', {
            'pedidos': pedidos_nuevos,
            'pedidos_listos': pedidos_listos
        })



class TomarMesaView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.id_empleado_mesero:
            messages.error(request, "Esta mesa ya fue tomada por otro mesero.")
            return redirect('notificaciones_mesero')

        mesero = Empleados.objects.get(usuario=request.user)

        pedido.id_empleado_mesero = mesero
        pedido.estado = 'asignado_mesero'
        pedido.save()

        messages.success(request, f"Has tomado la mesa #{pedido.id_mesa.id_mesa}")
        return redirect('ver_pedidos_mesero')


class VerPedidosMeseroView(View):
    def get(self, request):
        mesero = Empleados.objects.get(usuario=request.user)
        pedidos = Pedidos.objects.filter(
            id_empleado_mesero=mesero
        ).exclude(estado='pagado')

        return render(request, 'atencion_clientes/mesero/pedidos_asignados.html', {
            'pedidos': pedidos
        })


class EnviarPedidoCocinaView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'asignado_mesero':
            messages.error(request, "Este pedido no puede ser enviado a cocina aún.")
            return redirect('ver_pedidos_mesero')

        pedido.estado = 'enviado_cocina'
        pedido.save()

        messages.success(request, "Pedido enviado a cocina.")
        return redirect('ver_pedidos_mesero')

class EntregarPedidoView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'listo':
            messages.error(request, "Este pedido no puede marcarse como entregado.")
            return redirect('notificaciones_mesero')

        mesero = Empleados.objects.get(usuario=request.user)

        if pedido.id_empleado_mesero != mesero:
            messages.error(request, "No estás asignado a este pedido.")
            return redirect('notificaciones_mesero')

        pedido.estado = 'entregado'
        pedido.save()

        messages.success(request, f"Pedido de la mesa #{pedido.id_mesa.id_mesa} entregado.")
        return redirect('notificaciones_mesero')
