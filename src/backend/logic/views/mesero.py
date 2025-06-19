from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from logic.models import Pedidos, Empleados


class NotificacionesMesasView(LoginRequiredMixin, View):
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

        # Aquí va el HTML que muestra las notificaciones para el mesero
        return render(request, 'aqui_va_el_html_notificaciones_mesero.html', {
            'pedidos': pedidos_nuevos,
            'pedidos_listos': pedidos_listos
        })



class DetallePedidoMeseroView(LoginRequiredMixin, View):
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)
        detalles = pedido.detallespedido_set.all()
        mesero = Empleados.objects.get(usuario=request.user)

        puede_tomar = pedido.estado == 'nuevo' and pedido.id_empleado_mesero is None
        puede_entregar = pedido.estado == 'listo' and pedido.id_empleado_mesero == mesero

        # Aquí va el HTML que muestra el detalle del pedido (pedido + productos + botones)
        return render(request, 'aqui_va_el_html_detalle_pedido.html', {
            'pedido': pedido,
            'detalles': detalles,
            'puede_tomar': puede_tomar,
            'puede_entregar': puede_entregar
        })


class TomarMesaView(LoginRequiredMixin, View):
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


class VerPedidosMeseroView(LoginRequiredMixin, View):
    def get(self, request):
        mesero = Empleados.objects.get(usuario=request.user)
        pedidos = Pedidos.objects.filter(
            id_empleado_mesero=mesero
        ).exclude(estado='pagado')

        # Aquí va el HTML que muestra la lista de pedidos asignados al mesero
        return render(request, 'aqui_va_el_html_pedidos_asignados.html', {
            'pedidos': pedidos
        })


class EnviarPedidoCocinaView(LoginRequiredMixin, View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'asignado_mesero':
            messages.error(request, "Este pedido no puede ser enviado a cocina aún.")
            return redirect('ver_pedidos_mesero')

        pedido.estado = 'enviado_cocina'
        pedido.save()

        messages.success(request, "Pedido enviado a cocina.")
        return redirect('ver_pedidos_mesero')


class EntregarPedidoView(LoginRequiredMixin, View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)
        mesero = Empleados.objects.get(usuario=request.user)

        if pedido.estado != 'listo':
            messages.error(request, "Este pedido no puede marcarse como entregado.")
            return redirect('notificaciones_mesero')

        if pedido.id_empleado_mesero != mesero:
            messages.error(request, "No estás asignado a este pedido.")
            return redirect('notificaciones_mesero')

        pedido.estado = 'entregado'
        pedido.save()

        messages.success(request, f"Pedido entregado a la mesa #{pedido.id_mesa.id_mesa}")
        return redirect('notificaciones_mesero')
