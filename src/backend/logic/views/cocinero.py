from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from logic.models.atencion import Pedidos, DetallesPedido
from logic.models.inventario import MovimientosInventario
from logic.models.empleados import Empleados


class VerPedidosCocinaView(View):
    """Lista todos los pedidos para la cocina."""
    def get(self, request):
        pedidos = Pedidos.objects.filter(estado__in=['enviado_cocina', 'en_preparacion'])
        return render(request, 'cocina/ver_pedidos_cocina.html', {
            'pedidos': pedidos,
            'es_cocinero': True,
        })


class TomarPedidoCocinaView(View):
    """Permite al cocinero tomar un pedido para preparación."""
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'enviado_cocina':
            messages.error(request, "Este pedido no puede tomarse en este estado.")
            return redirect('ver_pedidos_cocina')

        if pedido.id_empleado_cocinero:
            messages.error(request, "Este pedido ya fue tomado por otro cocinero.")
            return redirect('ver_pedidos_cocina')

        cocinero = Empleados.objects.get(usuario=request.user)
        pedido.id_empleado_cocinero = cocinero
        pedido.estado = 'en_preparacion'
        pedido.save()

        messages.success(request, "Has tomado el pedido para prepararlo.")
        return redirect('ver_detalle_preparacion', pedido_id=pedido.id_pedido)


class VerDetallePreparacionView(View):
    """Muestra detalles para que el cocinero pueda registrar preparación e inventario."""
    def get(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'en_preparacion':
            messages.error(request, "Este pedido no está en preparación.")
            return redirect('ver_pedidos_cocina')

        if pedido.id_empleado_cocinero is None or pedido.id_empleado_cocinero.usuario != request.user:
            messages.error(request, "No estás autorizado para preparar este pedido.")
            return redirect('ver_pedidos_cocina')

        detalles = DetallesPedido.objects.filter(id_pedido=pedido)

        return render(request, 'cocina/ver_detalle_preparacion.html', {
            'pedido': pedido,
            'detalles': detalles,
            'es_cocinero': True,
        })


class FinalizarPedidoCocinaView(View):
    """Cambia el estado de 'en_preparacion' a 'listo' si todos los requisitos se cumplen."""
    def post(self, request, pedido_id):
        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado != 'en_preparacion':
            messages.error(request, "Este pedido no puede finalizarse.")
            return redirect('ver_pedidos_cocina')

        if pedido.id_empleado_cocinero.usuario != request.user:
            messages.error(request, "No estás autorizado para cerrar este pedido.")
            return redirect('ver_pedidos_cocina')

        movimientos = MovimientosInventario.objects.filter(id_pedido=pedido)

        if not movimientos.exists():
            messages.error(request, "Debes registrar los ingredientes usados antes de finalizar.")
            return redirect('ver_detalle_preparacion', pedido_id=pedido.id_pedido)

        pedido.estado = 'listo'
        pedido.save()

        messages.success(request, "Pedido marcado como listo.")
        return redirect('ver_pedidos_cocina')
