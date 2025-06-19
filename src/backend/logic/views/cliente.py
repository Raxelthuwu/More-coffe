from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from logic.models import Mesas, ProductosMenu, Pedidos, DetallesPedido

#Esto es lo que ven todos ya sea cliente o un rol de empleado -> el login iria aqui pero con un boton en el HTML
class SeleccionarMesaView(View):
    def get(self, request):
        mesas = Mesas.objects.all()
        return render(request, 'cliente/cliente.html', {'mesas': mesas}) # ud ya sabe como es la vuelta

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
            messages.error(request, "Mesa no encontrada.")
            return redirect('seleccionar_mesa')
        

#muestra el menú de productos disponibles para la mesa seleccionada
class MostrarMenuView(View):
    def get(self, request): 
        mesa_id = request.session.get('mesa_id')
        if not mesa_id:
            messages.error(request, "Primero debes seleccionar una mesa.")
            return redirect('seleccionar_mesa')

        productos = ProductosMenu.objects.all()
        return render(request, 'cliente/menu.html', {'productos': productos})


#envia el pedido al mesero, crea un nuevo pedido si no existe uno para la mesa seleccionada

class EnviarPedidoView(View):
    def post(self, request):
        mesa_id = request.session.get('mesa_id')
        if not mesa_id:
            return redirect('seleccionar_mesa')

        # Diego si lee esto -> Si se presiona "cancelar mesa"
        if request.POST.get('action') == 'cancelar_mesa':
            pedido_id = request.session.get('pedido_id')
            if pedido_id:
                pedido = get_object_or_404(Pedidos, pk=pedido_id)
                if pedido.estado == 'nuevo':
                    pedido.delete()
                    request.session.pop('pedido_id', None)
            request.session.pop('mesa_id', None)
            messages.info(request, "Se canceló la selección de mesa.")
            return redirect('seleccionar_mesa')

        mesa = get_object_or_404(Mesas, pk=mesa_id)

        # Diego si lee esto -> Crear o reutilizar pedido
        pedido_id = request.session.get('pedido_id')
        if pedido_id:
            pedido = get_object_or_404(Pedidos, pk=pedido_id)
        else:
            pedido = Pedidos.objects.create(
                id_mesa=mesa,
                id_empleado_mesero=None,
                fecha_hora_creacion=timezone.now(),
                estado='nuevo',
            )
            request.session['pedido_id'] = pedido.id_pedido

        # Guardar comentario (pongalo en el formulario HTML)
        comentario = request.POST.get('comentario')
        if comentario:
            pedido.comentarios = comentario
            pedido.save()



        # Diego si lee esto -> Agregar productos al pedido
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

        messages.success(request, f"Pedido actualizado para la mesa #{mesa.id_mesa}")
        return redirect('ver_cuenta')


# oe la clase para ver el contenido actual del pedido antes de enviarlo
#al igual, despues que se envie se seguira viendo el pedido actual
class VerPedidoActualView(View):
    def get(self, request):
        pedido_id = request.session.get('pedido_id')
        if not pedido_id:
            messages.error(request, "No tienes un pedido activo.")
            return redirect('seleccionar_mesa')

        pedido = get_object_or_404(Pedidos, pk=pedido_id)
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
        return render(request, 'cliente/ver_cuenta.html', context)


# la clase para cancelar un pedido completamente (ya creado pero no enviado al mesero)
class CancelarPedidoView(View):
    def post(self, request):
        pedido_id = request.session.get('pedido_id')
        if pedido_id:
            pedido = get_object_or_404(Pedidos, pk=pedido_id)
            if pedido.estado == 'nuevo':
                pedido.delete()
                messages.success(request, "Pedido cancelado correctamente.")
        request.session.pop('pedido_id', None)
        request.session.pop('mesa_id', None)
        return redirect('seleccionar_mesa')


# la clase para volver al menú y agregar más productos al pedido actual
class VolverAMenuView(View):
    def get(self, request):
        mesa_id = request.session.get('mesa_id')
        if not mesa_id:
            messages.error(request, "Primero selecciona una mesa.")
            return redirect('seleccionar_mesa')

        productos = ProductosMenu.objects.all()
        return render(request, 'aqui_va_su_html.html', {'productos': productos})



