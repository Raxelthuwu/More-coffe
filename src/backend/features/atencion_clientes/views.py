from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Mesas, ProductosMenu, Pedidos, DetallesPedido
from gestion_personal.models import Empleados


# CLIENTE

def seleccionar_mesa(request):
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero_mesa')
        try:
            mesa = Mesas.objects.get(numero_mesa=numero_mesa)
            request.session['id_mesa'] = mesa.id_mesa
            return redirect('mostrar_menu')
        except Mesas.DoesNotExist:
            messages.error(request, "Mesa no encontrada")
    return render(request, 'atencion_clientes/seleccionar_mesa.html')

def mostrar_menu(request):
    productos = ProductosMenu.objects.all()
    return render(request, 'atencion_clientes/menu_interactivo.html', {'productos': productos})

def enviar_pedido(request):
    if request.method == 'POST':
        id_mesa = request.session.get('id_mesa')
        if not id_mesa:
            return redirect('seleccionar_mesa')

        mesa = get_object_or_404(Mesas, pk=id_mesa)
        pedido = Pedidos.objects.create(
            id_mesa=mesa,
            id_empleado_mesero=None,  # aún sin mesero
            fecha_hora_creacion=timezone.now(),
            estado='nuevo',
        )

        for key in request.POST:
            if key.startswith('producto_'):
                id_producto = int(key.split('_')[1])
                cantidad = int(request.POST[key])
                producto = ProductosMenu.objects.get(pk=id_producto)
                DetallesPedido.objects.create(
                    id_pedido=pedido,
                    id_producto_menu=producto,
                    cantidad=cantidad,
                    precio_unitario_venta=producto.precio
                )

        messages.success(request, f"Pedido creado para la mesa {mesa.numero_mesa}")
        return redirect('ver_estado_pedido', id_pedido=pedido.id_pedido)

    return redirect('mostrar_menu')

def ver_estado_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    detalles = DetallesPedido.objects.filter(id_pedido=pedido)
    return render(request, 'atencion_clientes/estado_pedido.html', {'pedido': pedido, 'detalles': detalles})


# MESERO


@login_required
def notificaciones_mesas(request):
    pedidos_sin_mesero = Pedidos.objects.filter(id_empleado_mesero__isnull=True, estado='nuevo')
    return render(request, 'atencion_clientes/notificaciones_mesas.html', {'pedidos': pedidos_sin_mesero})

@login_required
def tomar_mesa(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    empleado = Empleados.objects.get(usuario=request.user)
    pedido.id_empleado_mesero = empleado
    pedido.estado = 'asignado_mesero'
    pedido.save()
    return redirect('ver_pedidos_mesero')

@login_required
def ver_pedidos_mesero(request):
    empleado = Empleados.objects.get(usuario=request.user)
    pedidos = Pedidos.objects.filter(id_empleado_mesero=empleado).exclude(estado='pagado')
    return render(request, 'atencion_clientes/pedidos_asignados.html', {'pedidos': pedidos})

@login_required
def enviar_pedido_cocina(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    pedido.estado = 'enviado_cocina'
    pedido.save()
    return redirect('ver_pedidos_mesero')


# COCINERO


@login_required
def ver_pedidos_cocina(request):
    pedidos = Pedidos.objects.filter(estado='enviado_cocina')
    return render(request, 'atencion_clientes/pedidos_cocina.html', {'pedidos': pedidos})

@login_required
def preparar_pedido(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    pedido.estado = 'en_preparacion'
    pedido.save()
    return redirect('ver_pedidos_cocina')

@login_required
def marcar_preparado(request, id_pedido):
    pedido = get_object_or_404(Pedidos, pk=id_pedido)
    pedido.estado = 'listo'
    pedido.save()
    return redirect('ver_pedidos_cocina')