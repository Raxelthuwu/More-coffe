from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from logic.models.inventario import ProductosInventario, MovimientosInventario, UnidadesMedida
from logic.models.empleados import Empleados
from logic.models.atencion import Pedidos
from decimal import Decimal


class VerInventarioView(LoginRequiredMixin, View):
    def get(self, request):
        # Obtener usuario autenticado y su rol
        empleado = get_object_or_404(Empleados, usuario=request.user)
        es_cocinero = empleado.id_rol.nombre_rol.lower() == "cocinero"
        es_administrador = empleado.id_rol.nombre_rol.lower() == "administrador"
        
        # Obtener parámetros de la URL
        pedido_id = request.GET.get('pedido_id')
        origen = request.GET.get('origen')
        
        # Validación para cocineros
        if es_cocinero and not pedido_id:
            raise PermissionDenied("Los cocineros deben acceder desde un pedido")
        
        return render(request, 'inventario/ver_inventario.html', {
            'productos': ProductosInventario.objects.select_related('id_proveedor').filter(activo=True),
            'es_cocinero': es_cocinero,
            'es_administrador': es_administrador,
            'pedido_id': pedido_id,
            'origen': origen
        })

class FormularioMovimientoView(LoginRequiredMixin, View):
    def get(self, request, pedido_id=None):
        empleado = get_object_or_404(Empleados, usuario=request.user)
        es_cocinero = empleado.id_rol.nombre_rol.lower() == "cocinero"
        es_administrador = empleado.id_rol.nombre_rol.lower() == "administrador"

        if es_cocinero and not pedido_id:
            messages.error(request, "Debes registrar movimientos asociados a un pedido.")
            return redirect('ver_pedidos_cocina')

        pedido = get_object_or_404(Pedidos, pk=pedido_id) if pedido_id else None

        return render(request, 'inventario/formulario_movimiento.html', {
            'productos_inventario': ProductosInventario.objects.all(),
            'unidades': UnidadesMedida.objects.all(),
            'es_cocinero': es_cocinero,
            'es_administrador': es_administrador,
            'pedido': pedido,
            'pedido_id': pedido_id,
        })
    def post(self, request, pedido_id=None):
        # Obtener usuario autenticado
        empleado = get_object_or_404(Empleados, usuario=request.user)
        es_cocinero = empleado.id_rol.nombre_rol.lower() == "cocinero"
        es_administrador = empleado.id_rol.nombre_rol.lower() == "administrador"

        # Datos del formulario
        producto_id = request.POST.get('producto_id')
        tipo = request.POST.get('tipo_movimiento')
        cantidad = request.POST.get('cantidad')
        unidad_id = request.POST.get('unidad')
        pedido_id = pedido_id or request.POST.get('pedido_id')

        # Si es cocinero, debe tener pedido
        if es_cocinero and not pedido_id:
            messages.error(request, "Debes registrar movimientos asociados a un pedido.")
            return redirect('ver_pedidos_cocina')

        # Validaciones básicas
        try:
            producto = ProductosInventario.objects.get(pk=producto_id)
            cantidad_decimal = Decimal(cantidad)

            if tipo == 'salida' and cantidad_decimal > producto.stock_actual:
                messages.error(request, "Stock insuficiente")
                if pedido_id:
                    return redirect('formulario_movimiento_pedido', pedido_id=pedido_id)
                return redirect('formulario_movimiento')

        except (ProductosInventario.DoesNotExist, ValueError, InvalidOperation):
            messages.error(request, "Datos inválidos")
            if pedido_id:
                return redirect('formulario_movimiento_pedido', pedido_id=pedido_id)
            return redirect('formulario_movimiento')

        # Actualizar stock
        if tipo == 'entrada':
            producto.stock_actual += cantidad_decimal
        else:
            producto.stock_actual -= cantidad_decimal
        producto.save()

        # Registrar movimiento
        MovimientosInventario.objects.create(
            id_producto_inv=producto,
            id_empleado=empleado,
            id_pedido_id=pedido_id,
            id_unidad_id=unidad_id,
            fecha_hora=timezone.now(),
            tipo_movimiento=tipo,
            cantidad=cantidad_decimal
        )

        messages.success(request, "Movimiento registrado correctamente")

        # Redirección tras guardar
        if pedido_id:
            return redirect('formulario_movimiento_pedido', pedido_id=pedido_id)
        return redirect('formulario_movimiento')
