from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from atencion_clientes.models import Mesas, ProductosMenu, Pedidos, DetallesPedido


class SeleccionarMesaView(View):
    def get(self, request):
        mesas = Mesas.objects.all()
        return render(request, 'atencion_clientes/cliente/seleccionar_mesa.html', {'mesas': mesas})

    def post(self, request):
        id_mesa = request.POST.get('mesa_id')
        try:
            mesa = Mesas.objects.get(id_mesa=id_mesa)

            mesa_ocupada = Pedidos.objects.filter(
                id_mesa=mesa,
                estado__in=['nuevo', 'asignado_mesero', 'enviado_cocina', 'en_preparacion']
            ).exists()

            if mesa_ocupada:
                messages.error(request, f"La mesa {mesa.id_mesa} ya está ocupada.")
                return redirect('seleccionar_mesa')

            request.session['mesa_id'] = mesa.id_mesa
            return redirect('mostrar_menu')

        except Mesas.DoesNotExist:
            messages.error(request, "Mesa no encontrada")
            return redirect('seleccionar_mesa')


class MostrarMenuView(View):
    def get(self, request):
        mesa_id = request.session.get('mesa_id')
        if not mesa_id:
            messages.error(request, "Primero debes seleccionar una mesa.")
            return redirect('seleccionar_mesa')

        productos = ProductosMenu.objects.all()
        return render(request, 'atencion_clientes/cliente/menu_interactivo.html', {'productos': productos})


class EnviarPedidoView(View):
    def post(self, request):
        mesa_id = request.session.get('mesa_id')
        if not mesa_id:
            return redirect('seleccionar_mesa')

        if request.POST.get('action') == 'cancelar':
            request.session.pop('mesa_id', None)
            messages.info(request, "Pedido cancelado.")
            return redirect('seleccionar_mesa')

        mesa = get_object_or_404(Mesas, pk=mesa_id)
        pedido = Pedidos.objects.create(
            id_mesa=mesa,
            id_empleado_mesero=None,
            fecha_hora_creacion=timezone.now(),
            estado='nuevo',  
        )

        for key, value in request.POST.items():
            if key.startswith("producto_") and value and int(value) > 0:
                id_producto = int(key.split('_')[1])
                producto = ProductosMenu.objects.get(pk=id_producto)
                DetallesPedido.objects.create(
                    id_pedido=pedido,
                    id_producto_menu=producto,
                    cantidad=int(value),
                    precio_unitario_venta=producto.precio
                )

        # Guardar pedido para la cuenta
        request.session['pedido_id'] = pedido.id_pedido

        messages.success(request, f"Pedido enviado para la mesa #{mesa.id_mesa}")
        return redirect('ver_cuenta_cliente')


class CuentaClienteView(View):
    def get(self, request):
        pedido_id = request.session.get('pedido_id')
        if not pedido_id:
            messages.error(request, "No se encontró un pedido activo.")
            return redirect('seleccionar_mesa')

        pedido = get_object_or_404(Pedidos, pk=pedido_id)

        if pedido.estado == 'pagado':
            messages.info(request, "Este pedido ya fue pagado.")
            request.session.pop('mesa_id', None)
            request.session.pop('pedido_id', None)
            return redirect('seleccionar_mesa')

        detalles = DetallesPedido.objects.filter(id_pedido=pedido)

        detalles_info = []
        total = 0
        for d in detalles:
            subtotal = d.cantidad * d.precio_unitario_venta
            detalles_info.append({
                'producto': d.id_producto_menu.nombre,
                'cantidad': d.cantidad,
                'precio_unitario': d.precio_unitario_venta,
                'subtotal': subtotal
            })
            total += subtotal

        context = {
            'pedido': pedido,
            'detalles': detalles_info,
            'total': total
        }
        return render(request, 'atencion_clientes/cliente/ver_cuenta.html', context)
