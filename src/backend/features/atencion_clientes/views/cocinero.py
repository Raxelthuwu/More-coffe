from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from atencion_clientes.models import Pedidos

class VerPedidosCocinaView(View):
    def get(self, request):
        pedidos = Pedidos.objects.filter(
            estado__in=['enviado_cocina', 'en_preparacion']
        )
        return render(request, 'atencion_clientes/cocina/pedidos.html', {
            'pedidos': pedidos
        })

class PrepararPedidoView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'enviado_cocina':
            messages.error(request, "Este pedido no está disponible para preparar.")
            return redirect('ver_pedidos_cocina')

        pedido.estado = 'en_preparacion'
        pedido.save()

        messages.success(request, f"Preparando pedido de la mesa #{pedido.id_mesa.id_mesa}")
        return redirect('ver_pedidos_cocina')

class PedidoListoView(View):
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'en_preparacion':
            messages.error(request, "Este pedido no está disponible para marcar como listo.")
            return redirect('ver_pedidos_cocina')

        pedido.estado = 'listo'
        pedido.save()

        messages.success(request, f"Pedido listo para mesa #{pedido.id_mesa.id_mesa}")
        return redirect('ver_pedidos_cocina')
